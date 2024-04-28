import subprocess
import speedtest
import socket
from multiprocessing import Pool
from scapy.all import traceroute

def ping_test(host):
    try:
        result = subprocess.run(["ping", "-c", "4", host], capture_output=True, text=True, timeout=10)
        if "64 bytes" in result.stdout:
            return "Host is reachable"
        else:
            return "Host is unreachable"
    except subprocess.TimeoutExpired:
        return "Ping timeout"

def speed_test():
    st = speedtest.Speedtest()
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    return download_speed, upload_speed

def dns_resolution_test(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.gaierror:
        return False

def port_connectivity_test(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        sock.connect((host, port))
        return True
    except (ConnectionRefusedError, TimeoutError):
        return False
    finally:
        sock.close()

def traceroute_test(host):
    results, _ = traceroute(host)
    return results

def test_host(host):
    results = {
        "Host": host,
        "Ping Test": ping_test(host),
        "Speed Test": speed_test(),
        "DNS Resolution Test": dns_resolution_test(host),
        "Port Connectivity Test (Port 80)": port_connectivity_test(host, 80),
        "Traceroute Test": traceroute_test(host)
    }
    return results

def display_ascii_art():
    ascii_art = subprocess.run(["figlet", "NetDiagnose"], stdout=subprocess.PIPE, text=True)
    print(ascii_art.stdout)

def main():
    display_ascii_art()
    print("Welcome to NetDiagnose - Your Network Troubleshooter")
    num_hosts = int(input("Enter the number of hosts you want to troubleshoot: "))
    hosts = []

    for _ in range(num_hosts):
        host = input("Enter host or IP address: ")
        hosts.append(host)

    with Pool(processes=num_hosts) as pool:
        results = pool.map(test_host, hosts)

    for result in results:
        print("\nResults for", result["Host"])
        for test, value in result.items():
            if test == "Host":
                continue
            print(f"{test}: {value}")

if __name__ == "__main__":
    main()
