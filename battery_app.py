import tkinter as tk
from tkinter import messagebox
from threading import Thread
import time
from manage_pinephone_bat import read_battery_capacity, read_battery_behaviour, inhibit_charge, enable_auto_charge, internal, external

class BatteryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PinePhone Pro Battery Manager")
        
        # Internal Battery
        self.int_label = tk.Label(root, text="Internal Battery:")
        self.int_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.int_status = tk.Label(root, text="Reading...")
        self.int_status.grid(row=0, column=1, padx=10, pady=10)
        
        self.int_disable_button = tk.Button(root, text="Disable Internal Charge", command=self.disable_internal_charge)
        self.int_disable_button.grid(row=0, column=2, padx=10, pady=10)
        
        self.int_enable_button = tk.Button(root, text="Enable Internal Charge", command=self.enable_internal_charge)
        self.int_enable_button.grid(row=0, column=3, padx=10, pady=10)
        
        # External Battery
        self.ext_label = tk.Label(root, text="External Battery:")
        self.ext_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.ext_status = tk.Label(root, text="Reading...")
        self.ext_status.grid(row=1, column=1, padx=10, pady=10)
        
        self.ext_disable_button = tk.Button(root, text="Disable External Charge", command=self.disable_external_charge)
        self.ext_disable_button.grid(row=1, column=2, padx=10, pady=10)
        
        self.ext_enable_button = tk.Button(root, text="Enable External Charge", command=self.enable_external_charge)
        self.ext_enable_button.grid(row=1, column=3, padx=10, pady=10)

        # Start the thread to update the status regularly
        self.update_thread = Thread(target=self.update_battery_status, daemon=True)
        self.update_thread.start()

    def update_battery_status(self):
        while True:
            int_bat_perc = read_battery_capacity(internal)
            ext_bat_perc = read_battery_capacity(external)
            int_bat_beh = read_battery_behaviour(internal)
            ext_bat_beh = read_battery_behaviour(external)

            # Update the labels with the latest values
            self.int_status.config(text=f"{int_bat_perc}% - {int_bat_beh}")
            self.ext_status.config(text=f"{ext_bat_perc}% - {ext_bat_beh}")

            time.sleep(10)  # Update every 10 seconds

    def disable_internal_charge(self):
        inhibit_charge(internal)
        messagebox.showinfo("Action", "Internal charging disabled")

    def enable_internal_charge(self):
        enable_auto_charge(internal)
        messagebox.showinfo("Action", "Internal charging enabled")

    def disable_external_charge(self):
        inhibit_charge(external)
        messagebox.showinfo("Action", "External charging disabled")

    def enable_external_charge(self):
        enable_auto_charge(external)
        messagebox.showinfo("Action", "External charging enabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = BatteryApp(root)
    root.mainloop()
