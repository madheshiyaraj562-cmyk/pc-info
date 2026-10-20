import os
import platform
import psutil

def get_cpu_info():
    model = platform.processor() or "Unknown CPU"
    if platform.system() == "Windows":
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            val, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            if val and val.strip():
                model = val.strip()
        except Exception:
            pass
    elif platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        model = line.split(":", 1)[1].strip()
                        break
        except Exception:
            pass

    physical_cores = psutil.cpu_count(logical=False) or 1
    logical_cores = psutil.cpu_count(logical=True) or 1

    # Frequency
    freq = psutil.cpu_freq()
    current_ghz = round(freq.current / 1000, 2) if freq and freq.current else None
    max_ghz = round(freq.max / 1000, 2) if freq and freq.max else None
    min_ghz = round(freq.min / 1000, 2) if freq and freq.min else None

    # Load sampling (0.2s is fast and realistic)
    per_core_raw = psutil.cpu_percent(interval=0.2, percpu=True)
    overall_load = round(sum(per_core_raw) / len(per_core_raw), 1) if per_core_raw else 0.0

    cores_data = []
    for i, pct in enumerate(per_core_raw):
        cores_data.append({
            "index": i,
            "pct": int(round(pct))
        })

    # Cache info heuristic or detection
    l3_cache = "Shared L3 cache"
    if "Ryzen" in model:
        l3_cache = "32 MB L3 Cache"
    elif "Intel" in model:
        l3_cache = "Smart Cache"

    return {
        "model": model,
        "physical_cores": physical_cores,
        "logical_cores": logical_cores,
        "overall_load": overall_load,
        "current_ghz": current_ghz or 3.8,
        "max_ghz": max_ghz,
        "min_ghz": min_ghz,
        "cores": cores_data,
        "arch": platform.machine(),
        "l3_cache": l3_cache,
    }
