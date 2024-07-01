import psutil
import requests
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
from screeninfo import get_monitors
import screen_brightness_control as sbc
import logging

# Configure logging
logging.basicConfig(filename='system_monitor.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class SystemMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Monitor")
        self.root.geometry("600x500")
        self.root.configure(bg="#282c34")

        self.style = ttk.Style()
        self.style.configure("TLabel", background="#282c34", foreground="#ffffff", font=("Arial", 12))
        self.style.configure("TButton", background="#61afef", foreground="#ffffff", font=("Arial", 12))
        self.style.map("TButton", background=[("active", "#528bb7")])

        self.create_widgets()
        self.check_system_health()

    def create_widgets(self):
        self.cpu_label = ttk.Label(self.root, text="CPU Usage: ")
        self.cpu_label.pack(pady=10)

        self.memory_label = ttk.Label(self.root, text="Memory Usage: ")
        self.memory_label.pack(pady=10)

        self.disk_label = ttk.Label(self.root, text="Disk Usage: ")
        self.disk_label.pack(pady=10)

        self.network_label = ttk.Label(self.root, text="Network Connectivity: ")
        self.network_label.pack(pady=10)

        self.screen_label = ttk.Label(self.root, text="Screen Info: ", wraplength=500)
        self.screen_label.pack(pady=10)

        self.brightness_label = ttk.Label(self.root, text="Brightness Level: ", wraplength=500)
        self.brightness_label.pack(pady=10)

        self.refresh_button = ttk.Button(self.root, text="Refresh", command=self.check_system_health)
        self.refresh_button.pack(pady=10)

        self.run_button = ttk.Button(self.root, text="Run", command=self.run_checks)
        self.run_button.pack(pady=10)

    def log_message(self, level, message):
        print(message)
        if level == "warning":
            messagebox.showwarning("Warning", message)
        elif level == "error":
            messagebox.showerror("Error", message)
        else:
            messagebox.showinfo("Info", message)

    def check_cpu_usage(self, threshold=80):
        try:
            usage = psutil.cpu_percent(interval=1)
            if usage > threshold:
                self.log_message("warning", f"High CPU usage detected! Usage: {usage}%")
            self.cpu_label.config(text=f"CPU Usage: {usage}%")
            return f"CPU Usage: {usage}%"
        except Exception as e:
            self.log_message("error", f"Error checking CPU usage: {str(e)}")
            return f"Error checking CPU usage: {str(e)}"

    def check_memory_usage(self, threshold=80):
        try:
            memory = psutil.virtual_memory()
            usage = memory.percent
            if usage > threshold:
                self.log_message("warning", f"High memory usage detected! Usage: {usage}%")
            self.memory_label.config(text=f"Memory Usage: {usage}%")
            return f"Memory Usage: {usage}%"
        except Exception as e:
            self.log_message("error", f"Error checking memory usage: {str(e)}")
            return f"Error checking memory usage: {str(e)}"

    def check_disk_usage(self, threshold=80):
        try:
            disk = psutil.disk_usage('/')
            usage = disk.percent
            if usage > threshold:
                self.log_message("warning", f"High disk usage detected! Usage: {usage}%")
            self.disk_label.config(text=f"Disk Usage: {usage}%")
            return f"Disk Usage: {usage}%"
        except Exception as e:
            self.log_message("error", f"Error checking disk usage: {str(e)}")
            return f"Error checking disk usage: {str(e)}"

    def check_network_connectivity(self, url='http://www.google.com'):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.network_label.config(text="Network Connectivity: Normal")
                return "Network Connectivity: Normal"
            else:
                self.log_message("warning", f"Network issue detected! Status code: {response.status_code}")
                self.network_label.config(text="Network Connectivity: Issue Detected")
                return f"Network Connectivity: Issue Detected, Status code: {response.status_code}"
        except requests.ConnectionError:
            self.log_message("error", "No network connectivity")
            self.network_label.config(text="Network Connectivity: No Connectivity")
            return "Network Connectivity: No Connectivity"
        except Exception as e:
            self.log_message("error", f"Error checking network connectivity: {str(e)}")
            return f"Error checking network connectivity: {str(e)}"

    def check_screen_issues(self):
        try:
            monitors = get_monitors()
            screen_info = ""
            for monitor in monitors:
                screen_info += f"Monitor: {monitor.name}, Width: {monitor.width}, Height: {monitor.height}, DPI: {monitor.dpi}\n"
            self.screen_label.config(text=f"Screen Info: \n{screen_info.strip()}")
            return screen_info.strip()
        except Exception as e:
            self.log_message("error", f"Error checking screen issues: {str(e)}")
            return f"Error checking screen issues: {str(e)}"

    def check_brightness_level(self):
        try:
            brightness = sbc.get_brightness()
            brightness_info = ""
            for i, level in enumerate(brightness):
                brightness_info += f"Monitor {i} brightness level: {level}%\n"
            self.brightness_label.config(text=f"Brightness Level: \n{brightness_info.strip()}")
            return brightness_info.strip()
        except Exception as e:
            self.log_message("error", f"Error checking brightness level: {str(e)}")
            return f"Error checking brightness level: {str(e)}"

    def check_system_health(self):
        self.check_cpu_usage()
        self.check_memory_usage()
        self.check_disk_usage()
        self.check_network_connectivity()
        self.check_screen_issues()
        self.check_brightness_level()

        # Refresh the checks every 60 seconds
        self.root.after(60000, self.check_system_health)

    def run_checks(self):
        cpu_info = self.check_cpu_usage()
        memory_info = self.check_memory_usage()
        disk_info = self.check_disk_usage()
        network_info = self.check_network_connectivity()
        screen_info = self.check_screen_issues()
        brightness_info = self.check_brightness_level()

        details = (f"{cpu_info}\n"
                   f"{memory_info}\n"
                   f"{disk_info}\n"
                   f"{network_info}\n"
                   f"Screen Info:\n{screen_info}\n"
                   f"Brightness Level:\n{brightness_info}")

        messagebox.showinfo("System Details", details)

def main():
    root = tk.Tk()
    app = SystemMonitorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
