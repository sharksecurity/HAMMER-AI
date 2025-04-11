import subprocess

def scan_passive(host):
    ports_list = []
    services_list = []
    stdoutdata = subprocess.getoutput(f"nmap -sT -T2 {host} --open | grep \"open\"")
    lines = stdoutdata.splitlines()
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            port_info = parts[0].split("/")
            try:
                ports_list.append(int(port_info[0]))
                services_list.append(parts[1])
            except:
                pass
    return ports_list, services_list

def scan_low(host):
    ports_list = []
    services_list = []
    device_type = ""
    stdoutdata = subprocess.getoutput(f"nmap -sT -O {host} --open")
    lines = stdoutdata.splitlines()
    for line in lines:
        if "open" in line:
            parts = line.split()
            if len(parts) >= 2:
                port_info = parts[0].split("/")
                try:
                    ports_list.append(int(port_info[0]))
                    services_list.append(parts[1])
                except:
                    pass
        if "Device type:" in line:
            device_type = line.split("Device type:")[1].strip().split()[0]
    return ports_list, device_type, services_list

def scan_high(host):
    ports_list = []
    services_list = []
    device_type = ""
    stdoutdata = subprocess.getoutput(f"nmap -sT -sV -O --top-ports 10000 {host} --open")
    lines = stdoutdata.splitlines()
    for line in lines:
        if "open" in line:
            parts = line.split()
            if len(parts) >= 2:
                port_info = parts[0].split("/")
                try:
                    ports_list.append(int(port_info[0]))
                    services_list.append(parts[1])
                except:
                    pass
        if "Device type:" in line:
            device_type = line.split("Device type:")[1].strip().split()[0]
    return ports_list, device_type, services_list

def scan_intrusive(host):
    ports_list = []
    services_list = []
    device_type = ""
    stdoutdata = subprocess.getoutput(f"nmap -sT -sV -O -p- {host} --open")
    lines = stdoutdata.splitlines()
    for line in lines:
        if "open" in line:
            parts = line.split()
            if len(parts) >= 2:
                port_info = parts[0].split("/")
                try:
                    ports_list.append(int(port_info[0]))
                    services_list.append(parts[1])
                except:
                    pass
        if "Device type:" in line:
            device_type = line.split("Device type:")[1].strip().split()[0]
    return ports_list, device_type, services_list