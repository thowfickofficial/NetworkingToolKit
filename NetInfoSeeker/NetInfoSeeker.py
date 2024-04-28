import socket
import uuid
import requests
import subprocess

def get_ipv4_addresses():
    return ', '.join(socket.gethostbyname_ex(socket.gethostname())[2])

def get_ipv6_addresses():
    return ', '.join(ip[4][0] for ip in socket.getaddrinfo(socket.gethostname(), None) if ":" in ip[4][0])

def get_public_ipv4():
    try:
        response = requests.get("https://api64.ipify.org?format=json", timeout=10)
        response.raise_for_status()
        return response.json()["ip"]
    except requests.exceptions.RequestException as e:
        return str(e)

def get_public_ipv6():
    try:
        response = requests.get("https://api64.ipify.org?format=jsonv6", timeout=10)
        response.raise_for_status()
        return response.json().get("ip", "N/A")
    except (requests.exceptions.RequestException, KeyError, ValueError) as e:
        return str(e)

def get_public_ip_with_curl():
    try:
        output = subprocess.check_output(["curl", "ifconfig.me"]).decode("utf-8").strip()
        return output
    except subprocess.CalledProcessError as e:
        return str(e)

def get_mac_address():
    return ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])

if __name__ == "__main__":
    print("Network Information:")
    print("Private IPv4 Addresses:", get_ipv4_addresses())
    print("Private IPv6 Addresses:", get_ipv6_addresses())
    public_ipv4 = get_public_ipv4()
    if not public_ipv4.startswith("Error:"):
        print("Public IPv4 Address:", public_ipv4)
    else:
        print("Public IPv4 Address: Not available (API) -", public_ipv4)
        public_ipv4 = get_public_ip_with_curl()
        print("Public IPv4 Address (curl):", public_ipv4)
    public_ipv6 = get_public_ipv6()
    if not public_ipv6.startswith("Error:"):
        print("Public IPv6 Address:", public_ipv6)
    else:
        print("Public IPv6 Address: Not available -", public_ipv6)
    print("MAC Address:", get_mac_address())
