import time
import psutil
import threading
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
import pyfiglet

def bytes_to_megabytes(bytes):
    return bytes / (1024 * 1024)

class NetworkBandwidthMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Bandwidth Monitor")
        self.root.geometry("800x400")

        # Display the name "NetBandwidthMonApp" in ASCII art
        ascii_name = pyfiglet.figlet_format("NetBandwidthMonApp")
        print(ascii_name)

        self.interface_label = ttk.Label(root, text="Select Network Interface:")
        self.interface_label.pack()

        self.interfaces = psutil.net_io_counters(pernic=True).keys()
        self.interface_var = tk.StringVar(root)
        self.interface_var.set(list(self.interfaces)[0])

        self.interface_menu = ttk.OptionMenu(root, self.interface_var, *self.interfaces)
        self.interface_menu.pack()

        self.duration_label = ttk.Label(root, text="Duration (seconds):")
        self.duration_label.pack()

        self.duration_var = tk.IntVar(root)
        self.duration_var.set(60)

        self.duration_entry = ttk.Entry(root, textvariable=self.duration_var)
        self.duration_entry.pack()

        self.start_button = ttk.Button(root, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack()

        self.stop_button = ttk.Button(root, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack()

        self.plot_frame = ttk.Frame(root)
        self.plot_frame.pack()

        self.running = False

    def monitor_network_bandwidth(self):
        interface = self.interface_var.get()
        duration = self.duration_var.get()
        interval = 1

        start_time = time.time()
        end_time = start_time + duration

        timestamps = []
        received_data = []
        sent_data = []

        while self.running and time.time() < end_time:
            stats = psutil.net_io_counters(pernic=True).get(interface)

            if stats is not None:
                received_mb = bytes_to_megabytes(stats.bytes_recv)
                sent_mb = bytes_to_megabytes(stats.bytes_sent)
                elapsed_time = round(time.time() - start_time, 2)

                timestamps.append(elapsed_time)
                received_data.append(received_mb)
                sent_data.append(sent_mb)

                self.update_plot(timestamps, received_data, sent_data)

            time.sleep(interval)

    def update_plot(self, timestamps, received_data, sent_data):
        plt.clf()
        plt.plot(timestamps, received_data, label="Received (MB)")
        plt.plot(timestamps, sent_data, label="Sent (MB)")
        plt.xlabel("Time (seconds)")
        plt.ylabel("Data (MB)")
        plt.title(f"Network Bandwidth Monitor ({self.interface_var.get()})")
        plt.legend()
        plt.grid(True)
        plt.pause(0.1)

    def start_monitoring(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        threading.Thread(target=self.monitor_network_bandwidth).start()

    def stop_monitoring(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = NetworkBandwidthMonitor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
