import socket
import tkinter as tk
from tkinter import messagebox

def scan_ports():
    target = entry_target.get()
    start_port = entry_start.get()
    end_port = entry_end.get()
    
    # Clear output
    text_output.delete('1.0', tk.END)
    
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        messagebox.showerror("Error", "Invalid target")
        return
    
    try:
        start = int(start_port)
        end = int(end_port)
    except ValueError:
        messagebox.showerror("Error", "Ports must be numbers")
        return
    
    text_output.insert(tk.END, f"Scanning {target} ({target_ip})...\n\n")
    
    for port in range(start, end + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            text_output.insert(tk.END, f"Port {port} is OPEN\n")
        
        s.close()
    
    text_output.insert(tk.END, "\nScan Completed ✅")

# GUI window
root = tk.Tk()
root.title("Network Port Scanner")
root.geometry("500x400")

# Labels & Inputs
tk.Label(root, text="Target (IP or Website):").pack()
entry_target = tk.Entry(root, width=40)
entry_target.pack()

tk.Label(root, text="Start Port:").pack()
entry_start = tk.Entry(root)
entry_start.pack()

tk.Label(root, text="End Port:").pack()
entry_end = tk.Entry(root)
entry_end.pack()

# Button
tk.Button(root, text="Scan", command=scan_ports).pack(pady=10)

# Output box
text_output = tk.Text(root, height=15, width=60)
text_output.pack()

root.mainloop()