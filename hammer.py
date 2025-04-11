import os
import socket
import subprocess
import json
import requests
from ctypes import *
import time

###
#
NRM  = "\x1B[0m"
RED  = "\x1B[31m"
GRN  = "\x1B[32m"
YEL  = "\x1B[33m"
BLU  = "\x1B[34m"
MAG  = "\x1B[35m"
CYN  = "\x1B[36m"
WHT  = "\x1B[37m"
#
###

# 加载banner
try:
    with open("banner.txt", "r") as file:
        banner_content = file.read()
    print("\033[94m" + banner_content + "\033[0m")  # 蓝色输出
    print("\033[91m        Let the AI break through your damn system.\033[0m")
    print("")
    print("\033[92m   SHARK Security - Advance Pentest Copyright © 2025\033[0m")
    print("\033[97m     James Taylor \033[92m<\033[96mhttps://\033[93mt.me/sharksecurityofficial\033[92m>\033[0m")
    print("")
except FileNotFoundError:
    print("Error: banner.txt not found.")
    exit(1)

# 全局变量
host = ""
domain = 0
ip = ""
host_ports = []
scan_services = []
web_tech = {}
isp = ""
asn = ""
device_type = ""
workmode = "passive"
workmodelist = ("passive", "low", "high", "intrusive")
has_sec_system = 0

def scan_passive(ip):
    ports = []
    services = []
    try:
        stdoutdata = subprocess.getoutput(f"nmap -T4 {ip} -v")
        lines = stdoutdata.splitlines()
        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                port_info = parts[0].split("/")
                try:
                    ports.append(int(port_info[0]))
                    services.append(parts[1])
                except:
                    pass
        return ports, services
    except Exception as e:
        print(f"[ \x1B[1m\x1B[31mERROR\x1B[0m ] {e}")
        return [], []

def scan_low(ip):
    ports = []
    services = []
    device_type = ""
    try:
        stdoutdata = subprocess.getoutput(f"nmap -sT {ip} --open")
        lines = stdoutdata.splitlines()
        for line in lines:
            if "open" in line:
                parts = line.split()
                if len(parts) >= 2:
                    port_info = parts[0].split("/")
                    try:
                        ports.append(int(port_info[0]))
                        services.append(parts[1])
                    except:
                        pass
            if "Device type:" in line:
                device_type = line.split("Device type:")[1].strip().split()[0]
        return ports, device_type, services
    except Exception as e:
        print(f"[ \x1B[1m\x1B[31mERROR\x1B[0m ] {e}")
        return [], "", []

def scan_high(ip):
    ports = []
    services = []
    device_type = ""
    try:
        stdoutdata = subprocess.getoutput(f"nmap -sT -sV --top-ports 10000 {ip} --open")
        lines = stdoutdata.splitlines()
        for line in lines:
            if "open" in line:
                parts = line.split()
                if len(parts) >= 2:
                    port_info = parts[0].split("/")
                    try:
                        ports.append(int(port_info[0]))
                        services.append(parts[1])
                    except:
                        pass
            if "Device type:" in line:
                device_type = line.split("Device type:")[1].strip().split()[0]
        return ports, device_type, services
    except Exception as e:
        print(f"[ \x1B[1m\x1B[31mERROR\x1B[0m ] {e}")
        return [], "", []

def scan_intrusive(ip):
    ports = []
    services = []
    device_type = ""
    try:
        stdoutdata = subprocess.getoutput(f"nmap -Pn -sT -sV -p- {ip} --open")
        lines = stdoutdata.splitlines()
        for line in lines:
            if "open" in line:
                parts = line.split()
                if len(parts) >= 2:
                    port_info = parts[0].split("/")
                    try:
                        ports.append(int(port_info[0]))
                        services.append(parts[1])
                    except:
                        pass
            if "Device type:" in line:
                device_type = line.split("Device type:")[1].strip().split()[0]
        return ports, device_type, services
    except Exception as e:
        print(f"[ \x1B[1m\x1B[31mERROR\x1B[0m ] {e}")
        return [], "", []

