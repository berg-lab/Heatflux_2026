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
Instructions
Network Setup: Set WiFi SSID and password in the wpa_supplicant.conf file. Place this file in the boot partition on the microSD card. Add an empty ssh file as well to enable the SSH server on the Pi.

Transfer Files: Copy the heatflux folder to the /home/pi/ directory on the Raspberry Pi.

Create Virtual Environment: Navigate to the folder and set up your Python environment:
```
cd /home/pi/heatflux
python3 -m venv env
source env/bin/activate
pip install pyserial influxdb
```

Configure Sensors: In readserial.py, edit the number of heatflux sensors used, and input their sensitivities (found on the calibration sheets that come with the sensors).

Automate on Boot: To make sure the scripts are always running and restart automatically, the script_handler.sh file can be set to run on boot. First, give it executable permissions and fix line endings if transferred from Windows:
```
sed -i -e 's/\r$//' /home/pi/heatflux/script_handler.sh
sudo chmod +x /home/pi/heatflux/script_handler.sh
```
Then, run sudo nano /etc/rc.local and add the following on the second to last line (before exit 0):

```
cd /home/pi/heatflux;./script_handler.sh &
```
