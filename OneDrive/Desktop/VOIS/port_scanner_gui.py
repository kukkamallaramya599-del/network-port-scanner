import socket
import threading
import tkinter as tk
from tkinter import messagebox, ttk

# Global variables
stop_flag = False

def scan_ports():
    global stop_flag
    stop_flag = False

    target = entry_target.get()
    start_port = entry_start.get()
    end_port = entry_end.get()

    text_output.delete('1.0', tk.END)
    progress_bar['value'] = 0

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

    total_ports = end - start + 1
    progress_bar['maximum'] = total_ports

    text_output.insert(tk.END, f"Scanning {target} ({target_ip})...\n\n")

    def scan(port):
        global stop_flag
        if stop_flag:
            return

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)

        result = s.connect_ex((target_ip, port))

        if result == 0:
            text_output.insert(tk.END, f"Port {port} is OPEN\n")

        s.close()

        progress_bar.step(1)

    threads = []

    for port in range(start, end + 1):
        if stop_flag:
            break

        t = threading.Thread(target=scan, args=(port,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not stop_flag:
        text_output.insert(tk.END, "\nScan Completed ✅")
    else:
        text_output.insert(tk.END, "\nScan Stopped ❌")


def stop_scan():
    global stop_flag
    stop_flag = True


# GUI Setup
root = tk.Tk()
root.title("Network Port Scanner")
root.geometry("600x500")

# Input Fields
tk.Label(root, text="Target (IP or Website):").pack()
entry_target = tk.Entry(root, width=40)
entry_target.pack()

tk.Label(root, text="Start Port:").pack()
entry_start = tk.Entry(root)
entry_start.pack()

tk.Label(root, text="End Port:").pack()
entry_end = tk.Entry(root)
entry_end.pack()

# Buttons
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

tk.Button(frame_buttons, text="Start Scan", command=scan_ports).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="Stop", command=stop_scan).grid(row=0, column=1, padx=5)

# Progress Bar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

# Output Box
text_output = tk.Text(root, height=18, width=70)
text_output.pack()

root.mainloop()