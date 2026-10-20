# pc-info 🖥️

A lightweight, cross-platform CLI tool that reports your computer's hardware details and generates a standalone, privacy-safe HTML dashboard.

## Features

- Full hardware report: CPU, GPU, RAM, storage, sensors, network, security and more
- Shareable HTML dashboard
- Safe mode that masks hostname, username, IP, MAC and Wi-Fi SSID
- Neofetch-style quick summary

## Installation

Requires Python 3. On Windows, install it with `winget install Python.Python.3.12`, then open a new terminal.

```
pip install https://github.com/madheshiyaraj562-cmyk/pc-info/archive/refs/heads/main.zip
```

Or with Git:

```
pip install git+https://github.com/madheshiyaraj562-cmyk/pc-info.git
```

## Usage

| Command | Description |
|---|---|
| `pc-info` | Full terminal report |
| `pc-info --help` | Show all options |
| `pc-info --html` | Generate and open `report.html` |
| `pc-info --html my_specs.html` | Use a custom file name |
| `pc-info --safe` | Mask sensitive info |
| `pc-info --html safe_report.html --safe` | Shareable safe report |
| `pc-info --fetch` | Quick neofetch-style summary |

> 💡 Use `--safe` before sharing a report with anyone.

## Uninstall

```
pip uninstall pc-info -y
```

## Author

Made by Raj Madheshiya @ 2026

## License

MIT License
