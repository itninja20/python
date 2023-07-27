#!/usr/bin/env python3


import subprocess
import psutil


def update_os():
    """Update the Raspberry Pi OS and firmware."""
    subprocess.run("sudo apt update && sudo apt upgrade -y", shell=True)


def enable_zram():
    """Enable ZRAM (Compressed Swap)."""
    subprocess.run("sudo apt install -y zram-config", shell=True)


def disable_unnecessary_services():
    """Disable unnecessary services."""
    services_to_disable = [
        "bluetooth",
        "ntp",
        "avahi-daemon",
        "triggerhappy",
        "xserver",
        # Add other services you don't need here.
    ]
    for service in services_to_disable:
        subprocess.run(f"sudo systemctl stop {service}", shell=True)
        subprocess.run(f"sudo systemctl disable {service}", shell=True)


def overclock():
    """Overclock the Raspberry Pi (with caution)."""
    subprocess.run("sudo raspi-config nonint do_overclock", shell=True)


def optimize_gpu_memory():
    """Optimize GPU memory allocation."""
    subprocess.run("sudo raspi-config nonint do_memory_split 16", shell=True)


def monitor_resources():
    """Monitor CPU, memory, and disk usage."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage("/")
    print(f"CPU Usage: {cpu_percent}%")
    print(f"Memory Usage: {memory_info.percent}%")
    print(f"Disk Usage: {disk_info.percent}%")

if __name__ == "__main__":
    update_os()
    enable_zram()
    disable_unnecessary_services()
    overclock()
    optimize_gpu_memory()
    monitor_resources()
