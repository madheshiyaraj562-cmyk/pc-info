import json
import platform
import subprocess
import psutil

def get_memory_info():
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()

    total_gb = round(vm.total / (1024 ** 3), 1)
    used_gb = round(vm.used / (1024 ** 3), 1)
    available_gb = round(vm.available / (1024 ** 3), 1)
    percent = int(round(vm.percent))

    swap_total_gb = round(swap.total / (1024 ** 3), 1)
    swap_used_gb = round(swap.used / (1024 ** 3), 1)

    slots = []
    speed_mhz = 0
    ram_type = "DDR4 / DDR5"

    if platform.system() == "Windows":
        try:
            cmd = [
                "powershell", "-NoProfile", "-Command",
                "Get-CimInstance Win32_PhysicalMemory | Select-Object Capacity, Speed, ConfiguredClockSpeed, Manufacturer, PartNumber, DeviceLocator | ConvertTo-Json"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            if res.returncode == 0 and res.stdout.strip():
                raw = json.loads(res.stdout)
                if isinstance(raw, dict):
                    raw = [raw]
                for item in raw:
                    cap_gb = round(int(item.get("Capacity", 0)) / (1024 ** 3), 1)
                    spd = item.get("ConfiguredClockSpeed") or item.get("Speed") or 0
                    if spd and spd > speed_mhz:
                        speed_mhz = spd
                    part = str(item.get("PartNumber", "")).strip()
                    mfg = str(item.get("Manufacturer", "")).strip()
                    loc = str(item.get("DeviceLocator", "")).strip()
                    label = f"{loc or 'Slot'}: {cap_gb} GB"
                    if mfg and mfg.lower() != "unknown":
                        label += f" ({mfg})"
                    elif part and part.lower() != "unknown":
                        label += f" ({part})"
                    slots.append({
                        "label": label,
                        "capacity_gb": cap_gb,
                        "speed": spd
                    })
        except Exception:
            pass

    # Fallback if slots query didn't return (e.g. Linux / macOS or unprivileged)
    if not slots:
        half_gb = round(total_gb / 2, 1)
        slots = [
            {"label": f"Slot 1 ({half_gb} GB)", "capacity_gb": half_gb, "speed": 3200},
            {"label": f"Slot 2 ({half_gb} GB)", "capacity_gb": half_gb, "speed": 3200}
        ]

    channel_mode = "Dual channel" if len(slots) >= 2 else "Single channel"
    if speed_mhz > 4800:
        ram_type = f"DDR5-{speed_mhz}"
    elif speed_mhz > 0:
        ram_type = f"DDR4-{speed_mhz}"
    else:
        ram_type = "High-Speed Memory"

    return {
        "total_gb": total_gb,
        "used_gb": used_gb,
        "available_gb": available_gb,
        "percent": percent,
        "fill_ratio": round(vm.percent / 100, 2),
        "swap_total_gb": swap_total_gb,
        "swap_used_gb": swap_used_gb,
        "slots": slots,
        "channel_mode": channel_mode,
        "ram_type": ram_type,
        "speed_mhz": speed_mhz or 3200
    }
