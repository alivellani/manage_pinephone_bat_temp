import sys
import os

CHARGE_BEHAVIOUR_PATH = "/sys/class/power_supply/rk818-battery/charge_behaviour"

def set_charge_behaviour(value):
    if not os.path.exists(CHARGE_BEHAVIOUR_PATH):
        print(f"Error: {CHARGE_BEHAVIOUR_PATH} does not exist.")
        sys.exit(1)

    try:
        with open(CHARGE_BEHAVIOUR_PATH, 'w') as f:
            f.write(value)
        print(f"Successfully set charge behaviour to {value}")
    except PermissionError:
        print("Permission denied: Make sure to run this script with appropriate privileges (e.g., sudo).")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python control_internal_battery.py <enable|disable>")
        sys.exit(1)

    status = sys.argv[1]
    if status == "enable":
        set_charge_behaviour("auto")
    elif status == "disable":
        set_charge_behaviour("1")
    else:
        print("Invalid argument, use 'enable' or 'disable'")
        sys.exit(1)
