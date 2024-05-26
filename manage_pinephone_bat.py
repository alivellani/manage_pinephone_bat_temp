import time
from datetime import datetime
import os

internal = "rk818-battery"
external = "ip5xxx-battery"
log_dir = "/home/kde/Documents/codes/manage_pinephone_bat/logs"

def read_battery_capacity(battery_type):
    with open(f'/sys/class/power_supply/{battery_type}/capacity', 'r') as file:
        capacity = file.read().strip()
    return capacity

def read_battery_behaviour(battery_type):
    with open(f'/sys/class/power_supply/{battery_type}/charge_behaviour', 'r') as file:
        behaviour = file.read().strip()
    return behaviour

def set_charge_behaviour(value, battery_type):
    path = f"/sys/class/power_supply/{battery_type}/charge_behaviour"
    try:
        fd = os.open(path, os.O_WRONLY)
        with os.fdopen(fd, 'w') as file:
            file.write(value)
        print(f"Charging behaviour for {battery_type} set to {value} successfully.")
    except PermissionError as e:
        print(f"Permission denied: {e}")
    except Exception as e:
        print(f"Failed to set charging behaviour for {battery_type}: {e}")

def inhibit_charge(battery_type):
    set_charge_behaviour("1", battery_type)

def enable_auto_charge(battery_type):
    set_charge_behaviour("auto", battery_type)

def is_batt_at_threshold(int_bat_perc, ext_bat_perc):
    if int_bat_perc == '100':
        inhibit_charge(internal)
        #print("set inhibiting charger internal")
    if int_bat_perc == "10":
        enable_auto_charge(internal)
        #print("setting auto charge intenral")
    if ext_bat_perc == '100':
        inhibit_charge(external)
        #print("set inhibit charger external")
    if ext_bat_perc == "20":
        enable_auto_charge(external)
        #print("set auto charge external")

def log_battery_status(int_bat_perc, ext_bat_perc, int_bat_beh, ext_bat_beh, charger_con):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = (f"{timestamp} Behaviour internal: {int_bat_beh}, "
                 f"Behaviour external: {ext_bat_beh}, "
                 f"Battery internal: {int_bat_perc}%, "
                 f"Battery external: {ext_bat_perc}%, "
                 f"charger: {charger_con}\n" )
    
    log_file = os.path.join(log_dir, datetime.now().strftime('%Y-%m-%d') + ".log")
    with open(log_file, 'a') as file:
        file.write(log_entry)

def is_charger_connected():
    with open(f'/sys/class/power_supply/ip5xxx-battery/charge_type', 'r') as file:
        charger = file.read().strip()
    return charger

if __name__ == "__main__":
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    enable_auto_charge(external)
    inhibit_charge(internal)

    while True:
        int_bat_perc = read_battery_capacity(internal)
        ext_bat_perc = read_battery_capacity(external)
        int_bat_beh = read_battery_behaviour(internal)
        ext_bat_beh = read_battery_behaviour(external)
        charger_con = is_charger_connected()
        log_battery_status(int_bat_perc, ext_bat_perc, int_bat_beh, ext_bat_beh, charger_con)
        is_batt_at_threshold(int_bat_perc, ext_bat_perc)
        time.sleep(600)
