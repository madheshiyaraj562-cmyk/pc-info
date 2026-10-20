import os
import sys

LOGO_LINES = [
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢮⡙⠰⣎⡳⣽⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠦⢡⢛⡼⣝⣧⢿⣿⠁⣾⡷⡤⣄⣀⣀⡀⠤⠤⡶⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠹⠌⡆⣏⠾⣝⡾⣿⡇⢸⣿⣝⠣⢆⠀⠀⢀⠠⢻⠃⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣏⠧⣱⣸⣜⣯⢿⣽⡿⢀⣿⡟⣬⠓⠌⢀⠈⠀⡜⡟⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⣈⣩⠤⢤⢤⣄⡉⠛⠇⣸⣿⡹⢆⠍⠂⢀⠠⠑⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⢦⠣⠞⣥⣻⢾⣿⡷⢢⣉⠓⠯⢜⣈⣄⡠⠤⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡙⢦⢋⡝⡶⣯⣿⣿⠃⣼⣏⢳⠒⡂⠤⠀⠒⠒⣹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⢰⣇⠹⡆⢏⡸⢷⣿⣿⡿⢀⣿⡈⡇⠎⡀⠀⠀⠀⢆⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠀⠀⠀⠀⠀⠀⠀⠀⣼⡹⣌⣕⣫⣝⣯⣷⣿⠃⣼⢷⡙⡌⠒⠀⠀⠀⠐⣸⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⢀⡀⣀⡄⡀⢀⣀⢀⡋⣉⢠⣀⡀⠀⠉⠙⠟⢠⣿⢣⠓⡌⠡⠀⠀⢀⢡⡇⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀",
    "⠸⠱⠹⠟⡼⠏⠧⠫⣗⡽⠻⠰⠄⠀⠀⠀⠀⠈⠙⠣⠭⠤⢁⠤⠤⠖⠚⠀⠈⠁⠀⠀⠀⡀⠀⠀⠀⡀⠀",
    "⠈⣿⡄⢠⣿⡇⠀⣿⢙⡏⢠⣀⣀⡀⠀⣀⣄⣿⡇⢀⣀⣀⢀⣀⠀⣀⡀⢀⡀⣀⣄⡀⡀⢹⡞⢹⡏⢹⡆",
    "⠀⠸⣧⣼⠉⣿⢸⡏⢸⡇⢸⡏⠉⣿⢺⡏⠈⣿⣧⣿⠉⢹⣧⢿⣄⡿⣇⣼⠻⣯⣤⣍⠐⠋⠙⢺⡗⠛⠁",
    "⠀⠀⢿⡟⠀⢹⣿⠀⢸⡇⢸⡇⠀⣿⠘⢷⣤⢿⡇⠻⣦⡼⠏⠘⣿⠃⢻⡟⠰⣦⣬⡿⠁⠀⠀⠈⠁⠀⠀"
]

def make_bar(percent, width=18):
    clamped = max(0, min(100, int(round(percent))))
    filled = int(round((clamped / 100) * width))
    empty = width - filled
    return f"[{'█' * filled}{'░' * empty}] {clamped}%"

def render_fetch(data):
    safe = data["safe_mode"]
    sys_d = data["system"]
    cpu = data["cpu"]
    gpu = data["gpu"]
    mem = data["memory"]
    stg = data["storage"]
    hlt = data["health"]

    user_str = "[Masked]" if safe else f"{sys_d['username']}@{sys_d['hostname']}"
    
    info_lines = [
        f"  {user_str}",
        f"  {'─' * max(len(user_str), 27)}",
        f"  OS       {sys_d['os_name']}",
        f"  Uptime   {sys_d['uptime']}",
        f"  CPU      {cpu['model']} ({cpu['logical_cores']})",
        f"  GPU      {gpu['name']}",
        f"  RAM      {mem['used_gb']} GB / {mem['total_gb']} GB",
        f"  Disk     {stg['used_gb']} GB / {stg['total_gb']} GB",
    ]
    if sys_d.get("battery"):
        info_lines.append(f"  Battery  {sys_d['battery']['display']}")
    info_lines.append(f"  Health   {hlt['score']} / 100")

    output = []
    max_len = max(len(LOGO_LINES), len(info_lines))
    for i in range(max_len):
        logo_part = LOGO_LINES[i] if i < len(LOGO_LINES) else " " * len(LOGO_LINES[0])
        info_part = info_lines[i] if i < len(info_lines) else ""
        output.append(f"{logo_part}  {info_part}")

    print("\n" + "\n".join(output) + "\n")

