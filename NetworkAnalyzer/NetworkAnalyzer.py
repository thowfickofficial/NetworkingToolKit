
from ping3 import ping, verbose_ping
import datetime
import threading
import matplotlib.pyplot as plt
import os
import pyfiglet
import sys
import socket



# Function to run the connectivity test for a single host
def run_single_host_test(host, count=5, interval=1):
    ping_results = port_connectivity_test(host, count=count, interval=interval)

    if ping_results:
        print(f"\nPing Results for {host}:")
        for result in ping_results:
            print(result)

        average_latency = calculate_average_latency(ping_results)
        if average_latency is not None:
            print(f"Average Latency: {average_latency:.2f} ms")
        
        return ping_results
    else:
        print(f"Failed to ping {host}")
        return None

# Function to run continuous connectivity tests for multiple hosts
def run_continuous_connectivity_tests(hosts, count=5, interval=1, alert_threshold=None, run_duration=None):
    start_time = datetime.datetime.now()
    ping_data = {host: [] for host in hosts}  # Store ping results for each host

    while True:
        current_time = datetime.datetime.now()
        elapsed_time = current_time - start_time

        if run_duration and elapsed_time.total_seconds() >= run_duration:
            break  # Exit if the specified run duration has elapsed

        for host in hosts:
            ping_results = run_single_host_test(host, count=count, interval=interval)
            
            if ping_results:
                ping_data[host].extend(ping_results)

                if alert_threshold is not None:
                    average_latency = calculate_average_latency(ping_results)
                    if average_latency is not None and average_latency > alert_threshold:
                        print(f"ALERT: Latency exceeded {alert_threshold} ms for {host}!")

    return ping_data

# Function to plot real-time ping results for a single host
def plot_real_time_ping_results(host, ping_data):
    timestamps, latencies = zip(*ping_data)
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, latencies, label='Latency (ms)')
    plt.xlabel('Time')
    plt.ylabel('Latency (ms)')
    plt.title(f'Real-Time Ping Results for {host}')
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to plot historical ping data for a single host
def plot_historical_ping_data(host, ping_data):
    timestamps, latencies = zip(*ping_data)
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, latencies, label='Average Latency (ms)')
    plt.xlabel('Timestamp')
    plt.ylabel('Average Latency (ms)')
    plt.title(f'Historical Ping Data for {host}')
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to calculate and display performance metrics for a single host
def display_performance_metrics(host, ping_data):
    latencies = [result[1] for result in ping_data if result[1] is not None]

    if latencies:
        min_latency = min(latencies)
        max_latency = max(latencies)
        average_latency = sum(latencies) / len(latencies)

        print(f"Performance Metrics for {host}:")
        print(f"Minimum Latency: {min_latency:.2f} ms")
        print(f"Maximum Latency: {max_latency:.2f} ms")
        print(f"Average Latency: {average_latency:.2f} ms")
    else:
        print(f"No data available for {host}")

# Function to save ping data to a file
def save_ping_data_to_file(file_path, ping_data):
    with open(file_path, 'w') as file:
        for host, data in ping_data.items():
            file.write(f"{host}:\n")
            for result in data:
                file.write(f"{result}\n")
            file.write("\n")

# Function to load ping data from a file
def load_ping_data_from_file(file_path):
    ping_data = {}
    current_host = None

    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()

            if line.endswith(":"):
                current_host = line[:-1]
                ping_data[current_host] = []
            else:
                if current_host is not None:
                    ping_data[current_host].append(line)

    return ping_data

# Function to calculate the average latency from a list of ping results
def calculate_average_latency(ping_results):
    if not ping_results:
        return None

    total_latency = sum(latency for _, latency in ping_results if latency is not None)
    num_valid_samples = sum(1 for _, latency in ping_results if latency is not None)

    if num_valid_samples == 0:
        return None

    return total_latency / num_valid_samples


def port_connectivity_test(host, port, timeout=1):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as e:
        return False
    

# Main function
def main():
    print(pyfiglet.figlet_format("NetworkAnalyzer", font="slant"))

    while True:
        print("Automated Network Testing")
        print("")
        print("\nMenu:")
        print("1. Run Connectivity Test for Single Host")
        print("2. Run Continuous Connectivity Tests for Multiple Hosts")
        print("3. Plot Real-Time Ping Results")
        print("4. Plot Historical Ping Data")
        print("5. Display Performance Metrics")
        print("6. Save Ping Data to File")
        print("7. Load Ping Data from File")
        print("8. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6/7/8): ")

        if choice == '1':
            host = input("Enter the host to ping (e.g., example.com): ")
            run_single_host_test(host)
        
        elif choice == '2':
            hosts = input("Enter multiple hosts to ping (comma-separated): ").split(',')
            hosts = [host.strip() for host in hosts]
            
            try:
                count = int(input("Enter the number of pings to send (default is 5): "))
            except ValueError:
                count = 5

            try:
                interval = float(input("Enter the ping interval in seconds (default is 1 second): "))
            except ValueError:
                interval = 1.0

            try:
                alert_threshold = float(input("Enter the alert threshold for latency (ms, leave empty for no alerts): "))
            except ValueError:
                alert_threshold = None

            try:
                run_duration = float(input("Enter the duration of the test in seconds (leave empty for continuous testing): "))
            except ValueError:
                run_duration = None

            ping_data = run_continuous_connectivity_tests(hosts, count, interval, alert_threshold, run_duration)
        
        elif choice == '3':
            if "ping_data" in globals():
                host_to_plot = input("Enter the host for which you want to plot real-time ping results: ")
                if host_to_plot in ping_data:
                    plot_real_time_ping_results(host_to_plot, ping_data[host_to_plot])
                else:
                    print(f"No data available for {host_to_plot}")
            else:
                print("No real-time ping data available.")

        elif choice == '4':
            if "ping_data" in globals():
                host_to_plot = input("Enter the host for which you want to plot historical ping data: ")
                if host_to_plot in ping_data:
                    plot_historical_ping_data(host_to_plot, ping_data[host_to_plot])
                else:
                    print(f"No data available for {host_to_plot}")
            else:
                print("No historical ping data available.")

        elif choice == '5':
            if "ping_data" in globals():
                host_to_analyze = input("Enter the host for which you want to display performance metrics: ")
                if host_to_analyze in ping_data:
                    display_performance_metrics(host_to_analyze, ping_data[host_to_analyze])
                else:
                    print(f"No data available for {host_to_analyze}")
            else:
                print("No ping data available for analysis.")
        
        elif choice == '6':
            if "ping_data" in globals():
                file_name = input("Enter the name of the file to save ping data: ")
                save_ping_data_to_file(file_name, ping_data)
                print(f"Ping data saved to {file_name}")
            else:
                print("No ping data available to save.")

        elif choice == '7':
            file_name = input("Enter the name of the file to load ping data: ")
            if os.path.exists(file_name):
                ping_data = load_ping_data_from_file(file_name)
                print(f"Ping data loaded from {file_name}")
            else:
                print(f"No file found: {file_name}")

        elif choice == '8':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please select a valid option (1/2/3/4/5/6/7/8).")

if __name__ == "__main__":
    main()