def show(show_full):
    print("\n=========================\x1B[1m\x1B[31mSTART\x1B[0m=========================")
    print(f"\nWorkmode: {RED}{workmode}{NRM}")
    print(f"Host: {RED}{host}{NRM}")

    if domain:
        print(f"Domain IP Address: {RED}{ip}{NRM}")

    if asn:
        print(f"ASN: {RED}{asn}{NRM}")

    if isp:
        if any(s in isp.lower() for s in ["sucuri", "akamai", "incapsula", "cloudfront", "stackpath", "fastly", "cloudflare"]):
            print(f"ISP: {RED}{isp}{NRM} {WHT}[{NRM}{YEL} Security system {NRM}{WHT}]")
        else:
            print(f"ISP: {RED}{isp}{NRM}")

    if host_ports:
        print(f"Ports: {RED}{host_ports}{NRM}")

    if device_type:
        print(f"Possible device type: {RED}{device_type}{NRM}")

    if host_ports:
        print(f"Products: {WHT}[{NRM}")
        for port, service in zip(host_ports, scan_services):
            print(f"     {RED}{port}{NRM} == {YEL}{service}{NRM}")
        print(f"{WHT}]{NRM}")

        if show_full:
            for port, service in zip(host_ports, scan_services):
                print(f"\nPort {RED}{port}{NRM} has service: {YEL}{service}{NRM}")

    print("\n==========================\x1B[1m\x1B[31mEND\x1B[0m==========================")

def get_info(ip):
    try:
        print("\n[ \x1B[1m+\x1B[0m ] Running information module")
        print("\n\t[ \x1B[1minfo\x1B[0m ] Starting passive information")
        headers = {
            'User-Agent': 'HAMMER 1.0'
        }
        
        # 定义多个 API URL
        api_urls = [
            f"http://ip-api.com/json/{ip}",
            f"https://api.ip.sb/geoip/{ip}",
            f"http://ip-api.org/json/{ip}"
        ]
        
        final_data = {}
        for url in api_urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    try:
                        data = json.loads(response.text)
                        if isinstance(data, dict):
                            final_data.update(data)
                    except json.JSONDecodeError:
                        print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] Failed to decode JSON from {url}")
                else:
                    print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] Failed to retrieve data from {url} (Status code: {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] {e}")
                print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] The link may be invalid or there is a network issue. Please check the URL and try again.")
                continue
        
        if not final_data:
            return {"error": "Failed to retrieve data from all APIs"}
        
        # 提取关键信息
        isp = final_data.get("isp", "")
        asn = final_data.get("asn", "")
        country = final_data.get("country", "")
        city = final_data.get("city", "")
        region = final_data.get("region", "")
        org = final_data.get("org", "")
        timezone = final_data.get("timezone", "")
        latitude = final_data.get("lat", "")
        longitude = final_data.get("lon", "")
        
        # 打印收集到的信息
        print(f"\n[ \x1B[1minfo\x1B[0m ] ISP: {RED}{isp}{NRM}")
        print(f"[ \x1B[1minfo\x1B[0m ] ASN: {RED}{asn}{NRM}")
        print(f"[ \x1B[1minfo\x1B[0m ] Country: {RED}{country}{NRM}")
        print(f"[ \x1B[1minfo\x1B[0m ] City: {RED}{city}{NRM}")
        print(f"[ \x1B[1minfo\x1B[0m ] Region: {RED}{region}{NRM}")
        print(f"[ \x1B[1minfo\x1B[0m ] Organization: {RED}{org}{NRM}")
        print(f"[ \x1B[1minfo\x1B[0m ] Timezone: {RED}{timezone}{NRM}")
        print(f"[ \x1B[1minfo\x1B[0m ] Latitude: {RED}{latitude}{NRM}")
        print(f"[ \x1B[1minfo\x1B[0m ] Longitude: {RED}{longitude}{NRM}")
        
        return final_data
    except Exception as e:
        print(f"[ \x1B[1m\x1B[31mERROR\x1B[0m ] {e}")
        return {"error": "Unknown error"}

