import socket
import threading
import nmap
import subprocess

# Define a range of common ports to scan
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389]

def scan_host(host, port, detect_service_version=False, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                    if detect_service_version:
                        banner = sock.recv(1024).decode('utf-8').strip()
                        print(f"[+] {host}:{port} is open ({service}) - Banner: {banner}")
                    else:
                        print(f"[+] {host}:{port} is open ({service})")
                except OSError:
                    service = "Unknown"
                    print(f"[+] {host}:{port} is open (Service: {service})")

    except (socket.timeout, ConnectionRefusedError):
        pass
    except Exception as e:
        print(f"[-] Error scanning {host}:{port}: {str(e)}")

def detect_os(host):
    try:
        nm = nmap.PortScanner()
        nm.scan(host, arguments='-O')
        os_info = nm[host]['osclass'][0]['osfamily']
        return os_info

    except Exception as e:
        return "Unknown"

def scan_ports(target, start_port, end_port, detect_service_version=False, timeout=1):
    open_ports = []

    for port in range(start_port, end_port + 1):
        scan_host(target, port, detect_service_version, timeout)
        os_info = detect_os(target)
        open_ports.append((target, os_info))

    return open_ports

def save_results_to_file(results, filename):
    with open(filename, 'w') as file:
        for host, os_info in results:
            file.write(f"{host} (OS: {os_info})\n")

def main():
    subprocess.run(["figlet", "NetProbe"])  # Display the tool name in ASCII art
    print("Mini Network Scanner")

    target = input("Enter the IP address or domain name of the target: ")
    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))
    detect_service_version = input("Detect service versions (y/n): ").strip().lower() == 'y'
    timeout = int(input("Enter the timeout (seconds) for port scan (default 1): ") or 1)
    output_filename = input("Enter the output filename (e.g., scan_results.txt): ")

    try:
        print(f"Scanning ports {start_port} to {end_port} on target {target}")
        open_ports = scan_ports(target, start_port, end_port, detect_service_version, timeout)
        save_results_to_file(open_ports, output_filename)
        print("Scan complete. Results saved to", output_filename)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
