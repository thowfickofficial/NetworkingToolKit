import nmap
import netifaces

def get_default_gateway():
    gateways = netifaces.gateways()
    return gateways['default'][netifaces.AF_INET][0]

def find_router_ip():
    gateway_ip = get_default_gateway()
    return '.'.join(gateway_ip.split('.')[:-1] + ['1'])

def scan_router(ip_address):
    nm = nmap.PortScanner()
    nm.scan(ip_address, arguments='-A')  # Aggressive scan for detailed information
    if nm.all_hosts():
        host_info = nm[ip_address]
        if 'hostnames' in host_info:
            print("Hostname: ", host_info['hostnames'][0]['name'])
        if 'vendor' in host_info:
            print("Vendor: ", host_info['vendor'])
        if 'osmatch' in host_info:
            print("OS: ", host_info['osmatch'][0]['name'])
        print("Open ports:")
        for port, protocol in host_info['tcp'].items():
            print(f"Port {port}/{protocol['name']}: {protocol['product']} - {protocol['version']}")

    else:
        print("No information found for the specified IP address.")

if __name__ == "__main__":
    router_ip = find_router_ip()
    print("Router IP:", router_ip)
    scan_router(router_ip)
