import pandas as pd
import matplotlib.pyplot as plt
import re
import os

def load_logs(folder_path):
    logs = {}
    file_names = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".log"):
            file_path = os.path.join(folder_path, file_name)
            log_data = pd.read_csv(file_path, sep='\t', header=None)
            logs[file_name] = log_data
            file_names.append(file_name)
    
    # Sort file names by date
    file_names.sort(key=lambda date: pd.to_datetime(date.split('.')[0]))
    return logs, file_names

def parse_logs(data):
    timestamps = []
    internal_battery = []
    external_battery = []

    timestamp_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
    internal_battery_pattern = r'Battery internal: (\d+)%'
    external_battery_pattern = r'Battery external: (\d+)%'

    for entry in data[0]:
        timestamp_match = re.search(timestamp_pattern, entry)
        internal_battery_match = re.search(internal_battery_pattern, entry)
        external_battery_match = re.search(external_battery_pattern, entry)
        
        if timestamp_match and internal_battery_match:
            timestamps.append(timestamp_match.group(1))
            internal_battery.append(int(internal_battery_match.group(1)))
            if external_battery_match:
                external_battery.append(int(external_battery_match.group(1)))
            else:
                external_battery.append(None)

    parsed_data = pd.DataFrame({
        'Timestamp': pd.to_datetime(timestamps),
        'InternalBattery': internal_battery,
        'ExternalBattery': external_battery
    })
    return parsed_data

def plot_battery_data(parsed_data, show_external):
    plt.figure(figsize=(12, 6))
    plt.plot(parsed_data['Timestamp'], parsed_data['InternalBattery'], label='Internal Battery')
    
    if show_external:
        plt.plot(parsed_data['Timestamp'], parsed_data['ExternalBattery'], label='External Battery')

    plt.xlabel('Timestamp')
    plt.ylabel('Battery Level (%)')
    plt.title('Internal and External Battery Levels Over Time')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Load all log files
#folder_path = '/run/user/1000/gvfs/sftp://kde@192.168.100.150/home/kde/Documents/codes/manage_pinephone_bat/logs/'
#folder_path = '/run/user/1000/gvfs/sftp:/kde@192.168.100.150/home/kde/Documents/codes/manage_pinephone_bat/logs/'
folder_path = 'logs'
logs, file_names = load_logs(folder_path)

# Display available indices
print("Available files:")
for idx, name in enumerate(file_names):
    print(f"{idx}: {name}")

# Ask the user for the range of days to include
range_input = input("Enter the range of indices of the days to include (e.g., 0-5): ")
start_idx, end_idx = map(int, range_input.split('-'))

# Filter the data based on the selected range
selected_logs = [file_names[i] for i in range(start_idx, end_idx + 1)]
selected_data = pd.concat([logs[log] for log in selected_logs], ignore_index=True)

# Parse the selected data
parsed_data = parse_logs(selected_data)

# Ask the user if they want to include the external battery data
show_external = input("Do you want to include the external battery data? (yes/no): ").strip().lower() == 'yes'

# Plot the data
plot_battery_data(parsed_data, show_external)
