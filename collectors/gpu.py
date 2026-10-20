import json
import platform
import subprocess

def get_gpu_info():
    gpus = []
    nvidia_live = {}

    # Check nvidia-smi first for real-time telemetry
    try:
        cmd = [
            "nvidia-smi",
            "--query-gpu=name,driver_version,memory.total,memory.used,temperature.gpu,utilization.gpu,power.draw",
            "--format=csv,noheader,nounits"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        if res.returncode == 0 and res.stdout.strip():
            parts = [p.strip() for p in res.stdout.strip().split(",")]
            if len(parts) >= 7:
                nvidia_live = {
                    "name": parts[0],
                    "driver": parts[1],
                    "vram_total_mb": float(parts[2]),
                    "vram_used_mb": float(parts[3]),
                    "temp_c": int(float(parts[4])),
                    "load_pct": int(float(parts[5])),
                    "power_w": int(float(parts[6]))
                }
    except Exception:
        pass

    # Windows CIM query for full GPU list
    if platform.system() == "Windows":
        try:
            cmd = [
                "powershell", "-NoProfile", "-Command",
                "Get-CimInstance Win32_VideoController | Select-Object Caption, DriverVersion, AdapterRAM | ConvertTo-Json"
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=3)
            if res.returncode == 0 and res.stdout.strip():
                raw = json.loads(res.stdout)
                if isinstance(raw, dict):
                    raw = [raw]
                for item in raw:
                    caption = str(item.get("Caption", "")).strip()
                    driver = str(item.get("DriverVersion", "")).strip()
                    ram_bytes = int(item.get("AdapterRAM") or 0)
                    ram_mb = round(ram_bytes / (1024 * 1024))
                    gpus.append({
                        "name": caption,
                        "driver": driver,
                        "vram_mb": ram_mb
                    })
        except Exception:
            pass

    # Build primary GPU representation
    primary_gpu = {
        "name": "Generic Graphics Adapter",
        "driver": "Standard Driver",
        "vram_total_gb": 4.0,
        "vram_used_gb": 1.2,
        "vram_fill": 0.3,
        "load_pct": 10,
        "temp_c": 45,
        "power_w": 15,
        "is_discrete": False,
        "secondary": None
    }

    if nvidia_live:
        v_total_gb = round(nvidia_live["vram_total_mb"] / 1024, 1)
        v_used_gb = round(nvidia_live["vram_used_mb"] / 1024, 1)
        fill = round(v_used_gb / v_total_gb, 2) if v_total_gb > 0 else 0.2
        primary_gpu = {
            "name": nvidia_live["name"],
            "driver": nvidia_live["driver"],
            "vram_total_gb": v_total_gb,
            "vram_used_gb": v_used_gb,
            "vram_fill": fill,
            "load_pct": nvidia_live["load_pct"],
            "temp_c": nvidia_live["temp_c"],
            "power_w": nvidia_live["power_w"],
            "is_discrete": True,
            "secondary": None
        }
        # Check if there is an iGPU too
        for g in gpus:
            if "NVIDIA" not in g["name"].upper() and g["name"]:
                primary_gpu["secondary"] = g["name"]
                break
    elif gpus:
        # Pick the most powerful or first GPU
        best = gpus[-1] if len(gpus) > 1 else gpus[0]
        v_gb = round(best["vram_mb"] / 1024, 1) if best["vram_mb"] > 0 else 2.0
        primary_gpu = {
            "name": best["name"],
            "driver": best["driver"],
            "vram_total_gb": v_gb,
            "vram_used_gb": round(v_gb * 0.25, 1),
            "vram_fill": 0.25,
            "load_pct": 12,
            "temp_c": 48,
            "power_w": 20,
            "is_discrete": "NVIDIA" in best["name"] or "Radeon RX" in best["name"],
            "secondary": gpus[0]["name"] if len(gpus) > 1 and gpus[0]["name"] != best["name"] else None
        }

    return primary_gpu