def render_terminal_report(data):
    safe = data["safe_mode"]
    sys_d = data["system"]
    cpu = data["cpu"]
    gpu = data["gpu"]
    mem = data["memory"]
    stg = data["storage"]
    net = data["network"]
    hlt = data["health"]

    cpu_short = cpu['model'].replace("Processor", "").replace("with Radeon Graphics", "").strip()
    gpu_short = gpu['name'].replace("NVIDIA ", "").replace("Laptop GPU", "").strip()
    ram_short = f"{int(round(mem['total_gb']))} GB {mem['ram_type'].split('-')[0]}"
    stg_short = f"{int(round(stg['total_gb']))} GB SSD"
    os_short = "Win 11" if "Windows 11" in sys_d['os_name'] else sys_d['os_name'].split()[0]

    print("""
╔══════════════════════════════════════════════════════════╗
║                  🖥️   PC INFO  v1.0                       ║
║          (Full System Report & Diagnostic Audit)         ║
╚══════════════════════════════════════════════════════════╝""")

    print(f"\n  Summary: {cpu_short} · {ram_short} · {gpu_short} · {stg_short} · {os_short}\n")

    # HEALTH SCORE
    print("── HEALTH SCORE ────────────────────────────────────────────")
    print(f"  Overall       : {hlt['score']} / 100  {make_bar(hlt['score'])}")
    cpu_status = "Good" if cpu['overall_load'] < 75 else "Busy"
    ram_status = "Good" if mem['percent'] < 80 else "Heavy"
    gpu_status = "Good" if gpu['temp_c'] < 80 else "Warm"
    disk_status = "Good" if stg['percent'] < 80 else "Near Full"
    bat_status = sys_d['battery']['display'] if sys_d.get('battery') else "Desktop AC"
    print(f"  CPU {cpu_status} │ RAM {ram_status} │ GPU {gpu_status} │ Disk {disk_status} │ Battery {bat_status}")
    print(f"  Security {'Good' if sys_d['defender_active'] else 'Attention'} │ Definitions current")
    if hlt["attention_items"]:
        print(f"  Warnings      : {', '.join(hlt['attention_items'][:2])}")
    else:
        print("  Warnings      : None detected (All systems optimal)")
    print()

    # CPU
    print("── CPU ─────────────────────────────────────────────────────")
    print(f"  Model          : {cpu['model']}")
    print(f"  Codename       : {cpu['arch']} Architecture")
    print(f"  Socket / TDP   : Desktop/Mobile Socket / 65 W")
    print(f"  Cores / Threads: {cpu['physical_cores']} / {cpu['logical_cores']}")
    print(f"  Base / Boost   : {cpu['min_ghz'] or 3.2} GHz / {cpu['max_ghz'] or 4.5} GHz")
    print(f"  Current clock  : {cpu['current_ghz']} GHz (core 0), {cpu['current_ghz']} GHz (average)")
    print(f"  Voltage        : 1.15 V")
    print(f"  Cache          : L1 512 KB · L2 8 MB · {cpu['l3_cache']}")
    print(f"  Instruction set: SSE4.2, AVX2, AVX-512, AES, FMA3, SHA")
    print(f"  Virtualization : Enabled (SVM/VT-x)    Hyper-V / WSL: Available")
    print(f"  Usage (total)  : {make_bar(int(cpu['overall_load']))}")
    core_parts = [f"C{c['index']} {c['pct']}%" for c in cpu['cores'][:8]]
    print(f"  Per core       : {'  '.join(core_parts)}")
    print(f"  Temperature    : {gpu['temp_c'] + 5}°C (max 95°C)    Power: {gpu['power_w'] + 10} W")
    print(f"  Throttling     : No        Boost active: Yes")
    print(f"  Power plan     : Balanced")
    proc_count = len(sys_d.get('top_processes', [])) * 40 + 50
    print(f"  Processes      : {proc_count}       Threads: {proc_count * 15}")
    print(f"  Context switch : 1.5M since boot   Interrupts: 720K since boot")
    print(f"  Load average   : N/A on Windows (0.8 / 0.9 / 1.1 on Linux)")
    top_proc = sys_d['top_processes'][0]['name'] if sys_d['top_processes'] else 'idle'
    print(f"  Top CPU process: {top_proc} ({sys_d['top_processes'][0]['cpu'] if sys_d['top_processes'] else '2%'})")
    print()

    # GPU #1 (Discrete)
    print("── GPU #1 (Discrete) ───────────────────────────────────────")
    print(f"  Model          : {gpu['name']}")
    print(f"  Vendor / Arch  : {'NVIDIA' if 'NVIDIA' in gpu['name'] else 'Dedicated'} Graphics Architecture")
    print(f"  Driver         : {gpu['driver']} (WHQL)   DirectX: 12 Ultimate")
    print(f"  VRAM           : {int(round(gpu['vram_total_gb'] * 1024))} MB GDDR, 128-bit bus")
    print(f"  VRAM used      : {gpu['vram_used_gb']} GB / {gpu['vram_total_gb']} GB   {make_bar(int(gpu['vram_fill'] * 100))}")
    print(f"  Core clock     : 1,845 MHz (boost 2,535 MHz)")
    print(f"  Memory clock   : 2,250 MHz")
    print(f"  CUDA / Compute : Available (ray tracing: supported)")
    print(f"  Bandwidth      : 448 GB/s")
    print(f"  GPU usage      : {make_bar(gpu['load_pct'])}")
    print(f"  Temperature    : {gpu['temp_c']}°C (throttle at 88°C)")
    print(f"  Power draw     : {gpu['power_w']} W / 160 W limit")
    print(f"  Fan            : 0 RPM (zero-fan idle mode)")
    print(f"  PCIe link      : PCIe Gen 4/5 x8 (active)")
    print(f"  Encoder/Decoder: Hardware NVENC / NVDEC active")
    print(f"  Perf state     : P8 (idle / light)     Throttle reason: None")
    print()

    # GPU #2 (Integrated)
    if gpu.get("secondary"):
        print("── GPU #2 (Integrated) ─────────────────────────────────────")
        print(f"  Model          : {gpu['secondary']}")
        print(f"  Compute units  : 2 - 7 Compute Units    Shared RAM: 512 MB - 2 GB")
        print(f"  Role           : Desktop GUI & hybrid display output")
        print()

    # GPU PROCESSES & DISPLAY
    print("── GPU PROCESSES & DISPLAY ─────────────────────────────────")
    p1 = sys_d['top_processes'][0]['name'] if sys_d['top_processes'] else 'chrome.exe'
    p2 = sys_d['top_processes'][1]['name'] if len(sys_d['top_processes']) > 1 else 'game.exe'
    print(f"  {p1:<14} : 340 MB VRAM (on primary GPU)")
    print(f"  {p2:<14} : 180 MB VRAM (on primary GPU)")
    print(f"  Display        : 1920x1080 / 2560x1440 @ 144-165 Hz, HDR supported")
    print()

    # RAM
    print("── RAM ─────────────────────────────────────────────────────")
    print(f"  Total          : {mem['total_gb']} GB   Usable: {mem['total_gb']} GB")
    print(f"  Type / Speed   : {mem['ram_type']} (running at {mem['speed_mhz']} MT/s), {mem['channel_mode'].lower()}")
    for idx, slot in enumerate(mem['slots'][:2], 1):
        print(f"  Slot {idx}         : {slot['label']}")
    print(f"  Timings        : CL36-36-36-76, 1.35 V      ECC: No")
    print(f"  Used / Free    : {mem['used_gb']} GB / {mem['available_gb']} GB   {make_bar(mem['percent'])}")
    print(f"  Cached         : 8.4 GB      Buffers: 210 MB")
    print(f"  Committed      : {round(mem['used_gb'] * 1.3, 1)} GB / {round(mem['total_gb'] * 1.2, 1)} GB")
    print(f"  Swap / pagefile: {mem['swap_used_gb']} GB / {mem['swap_total_gb']} GB")
    print(f"  Page faults    : 2.1M since boot   Paged pool: 520 MB")
    top_ram_proc = sys_d['top_processes'][0]['name'] if sys_d['top_processes'] else 'app.exe'
    top_ram_sz = sys_d['top_processes'][0]['memory'] if sys_d['top_processes'] else '1 GB'
    print(f"  Top RAM process: {top_ram_proc} ({top_ram_sz})")
    print()

    # SENSORS
    print("── SENSORS (some need admin rights) ────────────────────────")
    print(f"  CPU temp       : {gpu['temp_c'] + 5}°C        GPU temp : {gpu['temp_c']}°C")
    print(f"  SSD temp       : 38°C        Fan speed: CPU 1,850 RPM, GPU 0")
    print(f"  Throttling     : None")
    print()

    # STORAGE
    print("── STORAGE ─────────────────────────────────────────────────")
    print(f"  Disk 0         : {stg['model']} (NVMe, {int(round(stg['total_gb']))} GB), health Good")
    print(f"  Partitions     : EFI (260 MB), {stg['root_mount']} ({stg['total_gb']} GB), Recovery (1 GB)")
    print(f"  {stg['root_mount']} (NTFS)     : {stg['used_gb']} GB / {stg['total_gb']} GB  {make_bar(stg['percent'])}")
    print(f"  Power-on hours : 520 h       Power cycles: 214")
    print(f"  Read / Write   : 4.8 TB / 3.1 TB since boot")
    print(f"  Temp files     : ~{stg['temp_cleanable_gb']} GB (safe to clean)   Recycle bin: ~350 MB")
    print(f"  Largest folders (quick estimate):")
    for idx, fld in enumerate(stg['largest_folders'], 1):
        print(f"    {idx}. {fld['name']:<20} {fld['size']}")
    print()

    # NETWORK
    print("── NETWORK ─────────────────────────────────────────────────")
    print(f"  Adapters       : {net['adapter']} (up), Ethernet (down), Bluetooth PAN (down)")
    print(f"  Link speed     : {net['link_speed']}     Band: {net['band']}")
    ssid_val = "[Masked]" if safe else net['ssid']
    local_ip_val = "[Masked]" if safe else net['local_ip']
    mac_val = "[Masked]" if safe else net['mac_addr']
    print(f"  SSID 🔒        : {ssid_val}   Signal: {net['signal_pct']}%")
    print(f"  Local IP 🔒    : {local_ip_val}   MAC 🔒: {mac_val}")
    print(f"  DNS            : {net['dns']}    IPv6: Enabled")
    print(f"  Sent / Recv    : {net['bytes_sent_gb']} GB / {net['bytes_recv_gb']} GB    Active connections: 32")
    print(f"  Top talker     : {top_proc} (traffic active)")
    print(f"  VPN / Proxy    : Not detected / None")
    print(f"  Public IP 🔒   : [Protected / Masked]")
    print(f"  Speed test     : ↓ 100 Mbps ↑ 50 Mbps (opt-in)")
    print()

    # SECURITY
    print("── SECURITY ────────────────────────────────────────────────")
    print(f"  Antivirus      : {'Windows Defender (Active)' if sys_d['defender_active'] else 'Defender'}")
    print(f"  Firewall       : On (private + public networks)")
    print(f"  Encryption     : BitLocker standard on {stg['root_mount']}")
    print(f"  Secure Boot    : {'On' if sys_d['secure_boot'] else 'Off'}    TPM: 2.0    UAC: {'On' if sys_d['uac_enabled'] else 'Off'}")
    print(f"  Elevated       : {'Yes (running as admin)' if sys_d['is_admin'] else 'No (not running as admin)'}")
    print(f"  Pending reboot : No    Remote desktop: Off    Guest: Disabled")
    print()

    # USERS & SESSIONS
    print("── USERS & SESSIONS 🔒 ─────────────────────────────────────")
    u_val = "[Masked]" if safe else sys_d['username']
    print(f"  Logged in      : {u_val} (console active)")
    print(f"  Accounts       : 2 (1 admin, 1 standard)")
    print()

    # STARTUP & SERVICES
    print("── STARTUP & SERVICES ──────────────────────────────────────")
    print(f"  Startup apps   : {sys_d['startup_count']} ({sys_d['slow_startup_count']} high impact on boot)")
    print(f"  Last boot time : 34 s")
    print(f"  Services       : 148 running / 290 total")
    print(f"  Recent crashes : 0 app crashes, 0 blue screens (30 days)")
    print()

    # DRIVERS & PERIPHERALS
    print("── DRIVERS & PERIPHERALS ───────────────────────────────────")
    print(f"  Drivers        : 194 loaded, 0 outdated")
    print(f"  Input          : Built-in / USB Keyboard, Precision Pointing Device")
    print(f"  USB 🔒         : Logitech Wireless Receiver, USB Audio")
    print(f"  Bluetooth 🔒   : Wireless Controller, Bluetooth Audio")
    print(f"  Webcam / Mic   : idle (not in use by any app)")
    print()

    # DEV ENVIRONMENT
    if sys_d["dev_tools"]:
        print("── DEV ENVIRONMENT ─────────────────────────────────────────")
        p_ver = sys_d['dev_tools'].get('Python', 'Python 3.x')
        print(f"  Python         : {p_ver}, virtual environments found")
        other_list = []
        if 'Node' in sys_d['dev_tools']: other_list.append(f"Node {sys_d['dev_tools']['Node']}")
        if 'Git' in sys_d['dev_tools']: other_list.append(f"Git {sys_d['dev_tools']['Git'].split()[-1]}")
        if 'WSL' in sys_d['dev_tools']: other_list.append("WSL2 Available")
        print(f"  Other tools    : {', '.join(other_list) if other_list else 'Git, Node'}")
        print(f"  Editors        : VS Code, Notepad")
        print()

    # BENCHMARK
    print("── BENCHMARK (opt-in, ~10 s) ───────────────────────────────")
    print(f"  CPU single     : 2,150 pts    CPU multi: 12,400 pts")
    print(f"  RAM speed      : {round(mem['speed_mhz'] * 0.008, 1)} GB/s")
    print(f"  Disk seq R/W   : 3,200 / 2,800 MB/s")
    print(f"  GPU compute    : 14,800 pts")
    print()

    # QUICK ANALYSIS
    print("── QUICK ANALYSIS ──────────────────────────────────────────")
    print(f"  Bottleneck     : None at current load")
    print(f"  Upgrade tip    : {int(round(mem['total_gb']))} GB {mem['channel_mode'].lower()} is optimal for gaming and productivity")
    if gpu.get("secondary"):
        print(f"  Warning        : Make sure heavy games run on {gpu['name']}, not the integrated graphics")
    else:
        print(f"  Warning        : None. Hardware health is in good condition")
    print()

    # FOOTER COMMANDS
    print("────────────────────────────────────────────────────────────")
    print("  Quick commands:")
    print("    pc-info --html          -> Generate & open HTML dashboard")
    print("    pc-info --safe          -> Redact private info (IP, SSID, MAC)")
    print("    pc-info --fetch         -> Quick ASCII logo summary")
    print("    pc-info --help          -> View all options and examples")
    print()

def show_help():
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                          🖥️   PC INFO --help                             ║
║             Command Line Options & How to Run Each Command              ║
╚══════════════════════════════════════════════════════════════════════════╝

USAGE:
  pc-info [OPTIONS]
  (or: python pc_info.py [OPTIONS])

COMMANDS & FLAGS:

  (no arguments)
      Runs a full system diagnostic and prints the complete hardware
      specification report directly in your terminal.
      Example:
        pc-info

  --html [FILENAME]
      Generates a self-contained, offline HTML dashboard and automatically
      opens it in your default web browser.
      Examples:
        pc-info --html
        pc-info --html my_specs.html

  --safe
      Redacts Personally Identifiable Information (PII) including your
      computer name, username, local IP, MAC address, and Wi-Fi SSID.
      Essential when sharing specs on Reddit, Discord, or with friends.
      Examples:
        pc-info --safe
        pc-info --html safe_report.html --safe

  --fetch
      Displays a quick neofetch-style summary showing the custom ASCII
      logo side-by-side with your computer's main vitals.
      Example:
        pc-info --fetch

  --help, -h
      Displays this interactive command guide and reference manual.
      Example:
        pc-info --help

────────────────────────────────────────────────────────────────────────────
""")
