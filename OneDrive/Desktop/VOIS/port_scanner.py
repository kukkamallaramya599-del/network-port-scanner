import socket

# Common port services
services = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS"
}

target = input("Enter target (website or IP): ")

# Convert to IP
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid target. Please enter a correct website or IP.")
    exit()

print(f"\nScanning target: {target} ({target_ip})\n")

# Ask user for port range
start_port = int(input("Enter starting port: "))
end_port = int(input("Enter ending port: "))

print("\nScanning ports...\n")

for port in range(start_port, end_port + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    
    result = s.connect_ex((target_ip, port))
    
    if result == 0:
        service = services.get(port, "Unknown")
        print(f"[OPEN] Port {port} - {service}")
    
    s.close()

print("\nScan completed ✅")