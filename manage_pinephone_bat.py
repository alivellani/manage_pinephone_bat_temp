# # s/usr/bin/manage_pinephone_bat.py
# # sudo cp Documents/codes/manage_pinephone_bat/manage_pinephone_bat.py /usr/bin/manage_pinephone_bat.py


import time
from datetime import datetime
import os

internal = "rk818-battery"
external = "ip5xxx-battery"
log_dir = "/home/user/Documents/codes/manage_pinephone_bat/logs"

def read_battery_capacity(battery_type):
    try:
        with open(f'/sys/class/power_supply/{battery_type}/capacity', 'r') as file:
            capacity = file.read().strip()
        return int(capacity)
    except:
        return 'NA'

def read_battery_behaviour(battery_type):
    try:
        with open(f'/sys/class/power_supply/{battery_type}/charge_behaviour', 'r') as file:
            behaviour = file.read().strip()
        return behaviour
    except:
        return 'NA'

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

def check_thresh(perc, behav, loc):
    if perc > 90 and '[auto]' in behav:
        inhibit_charge(loc)
        print(f"set inhibiting charger {loc}")
    if perc < 50 and '[inhibit-charge]' in behav:
        enable_auto_charge(loc)
        print(f"setting auto charge {loc}")

def is_batt_at_threshold(int_bat_perc, ext_bat_perc, int_bat_beh, ext_bat_beh ):
    check_thresh(int_bat_perc, int_bat_beh, internal)
    check_thresh(ext_bat_perc, ext_bat_beh, external)

    # keyboard is connected, not charging the phone. 
    # will suck the keyboard battery dry
    # turn off keyboard then charge the phone
    # somehow all this smartness is not needed in postmarketos 
    # as internal battery is nto being charged by external

    # # regardless keyboard present or not, give priority to phone
    # check_thresh(int_bat_perc, int_bat_beh, internal)


    # if ext_bat_beh != 'NA':
    #     print("keyboard connected")
    #     check_thresh(int_bat_perc, int_bat_beh, internal)
              
    #     inhibit_charge(internal)

    #     check_thresh(ext_bat_perc, ext_bat_beh, external)
    # else:
    #     #check_thresh(int_bat_perc, int_bat_beh, internal)

def log_battery_status(int_bat_perc, ext_bat_perc, int_bat_beh, ext_bat_beh, int_charger_con, ext_charger_con):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = (f"{timestamp} Behaviour internal: {int_bat_beh}, "
                 f"Battery internal: {int_bat_perc}%, "
                 f"int_charger: {int_charger_con}, "
                 f"Behaviour external: {ext_bat_beh}, "   
                 f"Battery external: {ext_bat_perc}%, "
                 f"ext_charger: {ext_charger_con}\n" )
    
    log_file = os.path.join(log_dir, datetime.now().strftime('%Y-%m-%d') + ".log")
    with open(log_file, 'a') as file:
        file.write(log_entry)


def is_charger_connected(battery_type):
    try: 
        with open(f'/sys/class/power_supply/{battery_type}/charge_type', 'r') as file:
            charger = file.read().strip()
        return charger
    except:
        return 'NA'

if __name__ == "__main__":
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    #enable_auto_charge(external)
    # disable external charge by 
    enable_auto_charge(external)
    enable_auto_charge(internal)
    

    while True:
        int_bat_perc = read_battery_capacity(internal)
        print(f"int_bat_perc {int_bat_perc}")
        ext_bat_perc = read_battery_capacity(external)
        int_bat_beh = read_battery_behaviour(internal)
        
        ext_bat_beh = read_battery_behaviour(external)
        int_charger_con = is_charger_connected(internal)
        print(f"int_charger_con {int_charger_con}")
        ext_charger_con = is_charger_connected(external)
        log_battery_status(int_bat_perc, ext_bat_perc, int_bat_beh, ext_bat_beh, int_charger_con, ext_charger_con)
        is_batt_at_threshold(int_bat_perc, ext_bat_perc, int_bat_beh, ext_bat_beh )
        time.sleep(600)
