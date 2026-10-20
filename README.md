# pc-info 🖥️

A lightweight, cross-platform Python CLI tool that gathers full hardware diagnostic details about your computer and generates a beautiful, standalone, privacy-safe HTML dashboard to share with friends, communities, or repair shops.

---

## 🚀 How to Run Commands

### 1. View the Help Screen & Options Guide
```powershell
pc-info --help
```
*(You can also use `-h` or `pc-info help`).*

### 2. Full Terminal Diagnostic Report
```powershell
pc-info
```
* Shows the comprehensive hardware breakdown (CPU, GPU, RAM, Storage, Sensors, Network, Security, Startup, Dev Tools, and Quick Analysis).
* Includes a clean **"Press 'q' or Enter to quit"** prompt at the end so terminal windows do not close automatically.

### 3. Generate & Open the HTML Dashboard
```powershell
pc-info --html
```
* Generates `report.html` and automatically opens it in your default web browser.
* You can specify a custom filename: `pc-info --html my_specs.html`.

### 4. 🛡️ Safe Mode (Mask Sensitive Info)
```powershell
pc-info --safe
# or generate a safe HTML file to send to someone:
pc-info --html safe_report.html --safe
```
* Redacts hostname, username, IP address, MAC address, and Wi-Fi SSID.

### 5. Quick Neofetch-style Summary
```powershell
pc-info --fetch
```