# 主循环
while True:
    try:
        line = input(f'\n\001\x1B[37m\002H\001\x1B[0m\002\001\x1B[31m\002.\001\x1B[37m\002A\001\x1B[0m\002\001\x1B[31m\002.\001\x1B[37m\002M\001\x1B[0m\002\001\x1B[31m\002.\001\x1B[37m\002M\001\x1B[0m\002\001\x1B[31m\002.\001\x1B[37m\002E\001\x1B[0m\002\001\x1B[31m\002.\001\x1B[37m\002R\001\x1B[0m\002 \001\x1B[31m\002:\001\x1B[37m\002>\001\x1B[0m\002 ')
        line = line.split()

        if not line:
            continue

        if line[0] in ['quit', 'q', 'exit']:
            print("\n[ \x1B[1m+\x1B[0m ] Exiting HAMMER...")
            break

        elif line[0] == 'set':
            if len(line) < 3:
                print("\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] Syntax error in set")
                continue

            if line[1] == 'host':
                try:
                    host = line[2]
                    ip = socket.gethostbyname(host)
                    print(f"\n[ \x1B[1m+\x1B[0m ] Setting host to: {YEL}{host}{NRM} (IP: {YEL}{ip}{NRM})")
                    host_ports = []
                    scan_services = []
                    isp = ""
                    asn = ""
                    device_type = ""
                except:
                    print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] \"{line[2]}\" is not a valid domain or IP address")

            elif line[1] == 'workmode':
                if line[2] in workmodelist:
                    workmode = line[2]
                    print(f"\n[ \x1B[1m+\x1B[0m ] Using: {YEL}{workmode}{NRM} as workmode")
                else:
                    print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] \"{line[2]}\" not found in workmode\n\n{RED}[{MAG}{workmodelist}{RED}]{NRM}")

            else:
                print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] \"{line[1]}\" not found in set options")

        elif line[0] == 'show':
            try:
                if line[1] == 'full':
                    show(1)
                else:
                    show(0)
            except:
                show(0)

        elif line[0] == 'scan':
            if not host:
                print("\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] Host not set")
                continue

            print(f"\n[ \x1B[1m+\x1B[0m ] Running Scan module with mode: {RED}{workmode}{NRM}")
            if workmode == 'passive':
                host_ports, scan_services = scan_passive(ip)
            elif workmode == 'low':
                host_ports, device_type, scan_services = scan_low(ip)
            elif workmode == 'high':
                host_ports, device_type, scan_services = scan_high(ip)
            elif workmode == 'intrusive':
                host_ports, device_type, scan_services = scan_intrusive(ip)
            print("\n[ \x1B[1mDONE\x1B[0m ]")

        elif line[0] == 'info':
            if not host:
                print("\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] Host not set")
                continue
            info_data = get_info(ip)
            if "error" not in info_data:
                isp = info_data.get("isp", "")
                asn = info_data.get("asn", "")
                print("\n[ \x1B[1mDONE\x1B[0m ]")
            else:
                print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] {info_data['error']}")

        elif line[0] == 'help' or line[0] == '?':
            print("\n\x1B[32mReal Hackers don't need help, but here's a quick guide:")
            print("\nset host <IP/Domain> --> Set target host")
            print("set workmode <mode> --> Set scan mode (passive/low/high/intrusive)")
            print("scan --> Run scan on the target")
            print("show --> Show scan results")
            print("show full --> Show detailed scan results")
            print("info --> Get passive information about the target")
            print("quit/exit --> Exit HAMMER")
            print("\n\x1B[31mkey:8jK3l5mN9pQ1rS2tUvWxYzA4bC6dE7fG")
            print("\n")

        else:
            print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] Command \"{line[0]}\" not found")

    except Exception as e:
        print(f"\n[ \x1B[1m\x1B[31mERROR\x1B[0m ] {e}")
