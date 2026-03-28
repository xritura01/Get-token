import webview,threading,os,re,base64,json,asyncio,win32crypt,requests,subprocess,sys
from curl_cffi import requests as req
from Crypto.Cipher import AES
token = None
captured_token = None
SUPER_PROPS = base64.b64encode(json.dumps({
    "os": "Windows",
    "browser": "Discord Client",
    "release_channel": "stable",
    "client_version": "1.0.9227",
    "os_version": "10.0.26200",
    "os_arch": "x64",
    "app_arch": "x64",
    "system_locale": "en-GB",
    "has_client_mods": False,
    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9227 Chrome/138.0.7204.251 Electron/37.6.0 Safari/537.36",
    "browser_version": "37.6.0",
    "os_sdk_version": "26200",
    "client_build_number": 509303,
    "native_build_number": 76717,
    "client_event_source": None,
}).encode()).decode()

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9227 Chrome/138.0.7204.251 Electron/37.6.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-GB,en-US;q=0.9,ar-SA;q=0.8",
    "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "X-Debug-Options": "bugReporterEnabled",
    "X-Discord-Locale": "en-US",
    "X-Discord-Timezone": "Europe/London",
    "X-Super-Properties": SUPER_PROPS,
}
INJECT_UI = r"""
(function() {
  const panel = document.createElement('div');
  panel.style.cssText = `position:fixed;top:10px;right:10px;z-index:99999;background:#2b2d31;border:1px solid #404249;border-radius:8px;padding:10px;display:flex;flex-direction:column;gap:6px;font-family:sans-serif;min-width:200px;box-shadow:0 4px 15px rgba(0,0,0,0.5);`;
  panel.innerHTML = `
    <div style="color:#dbdee1;font-size:11px;font-weight:600;margin-bottom:4px;">🔑 TOKEN METHOD</div>
    <button id="btn-login" style="background:#5865f2;color:white;border:none;border-radius:4px;padding:6px 10px;cursor:pointer;font-size:12px;">🌐 Login via Discord</button>
    <button id="btn-browser" style="background:#404249;color:white;border:none;border-radius:4px;padding:6px 10px;cursor:pointer;font-size:12px;">💾 Extract from Browser</button>
    <button id="btn-desktop" style="background:#404249;color:white;border:none;border-radius:4px;padding:6px 10px;cursor:pointer;font-size:12px;">🖥️ Extract from Discord App</button>
    <button id="btn-manual" style="background:#404249;color:white;border:none;border-radius:4px;padding:6px 10px;cursor:pointer;font-size:12px;">✏️ Paste Manually</button>
    <div id="manual-box" style="display:none;flex-direction:column;gap:4px;">
      <input id="token-input" type="password" placeholder="Paste token here..." style="background:#1e1f22;color:white;border:1px solid #404249;border-radius:4px;padding:6px;font-size:12px;outline:none;"/>
      <button id="btn-submit" style="background:#57f287;color:#000;border:none;border-radius:4px;padding:6px;cursor:pointer;font-size:12px;font-weight:600;">Submit</button>
    </div>
    <div id="status" style="color:#949ba4;font-size:10px;text-align:center;"></div>
  `;
  document.body.appendChild(panel);
  const s = document.getElementById('status');
  const ss = (m, c) => { s.textContent = m; s.style.color = c; };
  document.getElementById('btn-login').onclick   = () => ss('Login and token will be captured automatically', '#5865f2');
  document.getElementById('btn-browser').onclick = () => { ss('Searching browser files...', '#faa81a'); window.pywebview.api.extract_from_browser(); };
  document.getElementById('btn-desktop').onclick = () => { ss('Searching Discord app...', '#faa81a'); window.pywebview.api.extract_from_desktop(); };
  document.getElementById('btn-manual').onclick  = () => { const b = document.getElementById('manual-box'); b.style.display = b.style.display === 'none' ? 'flex' : 'none'; };
  document.getElementById('btn-submit').onclick  = () => { const t = document.getElementById('token-input').value.trim(); if (!t) { ss('Enter a token first', '#ed4245'); return; } ss('Validating...', '#faa81a'); window.pywebview.api.on_manual(t); };
  const oFetch = globalThis.fetch;
  globalThis.fetch = async function(...args) { const auth = new Headers(args[1]?.headers || {}).get('Authorization'); if (auth) window.pywebview.api.on_found({ auth }); return oFetch.apply(this, args); };
  const oOpen = XMLHttpRequest.prototype.open;
  const oSet = XMLHttpRequest.prototype.setRequestHeader;
  XMLHttpRequest.prototype.open = function(m, url, ...r) { this._url = url; return oOpen.apply(this, [m, url, ...r]); };
  XMLHttpRequest.prototype.setRequestHeader = function(h, v) { if (h.toLowerCase() === 'authorization') window.pywebview.api.on_found({ auth: v }); return oSet.apply(this, [h, v]); };
})();
"""
VERSION = "v1.0.0"
def DetectEdge():
    return os.path.exists(r"C:\Program Files (x86)\Microsoft\EdgeWebView\Application")
