import paramiko
import os
from datetime import datetime

# Define the network devices and their SSH credentials
devices = [
    {
        "hostname": "device1.example.com",
        "port": 22,
        "username": "your_username",
        "password": "your_password",
    },
    # Add more devices as needed
]

# Define the directory where configuration changes will be logged
log_directory = "config_logs"

# Create the log directory if it doesn't exist
if not os.path.exists(log_directory):
    os.mkdir(log_directory)

# Function to connect to a device and retrieve its configuration
def get_device_config(device):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            device["hostname"],
            port=device["port"],
            username=device["username"],
            password=device["password"],
            timeout=10,
        )
        
        # Modify the command based on the type of device and how configurations are stored
        stdin, stdout, stderr = ssh.exec_command("show running-config")

        config = stdout.read().decode("utf-8")
        
        ssh.close()
        return config

    except Exception as e:
        print(f"Error connecting to {device['hostname']}: {str(e)}")
        return None

# Function to log the configuration changes
def log_config_change(device, old_config, new_config):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_filename = f"{log_directory}/{device['hostname']}_{timestamp}.txt"
    
    with open(log_filename, "w") as log_file:
        log_file.write(f"Change Timestamp: {timestamp}\n")
        log_file.write(f"Device: {device['hostname']}\n\n")
        log_file.write("Old Configuration:\n")
        log_file.write(old_config)
        log_file.write("\nNew Configuration:\n")
        log_file.write(new_config)

# Main function to track configuration changes
def track_config_changes():
    for device in devices:
        old_config = get_device_config(device)
        if old_config is None:
            continue
        
        # Simulate a configuration change (for testing purposes)
        # In a real scenario, you should periodically call get_device_config and compare the configurations
        # to detect changes.
        new_config = old_config + "\n! This is a simulated change.\n"
        
        log_config_change(device, old_config, new_config)

if __name__ == "__main__":
    track_config_changes()
