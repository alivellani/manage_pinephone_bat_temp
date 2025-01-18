# Manage PinePhone Battery

## Introduction
Manage PinePhone Battery is a utility designed to enhance battery management on PinePhone devices. This tool allows for setting charging thresholds to optimize battery lifespan by preventing overcharging. The included scripts facilitate detailed battery status monitoring and automatic adjustment of charging behavior based on user-defined thresholds.

## Getting Started

### Prerequisites
Before you begin, ensure that you have `git` installed on your PinePhone to clone the repository.

### Installation
To install and set up the Manage PinePhone Battery service, follow these steps:

1. **Clone the repository:**
   ```
   git clone https://github.com/alivellani/manage_pinephone_bat_temp.git
   cd manage_pinephone_bat_temp
   ```

2. **Install the service and script:**
   Copy the script and service files into the appropriate directories.
   ```
   sudo cp manage_pinephone_bat.service /etc/systemd/system/
   sudo cp manage_pinephone_bat.py /usr/bin/
   ```

3. **Reload systemd:**
   Update systemd to recognize the new service file.
   ```
   sudo systemctl daemon-reload
   ```

4. **Enable the service:**
   Configure the service to start automatically at boot.
   ```
   sudo systemctl enable manage_pinephone_bat.service
   ```

5. **Start the service:**
   Begin the service immediately to start managing the battery.
   ```
   sudo systemctl start manage_pinephone_bat.service
   ```

## Usage
Once the service is running, it will automatically monitor and adjust the charging of your PinePhone's battery according to the thresholds set within the script. The `manage_pinephone_bat.py` script can be customized to suit your specific battery health strategies.

## Contributing
Contributions to improve Manage PinePhone Battery are welcomed. Please fork the repository, make your suggested changes, and submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer
This software is provided "as is", without warranty of any kind. The author is not responsible for any damages that may arise from its use. Please review the code and ensure its compatibility with your device before deployment.