def check_for_updates():
    repo = "xritura01/Get-token"
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        response = requests.get(url, timeout=5).json()
        latest_version = response.get('tag_name')
        if latest_version and latest_version != VERSION:
            if 'assets' in response and len(response['assets']) > 0:
                download_url = response['assets'][0]['browser_download_url']
                return download_url
    except Exception as e:
        print(f"Update check failed: {e}")
    return None
def run_update(download_url):
    current_exe = os.path.realpath(sys.executable)
    exe_directory = os.path.dirname(current_exe)
    exe_name = os.path.basename(current_exe)
    temp_exe_path = os.path.join(exe_directory, "update_temp.exe")
    bat_path = os.path.join(exe_directory, "updater.bat")
    print(f"Downloading update to {temp_exe_path}...")
    try:
        r = requests.get(download_url, stream=True)
        r.raise_for_status()
        with open(temp_exe_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        bat_content = f"""@echo off
timeout /t 2 /nobreak > nul
:loop
del /f "{current_exe}"
if exist "{current_exe}" (
    timeout /t 1 /nobreak > nul
    goto loop
)
ren "{temp_exe_path}" "{exe_name}"
start "" "{current_exe}"
del "%~f0"
"""
        with open(bat_path, "w") as f:
            f.write(bat_content)
        print("Update ready. Restarting...")
        subprocess.Popen([bat_path], shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        sys.exit(0)
    except Exception as e:
        print(f"Update failed: {e}")
        if os.path.exists(temp_exe_path):
            os.remove(temp_exe_path)
def find_browser_tokens():
    paths = {
        "Chrome": os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Local Storage\leveldb"),
        "Edge": os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Local Storage\leveldb"),
        "Brave": os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Local Storage\leveldb"),
    }
    Browser=False
    found = []
    for b, path in paths.items():
        if not os.path.exists(path):
            continue
        Browser = True
        for file in os.listdir(path):
            if not file.endswith((".ldb", ".log")):
                continue
            try:
                with open(os.path.join(path, file), "rb") as f:
                    content = f.read().decode("utf-8", errors="ignore")
                    for t in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27,}", content):
                      if t not in found:
                        found.append(t)
            except:
                continue
    if not Browser:
        window.evaluate_js("document.getElementById('status').textContent = '✗ Compatiable browser is not installed'; document.getElementById('status').style.color = '#ed4245';")
        return None
    return found

def GetMasterKey(app):
    state = os.path.expandvars(f"%APPDATA%\\{app}\\Local State")
    if not os.path.exists(state):
        return None
    try:
        with open(state,"r") as f:
            state = json.load(f)
        encrypted_key = base64.b64decode(state["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except:
        return None
    
def DecryptToken(TokenEnc,MasterKey):
    try:
        data = base64.b64decode(TokenEnc.split("dQw4w9WgXcQ:")[1])
        iv = data[3:15]
        payload = data[15:]
        ciper = AES.new(MasterKey,AES.MODE_GCM,iv)
        return ciper.decrypt(payload)[:-16].decode()
    except:
        return None

def find_dc_tokens():
    apps= {
        "Discord":"Discord",
        "Discord Canary":"discordcanary",
        "Discord PTB":  "discordptb",
    }
    found = []
    client = False
    for app, folder in apps.items():
        path = os.path.expandvars(f"%APPDATA%\\{app}\\Local Storage\\leveldb")
        if not os.path.exists(path):
            continue
        client = True
        MasterKey = GetMasterKey(folder)
        for file in os.listdir(path):
          if not file.endswith((".ldb", ".log")):
              continue
          try:
              with open(os.path.join(path, file), "rb") as f:
                  content = f.read().decode("utf-8", errors="ignore")
              if MasterKey:
                  for m in re.findall(r"dQw4w9WgXcQ:[^\"\\]{20,}", content):
                      token = DecryptToken(m, MasterKey)
                      if token and token not in found:
                          found.append(token)
              for t in re.findall(r"[\w-]{24}\.[\w-]{6}\.[\w-]{27,}", content):
                  if t not in found:
                      found.append(t)
          except:
                continue
    if not client:
        window.evaluate_js("document.getElementById('status').textContent = '✗ Discord Client is not Installed'; document.getElementById('status').style.color = '#ed4245';")
        return None
    return found

async def _validate_token(t):
    headers = {**HEADERS, "Authorization": t}
    session = req.AsyncSession(impersonate="chrome", default_headers=False)
    r = await session.get("https://discord.com/api/v9/users/@me", headers=headers)
    await session.close()
    if r.status_code == 200:
        return r.json()
    return None

def validate_token(t):
    return asyncio.run(_validate_token(t))

def Dropdown(options, callback_name):
    buttons_js = ""
    for i, item in enumerate(options):
        if isinstance(item, tuple):
            value, label = item[0], item[1]
        else:
            value = label = item
        buttons_js += f"""
        const btn{i} = document.createElement('button');
        btn{i}.textContent = '{label}';
        btn{i}.style.cssText = 'background:#404249;color:white;border:none;border-radius:4px;padding:6px;cursor:pointer;font-size:12px;width:100%;text-align:left;';
        btn{i}.onmouseover = () => btn{i}.style.background = '#5865f2';
        btn{i}.onmouseout  = () => btn{i}.style.background = '#404249';
        btn{i}.onclick = () => window.pywebview.api.{callback_name}('{value}');
        document.getElementById('manual-box').appendChild(btn{i});
        """
    return f"""
        document.getElementById('status').textContent = 'Multiple accounts found — pick one:';
        document.getElementById('status').style.color = '#faa81a';
        document.getElementById('manual-box').style.display = 'flex';
        document.getElementById('token-input').style.display = 'none';
        document.getElementById('btn-submit').style.display = 'none';
        {buttons_js}
    """

class API:
    def on_found(self, data):
        global token
        auth = data.get("auth", "")
        if token is None and auth and not auth.startswith("undefined"):
            token = auth
            window.evaluate_js("document.getElementById('status').textContent = '✓ Token captured!'; document.getElementById('status').style.color = '#57f287';")
            threading.Timer(0.8, window.destroy).start()
    def select_token(self,t):
      global token
      token = t
      window.evaluate_js("document.getElementById('status').textContent = '✓ Token selected!'; document.getElementById('status').style.color = '#57f287';")
      threading.Timer(0.8, window.destroy).start()
    def extract_from_browser(self):
        global token
        tokens=find_browser_tokens()
        if tokens is None:
            return
        validated_tokens = []
        for t in find_browser_tokens():
            result = validate_token(t)
            if result:
                validated_tokens.append(t)
        if len(validated_tokens) == 0:
            window.evaluate_js("document.getElementById('status').textContent = '✗ No valid tokens found in browsers'; document.getElementById('status').style.color = '#ed4245';")
        elif len(validated_tokens) > 1:
            for i, t in enumerate(validated_tokens):
                print(f"  [{i+1}] {t}")
            window.evaluate_js(Dropdown(validated_tokens, "select_token"))
        else:
            token = validated_tokens[0]
            threading.Timer(0.8, window.destroy).start()
            window.evaluate_js("document.getElementById('status').textContent = '✓ Found valid token!'; document.getElementById('status').style.color = '#57f287';")
    def extract_from_desktop(self):
        global token
        tokens=find_dc_tokens()
        if tokens is None:
            return
        validated_tokens = []
        for t in find_dc_tokens():
            result = validate_token(t)
            if result:
                validated_tokens.append(t)
        if len(validated_tokens) == 0:
            window.evaluate_js("document.getElementById('status').textContent = '✗ No valid tokens found in desktop apps'; document.getElementById('status').style.color = '#ed4245';")
        elif len(validated_tokens) > 1:
            for i, t in enumerate(validated_tokens):
                print(f"  [{i+1}] {t}")
            window.evaluate_js(Dropdown(validated_tokens, "select_token"))
        else:
            window.evaluate_js("document.getElementById('status').textContent = '✓ Found valid token!'; document.getElementById('status').style.color = '#57f287';")
            threading.Timer(0.8, window.destroy).start()
    def on_manual(self, t):
        result = validate_token(t)
        if result:
            global token
            token = t
            username = result["username"]
            window.evaluate_js(f"document.getElementById('status').textContent = '✓ Valid! Logged in as {username}'; document.getElementById('status').style.color = '#57f287';")
            threading.Timer(0.8, window.destroy).start()
        else:
            window.evaluate_js("document.getElementById('status').textContent = '✗ Invalid token'; document.getElementById('status').style.color = '#ed4245';")

window = None

def RunJS(w):
    w.evaluate_js(INJECT_UI)

def GetToken():
    update = check_for_updates()
    if update:
        print("A New Version is Available")
        choice = input("Would you like to update now? (y/n): ").strip().lower()
        if choice == "y":
            run_update(update)
    global token, window
    token = None
    gui = "edgechromium" if DetectEdge() else print("Unable to find Microsoft Edge Runtime, using QT") ;gui= "qt"
    def on_closed():
        if token is None:
            pass
    window = webview.create_window("Login with Discord","https://discord.com/login",js_api=API(),width=1000,height=700,text_select=False)
    window.events.closed += on_closed
    webview.start(RunJS, window, debug=False,gui=gui)
    if token is None:
        token = input("  Window closed — paste token manually: ").strip()
    r = validate_token(token)
    if not r:
        print("Unable to validate token.")
        return None
    return token
