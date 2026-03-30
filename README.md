# Heatflux_2026


# Raspberry Pi-based data logger for FluxTeq sensors

The [FluxTeq COMPAQ DAQ](https://www.fluxteq.com/product-page/compaq-daq) has a standard USB interface that can be plugged into a Raspberry Pi. This can then be used as a data logger to store data locally on the Pi's microSD card, or upload to an InfluxDB database on a remote server. 

This repository has been updated to support **Python 3**, isolated virtual environments (`venv`), dynamic sensor counting, and real-time 1-second logging.

---
## Prerequisites

Modern Raspberry Pi OS environments require virtual environments to install Python packages. Run the following commands to install the `venv` prerequisite:
```
sudo apt-get update
sudo apt-get install python3-venv
```
## Instructions
Network Setup: Set WiFi SSID and password in the wpa_supplicant.conf file. Place this file in the boot partition on the microSD card. Add an empty ssh file as well to enable the SSH server on the Pi.

Transfer Files: Copy the heatflux folder to the /home/pi/ directory on the Raspberry Pi.

Create Virtual Environment: Navigate to the folder and set up your Python environment:
```
cd /home/pi/heatflux
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Configure Sensors: In readserial.py, edit the number of heatflux sensors used, and input their sensitivities (found on the calibration sheets that come with the sensors).

Configure Database Credentials:** For security, database credentials are not hardcoded. Create a file named `database.ini` in the `/home/pi/heatflux` directory:
```
nano /home/pi/heatflux/database.ini
```
Paste the following template and fill in your InfluxDB (v1.x) details:
```
[influxdb]
server = 192.168.x.x
port = 8086
user = your_username
password = your_password
database = your_database
```
Automation (Systemd Service):

To ensure the scripts run in the background, start automatically on boot, and restart if they crash, configure a systemd service.

Ensure the handler script has executable permissions and Unix line endings:

```
sed -i -e 's/\r$//' /home/pi/heatflux/script_handler.sh
sudo chmod +x /home/pi/heatflux/script_handler.sh
```
Create a new service file:
```
sudo nano /etc/systemd/system/heatflux.service
```
Paste the following configuration into the file, save, and exit:
```
[Unit]
Description=FluxTeq Heat Flux Data Logger
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/heatflux
ExecStart=/home/pi/heatflux/script_handler.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
Enable and start the service:

```
sudo systemctl daemon-reload
sudo systemctl enable heatflux.service
sudo systemctl start heatflux.service
```
You can check the status of your data logger at any time by running ```sudo systemctl status heatflux.service```


Reboot your Raspberry Pi. The data logger will automatically initialize the DAQ, create the local .csv backup, and begin pushing data to InfluxDB.
Once configured, simply reboot your Raspberry Pi. The data logger will automatically initialize the DAQ, create the local .csv backup, and begin pushing data to InfluxDB.
