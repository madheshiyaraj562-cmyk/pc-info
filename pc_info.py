#!/usr/bin/env python3
import argparse
import sys

# Ensure UTF-8 output on Windows consoles to prevent charmap encoding errors
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from collectors.cpu import get_cpu_info
from collectors.memory import get_memory_info
from collectors.gpu import get_gpu_info
from collectors.storage import get_storage_info
from collectors.network import get_network_info
from collectors.system import get_system_info
from health import calculate_health
from renderers.terminal import render_terminal_report, render_fetch, show_help
from renderers.html_renderer import render_html_report

def gather_all_data(safe_mode=False):
    print("Scanning system components...", file=sys.stderr, end="\r")
    
    cpu_data = get_cpu_info()
    mem_data = get_memory_info()
    gpu_data = get_gpu_info()
    stg_data = get_storage_info()
    net_data = get_network_info()
    sys_data = get_system_info()
    
    health_data = calculate_health(cpu_data, mem_data, gpu_data, stg_data, sys_data)

    print("                               ", file=sys.stderr, end="\r")

    return {
        "safe_mode": safe_mode,
        "cpu": cpu_data,
        "memory": mem_data,
        "gpu": gpu_data,
        "storage": stg_data,
        "network": net_data,
        "system": sys_data,
        "health": health_data
    }

def main():
    # Check for manual help invocation before argparse
    if any(arg in sys.argv for arg in ["--help", "-h", "help"]):
        show_help()
        return

    parser = argparse.ArgumentParser(
        description="pc-info: Hardware profiler & safe shareable HTML dashboard generator.",
        add_help=False
    )
    parser.add_argument(
        "--help", "-h", action="store_true",
        help="Show detailed help guide with examples."
    )
    parser.add_argument(
        "--fetch", action="store_true",
        help="Display short summary with ASCII logo (neofetch style)."
    )
    parser.add_argument(
        "--html", nargs="?", const="report.html", default=None,
        help="Generate a self-contained HTML dashboard (default: report.html)."
    )
    parser.add_argument(
        "--open", action="store_true",
        help="Automatically open the generated HTML dashboard in your default browser."
    )
    parser.add_argument(
        "--safe", action="store_true",
        help="Redact personal information (SSID, IP, MAC, usernames, hostnames)."
    )

    args = parser.parse_args()

    # 1. Custom Help
    if args.help:
        show_help()
        return

    # Collect data once for reports
    data = gather_all_data(safe_mode=args.safe)

    # 2. HTML report
    if args.html:
        filename = args.html
        auto_open = args.open or True
        saved_path = render_html_report(data, output_path=filename, auto_open=auto_open)
        print(f"✨ HTML dashboard generated: {saved_path}")
        if auto_open:
            print("Opening in default browser.....")
        return

    # 3. Terminal Fetch
    if args.fetch:
        render_fetch(data)
        return

    # 4. Default: Full Terminal Report
    render_terminal_report(data)
    
    # Clean quit prompt if running interactively
    if sys.stdin.isatty():
        try:
            print("  Press 'q' or Enter to quit... ", end="", flush=True)
            if sys.platform == "win32":
                import msvcrt
                ch = msvcrt.getch()
            else:
                input()
            print()
        except (KeyboardInterrupt, EOFError):
            print()

if __name__ == "__main__":
    main()
