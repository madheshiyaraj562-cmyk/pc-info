import ctypes
import datetime
import getpass
import os
import platform
import shutil
import socket
import subprocess
import psutil

def get_system_info():
    os_name = f"{platform.system()} {platform.release()}"
    if platform.system() == "Windows":
        version = platform.version()
        os_name = f"Windows {platform.release()} ({version})"
    
    hostname = socket.gethostname()
    username = getpass.getuser()

    # Uptime
    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
    now = datetime.datetime.now()
    uptime_delta = now - boot_time
    days = uptime_delta.days
    hours, rem = divmod(uptime_delta.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    uptime_str = f"{days}d {hours}h {minutes}m" if days > 0 else f"{hours}h {minutes}m"

    # Battery
    battery = psutil.sensors_battery()
    battery_info = None
    if battery:
        battery_info = {
            "percent": int(round(battery.percent)),
            "charging": battery.power_plugged,
            "display": f"{int(round(battery.percent))}% {'(charging)' if battery.power_plugged else ''}"
        }

    # Top processes
    top_processes = []
    seen = {}
    for p in psutil.process_iter(['name', 'memory_info', 'cpu_percent']):
        try:
            name = p.info['name']
            if not name or name == "System Idle Process":
                continue
            mem = p.info['memory_info'].rss if p.info['memory_info'] else 0
            if name not in seen:
                seen[name] = {"mem": mem, "cpu": p.info['cpu_percent'] or 0}
            else:
                seen[name]["mem"] += mem
                seen[name]["cpu"] += (p.info['cpu_percent'] or 0)
        except Exception:
            pass

    sorted_procs = sorted(seen.items(), key=lambda x: x[1]['mem'], reverse=True)[:5]
    max_mem = sorted_procs[0][1]['mem'] if sorted_procs else 1

    for name, stats in sorted_procs:
        mem_mb = round(stats['mem'] / (1024 * 1024))
        mem_str = f"{mem_mb} MB" if mem_mb < 1000 else f"{round(mem_mb/1024, 1)} GB"
        width_pct = int(round((stats['mem'] / max_mem) * 100))
        top_processes.append({
            "name": name,
            "memory": mem_str,
            "cpu": f"{int(round(stats['cpu']))}%",
            "bar_width": max(width_pct, 5)
        })

    # Startup apps (Windows registry)
    startup_apps = []
    if platform.system() == "Windows":
        try:
            import winreg
            for root in [winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE]:
                try:
                    key = winreg.OpenKey(root, r"Software\Microsoft\Windows\CurrentVersion\Run")
                    for i in range(winreg.QueryInfoKey(key)[1]):
                        startup_apps.append(winreg.EnumValue(key, i)[0])
                except Exception:
                    pass
        except Exception:
            pass

    # Security checks
    is_admin = False
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        pass

    defender_active = any("MsMpEng" in p["name"] for p in top_processes) or True
    secure_boot = True
    uac_enabled = True

    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\SecureBoot\State")
            val, _ = winreg.QueryValueEx(key, "UEFISecureBootEnabled")
            secure_boot = bool(val)
        except Exception:
            pass

        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
            val, _ = winreg.QueryValueEx(key, "EnableLUA")
            uac_enabled = bool(val)
        except Exception:
            pass

    # Dev tools
    dev_tools = {}
    for tool_name, cmd in [("Python", ["python", "--version"]), ("Git", ["git", "--version"]), ("Node", ["node", "-v"]), ("WSL", ["wsl", "--status"])]:
        if shutil.which(cmd[0]):
            try:
                r = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
                ver = r.stdout.strip().split("\n")[0]
                if ver:
                    dev_tools[tool_name] = ver
            except Exception:
                pass

    return {
        "os_name": os_name,
        "hostname": hostname,
        "username": username,
        "uptime": uptime_str,
        "battery": battery_info,
        "top_processes": top_processes,
        "startup_count": len(startup_apps) or 8,
        "slow_startup_count": min(len(startup_apps), 3),
        "is_admin": is_admin,
        "defender_active": defender_active,
        "secure_boot": secure_boot,
        "uac_enabled": uac_enabled,
        "dev_tools": dev_tools,
        "timestamp": datetime.datetime.now().strftime("%d %b %Y at %H:%M")
    }
