import socket
import ipaddress

def scan_ports(target, ports, service_detection=False, scan_udp=False):
    open_ports = []
    
    for port in ports:
        try:
            if scan_udp:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            
            if result == 0:
                open_ports.append(port)
                if service_detection:
                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = "Unknown"
                    print(f"Port {port} is open - Service: {service}")
                else:
                    print(f"Port {port} is open")
            sock.close()
        except KeyboardInterrupt:
            print("Scanning interrupted by user.")
            break
        except Exception as e:
            print(f"Error scanning port {port}: {e}")
    
    return open_ports

def scan_ip_range(ip_range, ports, service_detection=False, scan_udp=False):
    open_ports = {}
    
    for ip in ipaddress.IPv4Network(ip_range, strict=False):
        ip_str = str(ip)
        open_ports[ip_str] = scan_ports(ip_str, ports, service_detection, scan_udp)
    
    return open_ports

def main():
    print("Welcome to the Port Scanner!")
    print("This tool allows you to scan for open ports on a target system or network.")
    
    target_type = input("Enter target type (single IP or IP range): ").strip().lower()
    
    if target_type == 'single':
        target = input("Enter the target IP address or hostname: ")
        port_range = input("Enter the port range to scan (e.g., 80-100): ").split('-')
        
        if len(port_range) != 2:
            print("Invalid port range. Please specify a range as 'start-end'.")
            return
        
        start_port = int(port_range[0])
        end_port = int(port_range[1])
        
        ports_to_scan = range(start_port, end_port + 1)
        
        service_detection = input("Do you want to perform service version detection? (yes/no): ").strip().lower() == 'yes'
        scan_udp = input("Do you want to scan UDP ports as well? (yes/no): ").strip().lower() == 'yes'
        
        print(f"Scanning target: {target}")
        open_ports = scan_ports(target, ports_to_scan, service_detection, scan_udp)
        
        if not open_ports:
            print("No open ports found.")
    
    elif target_type == 'range':
        ip_range = input("Enter the IP range to scan (e.g., 192.168.1.1/24): ")
        port_range = input("Enter the port range to scan (e.g., 80-100): ").split('-')
        
        if len(port_range) != 2:
            print("Invalid port range. Please specify a range as 'start-end'.")
            return
        
        start_port = int(port_range[0])
        end_port = int(port_range[1])
        
        ports_to_scan = range(start_port, end_port + 1)
        
        service_detection = input("Do you want to perform service version detection? (yes/no): ").strip().lower() == 'yes'
        scan_udp = input("Do you want to scan UDP ports as well? (yes/no): ").strip().lower() == 'yes'
        
        print(f"Scanning IP range: {ip_range}")
        open_ports = scan_ip_range(ip_range, ports_to_scan, service_detection, scan_udp)
        
        print("Open ports:")
        for ip, ports in open_ports.items():
            if ports:
                print(f"IP Address: {ip}")
                for port in ports:
                    print(f"  Port {port} is open")
            else:
                print(f"No open ports found for IP Address: {ip}")
    
    else:
        print("Invalid target type. Please enter 'single' or 'range'.")

if __name__ == "__main__":
    main()
