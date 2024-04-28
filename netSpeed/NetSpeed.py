import speedtest
import time
import subprocess

def display_speed(download_speed, upload_speed):
    print(f"Download Speed: {download_speed / 1_000_000:.2f} Mbps")
    print(f"Upload Speed: {upload_speed / 1_000_000:.2f} Mbps")
    print("-" * 40)

def main():
    print("Internet Speed Test - Live Data")
    print("-" * 40)

    while True:
        try:
            st = speedtest.Speedtest()
            
            # Replace '1234' with the ID of a specific server you want to use
            st.get_best_server(server_list=["1234"])

            download_speed = st.download()
            upload_speed = st.upload()
            display_speed(download_speed, upload_speed)

        except Exception as e:
            print(f"Error: {e}")

        time.sleep(5)  # Wait for 5 seconds before measuring again

if __name__ == "__main__":
    # Display the tool name in figlet style
    subprocess.run(["figlet", "NetSpeed"])
    main()

