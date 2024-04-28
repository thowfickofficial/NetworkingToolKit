import pywifi
import re
import subprocess
import time
from tabulate import tabulate  # For formatting tables

# ANSI escape codes for colored output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Signal strength indicator thresholds
SIGNAL_STRONG = -50
SIGNAL_MEDIUM = -70

# List to store network profiles
network_profiles = []

def scan_wifi_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Assuming the first wireless interface is your Wi-Fi interface

    iface.scan()
    scan_results = iface.scan_results()

    return scan_results

def get_signal_quality(signal_strength):
    if signal_strength >= SIGNAL_STRONG:
        return GREEN + "Strong" + RESET
    elif signal_strength >= SIGNAL_MEDIUM:
        return YELLOW + "Medium" + RESET
    else:
        return RED + "Weak" + RESET

def get_channel(bssid):
    try:
        iwlist_scan = subprocess.check_output(['iwlist', 'wlan0', 'channel'], universal_newlines=True)
        channel_match = re.search(r'Channel (\d+)', iwlist_scan)
        if channel_match:
            return int(channel_match.group(1))
        else:
            return "Unknown"
    except subprocess.CalledProcessError:
        return "Unknown"

def get_wifi_security_type(network):
    # Mapping of encryption type integers to their names
    encryption_types = {
        0: "Open",
        1: "WEP",
        2: "WPA-PSK",
        3: "WPA2-PSK",
        4: "WPA-Enterprise",
        5: "WPA2-Enterprise",
    }
    
    # Check if 'akm' is not empty before accessing its first element
    if network.akm:
        security_type = encryption_types.get(network.akm[0], "Unknown")
    else:
        security_type = "Open"  # Default to "Open" if encryption type is not available
    
    return security_type

def display_ssid(ssid):
    if ssid:
        return ssid
    else:
        return "Hidden SSID"

def print_network_info(network):
    ssid = display_ssid(network.ssid)
    signal_strength = network.signal
    security_type = get_wifi_security_type(network)
    bssid = network.bssid
    channel = get_channel(bssid)

    signal_quality = get_signal_quality(signal_strength)
    
    network_details = {
        "SSID": ssid,
        "BSSID": bssid,
        "Signal Strength (dBm)": signal_strength,
        "Signal Quality": signal_quality,
        "Channel": channel,
        "Security Type": security_type,
    }

    print(tabulate([network_details], headers="keys", tablefmt="grid"))
    print(f"{YELLOW}{'-' * 30}{RESET}")

def sort_and_filter_networks(networks, sort_by="signal_strength"):
    if sort_by == "signal_strength":
        networks.sort(key=lambda x: x.signal, reverse=True)
    elif sort_by == "security_type":
        networks.sort(key=lambda x: x.akm[0])
    elif sort_by == "ssid":
        networks.sort(key=lambda x: display_ssid(x.ssid))
    # Add more sorting criteria as needed

def connect_to_network(network, password=None):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    
    profile = pywifi.Profile()
    profile.ssid = network.ssid
    profile.auth = network.akm[0]
    profile.akm.append(network.akm[0])
    
    if password:
        profile.key = password
    
    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)
    iface.connect(tmp_profile)
    time.sleep(5)  # Wait for connection to establish
    
    if iface.status() == pywifi.const.IFACE_CONNECTED:
        print(f"{GREEN}Connected to '{display_ssid(network.ssid)}'!{RESET}")
        network_profiles.append(profile)
    else:
        print(f"{RED}Connection to '{display_ssid(network.ssid)}' failed.{RESET}")

def save_profiles():
    with open("wifi_profiles.txt", "w") as f:
        for profile in network_profiles:
            f.write(f"SSID: {profile.ssid}\n")
            f.write(f"Authentication Type: {profile.auth}\n")
            f.write(f"Key: {profile.key}\n")
            f.write("-" * 30 + "\n")

def load_profiles():
    try:
        with open("wifi_profiles.txt", "r") as f:
            lines = f.read().split("\n")
        
        profile_info = {}
        current_ssid = None
        
        for line in lines:
            if line.startswith("SSID: "):
                current_ssid = line.replace("SSID: ", "")
                profile_info[current_ssid] = {"SSID": current_ssid}
            elif line.startswith("Authentication Type: "):
                profile_info[current_ssid]["Authentication Type"] = line.replace("Authentication Type: ", "")
            elif line.startswith("Key: "):
                profile_info[current_ssid]["Key"] = line.replace("Key: ", "")
        
        return profile_info
    except FileNotFoundError:
        return {}

def main():
    try:
        wifi_scan_results = scan_wifi_networks()
        
        print(f"{GREEN}Scanning for nearby WiFi networks...{RESET}")
        print("")

        # Sort and filter networks based on user input
        sort_criteria = input(f"{CYAN}Sort by (signal_strength/security_type/ssid): {RESET}").strip()
        sort_and_filter_networks(wifi_scan_results, sort_criteria)

        for network in wifi_scan_results:
            print_network_info(network)

        while True:
            connect_option = input(f"{CYAN}Enter the SSID to connect (or 'q' to quit): {RESET}").strip()
            
            if connect_option.lower() == 'q':
                save_profiles()
                print(f"{CYAN}Thanks for using this tool!{RESET}")
                break
            
            selected_network = next((net for net in wifi_scan_results if display_ssid(net.ssid) == connect_option), None)
            if selected_network:
                password = input(f"{CYAN}Enter the network password for '{connect_option}' (if required): {RESET}").strip()
                connect_to_network(selected_network, password)
            else:
                print(f"{RED}Invalid SSID. Please try again.{RESET}")
    
    except KeyboardInterrupt:
        save_profiles()
        print(f"{CYAN}\nThanks for using this tool!{RESET}")

if __name__ == "__main__":
    main()
