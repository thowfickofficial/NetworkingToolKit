import psutil
import platform
import subprocess

def get_system_info():
    # Get basic system information
    system_info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }

    # Get CPU information
    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "CPU Usage (%)": psutil.cpu_percent(interval=1)
    }

    # Get memory information
    memory = psutil.virtual_memory()
    memory_info = {
        "Total Memory (MB)": memory.total / (1024 ** 2),
        "Available Memory (MB)": memory.available / (1024 ** 2),
        "Used Memory (MB)": memory.used / (1024 ** 2),
        "Memory Usage (%)": memory.percent
    }

    # Get disk information
    disk = psutil.disk_usage('/')
    disk_info = {
        "Total Disk Space (GB)": disk.total / (1024 ** 3),
        "Used Disk Space (GB)": disk.used / (1024 ** 3),
        "Free Disk Space (GB)": disk.free / (1024 ** 3),
        "Disk Usage (%)": disk.percent
    }

    return {
        "System Information": system_info,
        "CPU Information": cpu_info,
        "Memory Information": memory_info,
        "Disk Information": disk_info
    }

if __name__ == "__main__":
    subprocess.run(["figlet", "SysInfoMonitor"])
    system_info = get_system_info()
    for category, info in system_info.items():
        print(f"\n{category}:")
        for key, value in info.items():
            print(f"{key}: {value}")
