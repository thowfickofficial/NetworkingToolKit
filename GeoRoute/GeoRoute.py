import sys
import socket
import struct
import time
import argparse
import random
import requests
import folium
from scapy.all import *
from scapy.layers.inet import IP, ICMP

import pyfiglet

# Display the tool name using PyFiglet
def display_tool_name():
    ascii_art = pyfiglet.figlet_format("GeoRoute", font="slant")
    print(ascii_art)

def get_location_info(ip_address):
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}/json")
        data = response.json()
        return data.get("city", "Unknown"), data.get("region", "Unknown"), data.get("country", "Unknown")
    except Exception as e:
        return "Unknown", "Unknown", "Unknown"

def send_icmp_request(dest_addr, ttl, timeout):
    icmp_id = random.randint(1, 65535)
    icmp_seq = random.randint(1, 65535)
    packet = IP(dst=dest_addr, ttl=ttl) / ICMP(id=icmp_id, seq=icmp_seq)

    send_time = time.time()
    reply = sr1(packet, timeout=timeout, verbose=False)

    if reply:
        recv_time = time.time()
        return reply.src, recv_time - send_time
    else:
        return None, None

def traceroute(dest_host, max_hops=30, timeout=2, show_map=False):
    dest_addr = socket.gethostbyname(dest_host)
    hop_data = []

    print(f"Traceroute to {dest_host} ({dest_addr}), max {max_hops} hops:")

    m = folium.Map(location=[0, 0], zoom_start=2)
    popup_html = folium.Html("Start", script=True)
    popup = folium.Popup(popup_html, max_width=200)
    icon = folium.CustomIcon(icon_image="https://i.imgur.com/baAsOCL.png", icon_size=(32, 32))

    for ttl in range(1, max_hops + 1):
        addr, response_time = send_icmp_request(dest_addr, ttl, timeout)

        if addr:
            try:
                city, region, country = get_location_info(addr)
            except Exception as e:
                city, region, country = "Unknown", "Unknown", "Unknown"

            hop_data.append((addr, city, region, country))

            try:
                host = socket.gethostbyaddr(addr)
                host_name = f" ({host[0]})"
            except socket.herror:
                host_name = ""

            print(f"{ttl}\t{addr}{host_name}\t{response_time * 1000:.3f} ms")

            if show_map:
                location_info = f"City: {city}, Region: {region}, Country: {country}"
                popup_html = folium.Html(f"{ttl}: {addr}{host_name}<br>{location_info}", script=True)
                popup = folium.Popup(popup_html, max_width=200)
                folium.Marker(location=[city, region], popup=popup, icon=icon).add_to(m)

            if addr == dest_addr:
                break
        else:
            print(f"{ttl}\t*\tTimeout")

    if show_map:
        m.save("traceroute_map.html")
        print("Route map saved as 'traceroute_map.html'")

def main():
    display_tool_name()  # Display the tool name when the program starts
    dest_host = input("Enter the destination host or IP address: ")
    max_hops = int(input("Enter the maximum number of hops (default is 30): ") or 30)
    timeout = int(input("Enter the timeout for each hop in seconds (default is 2): ") or 2)
    show_map = input("Display a route map? (yes/no): ").lower() == "yes"

    try:
        traceroute(dest_host, max_hops, timeout, show_map)
    except KeyboardInterrupt:
        print("\nTraceroute stopped by the user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
