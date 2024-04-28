import os
import platform
import subprocess
import speedtest
import argparse
import threading
import time
import socket
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama for colored output

def clear_screen():
    # Function to clear the console screen based on the operating system.
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def resolve_ip(hostname):
    # Function to resolve a hostname to an IP address.
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        return None

def check_latency(target, interval):
    # Function to continuously check latency to a target (IP or hostname) using ping.
    while True:
        try:
            if ":" in target:
                # IPv6 address
                result = subprocess.run(["ping", "-c", "4", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            else:
                # IPv4 address or hostname (resolved to IP)
                ip_address = resolve_ip(target)
                if ip_address is None:
                    print(Fore.RED + f"Failed to resolve hostname: {target}")
                    time.sleep(interval)
                    continue
                result = subprocess.run(["ping", "-c", "4", ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)

            if result.returncode == 0:
                lines = result.stdout.splitlines()
                avg_latency = lines[-1].split("/")[-2]
                print(f"Average Latency to {target}: {avg_latency} ms")
            else:
                print(Fore.RED + f"Ping request to {target} failed.")
        except Exception as e:
            print(Fore.RED + str(e))
        
        time.sleep(interval)

def check_bandwidth(interval):
    # Function to continuously check bandwidth using Speedtest CLI.
    while True:
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 10**6  # Convert to Mbps
            upload_speed = st.upload() / 10**6  # Convert to Mbps
            print(f"Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps")
        except Exception as e:
            print(Fore.RED + str(e))
        
        time.sleep(interval)

def display_network_info():
    # Function to display general network information.
    hostname = platform.node()
    system = platform.system()
    release = platform.release()
    ip_address = subprocess.getoutput("hostname -I").strip()
    
    print("Network Information")
    print("===================")
    print(f"Hostname: {hostname}")
    print(f"Operating System: {system} {release}")
    print(f"IP Address: {ip_address}")

def main():
    parser = argparse.ArgumentParser(description="Advanced Network Monitoring Tool")
    parser.add_argument(
        "-latency",
        metavar="TARGET",
        help="Check latency to a target IP address or hostname.",
    )
    parser.add_argument(
        "-bandwidth",
        action="store_true",
        help="Check bandwidth (download and upload speed).",
    )
    parser.add_argument(
        "-info",
        action="store_true",
        help="Display general network information.",
    )
    parser.add_argument(
        "-continuous",
        action="store_true",
        help="Enable continuous monitoring.",
    )
    parser.add_argument(
        "-interval",
        type=int,
        default=10,
        help="Interval (in seconds) for continuous monitoring. Default is 10 seconds.",
    )

    args = parser.parse_args()

    if args.info:
        display_network_info()
    elif args.latency:
        if args.continuous:
            print("Continuous Latency Monitoring (Press Ctrl+C to stop):")
            try:
                check_latency_thread = threading.Thread(target=check_latency, args=(args.latency, args.interval))
                check_latency_thread.daemon = True
                check_latency_thread.start()
                check_latency_thread.join()
            except KeyboardInterrupt:
                pass
        else:
            result = check_latency(args.latency, args.interval)
            print(result)
    elif args.bandwidth:
        if args.continuous:
            print("Continuous Bandwidth Monitoring (Press Ctrl+C to stop):")
            try:
                check_bandwidth_thread = threading.Thread(target=check_bandwidth, args=(args.interval,))
                check_bandwidth_thread.daemon = True
                check_bandwidth_thread.start()
                check_bandwidth_thread.join()
            except KeyboardInterrupt:
                pass
        else:
            result = check_bandwidth(args.interval)
            print(result)
    else:
        while True:
            clear_screen()
            print(Fore.MAGENTA + r'''        
 _       _______________________ _______ _               
( (    /(  ____ \__   __(       (  ___  ( (    /|\     /|
|  \  ( | (    \/  ) (  | () () | (   ) |  \  ( ( \   / )
|   \ | | (__      | |  | || || | |   | |   \ | |\ (_) / 
| (\ \) |  __)     | |  | |(_)| | |   | | (\ \) | ) _ (  
| | \   | (        | |  | |   | | |   | | | \   |/ ( ) \ 
| )  \  | (____/\  | |  | )   ( | (___) | )  \  ( /   \ )
|/    )_(_______/  )_(  |/     \(_______|/    )_|/     \|
                                                                                                                                                                     
            ''' + Style.RESET_ALL)
            print("Network Monitoring Tool")
            print("===============================")
            print("1. Check Latency")
            print("2. Check Bandwidth")
            print("3. Display Network Info")
            print("4. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                target = input("Enter the target IP address or hostname to check latency: ")
                if args.continuous:
                    print("Continuous Latency Monitoring (Press Ctrl+C to stop):")
                    try:
                        check_latency_thread = threading.Thread(target=check_latency, args=(target, args.interval))
                        check_latency_thread.daemon = True
                        check_latency_thread.start()
                        check_latency_thread.join()
                    except KeyboardInterrupt:
                        pass
                else:
                    result = check_latency(target, args.interval)
                    print(result)
            elif choice == "2":
                if args.continuous:
                    print("Continuous Bandwidth Monitoring (Press Ctrl+C to stop):")
                    try:
                        check_bandwidth_thread = threading.Thread(target=check_bandwidth, args=(args.interval,))
                        check_bandwidth_thread.daemon = True
                        check_bandwidth_thread.start()
                        check_bandwidth_thread.join()
                    except KeyboardInterrupt:
                        pass
                else:
                    result = check_bandwidth(args.interval)
                    print(result)
            elif choice == "3":
                display_network_info()
                input("Press Enter to continue...")
            elif choice == "4":
                break
            else:
                print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
