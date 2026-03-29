# -*- coding: utf-8 -*-

# This script initializes Fluxteq's Compaq DAQ,
# reads data from serial port and saves to temporary file

import time
import serial
import os

number_of_sensors = '1' # set number of sensors connected to Compaq DAQ
sensitivities = ['1.08']    # set sensitivities. First one is channel 0
temp_data_dir = '/var/tmp/temp_heatflux'

# initialize serial port
try:
    serialport = serial.Serial('/dev/ttyUSB0', 9600, timeout=2) # make sure baud rate is the same
except serial.SerialException as e:
    print(f'Serial Port Failed: {e}')
    while True:     # loop forever
        time.sleep(1)
        pass

time.sleep(3)  # wait few seconds till serial port initialized

# send initial configuration to the DAQ to begin logging
try:
    # PYTHON 3 FIX: encode strings to bytes before writing
    serialport.write(number_of_sensors.encode('utf-8'))
    time.sleep(1.5)
    for n in range(int(number_of_sensors)):
        serialport.write(sensitivities[n].encode('utf-8'))
        time.sleep(1.5)
    print("Successfully configured DAQ.")
except Exception as e:
    print(f'Failed to write data: {e}')
    pass

time.sleep(1)

# loop forever
while True:
    data = serialport.read(1)   # get first byte from serial port
    n = serialport.in_waiting   # check remaining number of bytes
    if n:    # wait till data arrives and then read it
        data = data + serialport.readline()    # read one line and merge with first byte
        
        try:
            # PYTHON 3 FIX: decode the incoming bytes back into a standard string
            decoded_data = data.decode('utf-8')
            
            # --- DEBUG PRINT: See the cleaned up string only ---
            print(f"DATA: {decoded_data.strip()}") 
            
            file = open('%s/t.csv' % temp_data_dir,'w')
            file.write(decoded_data)     # save data in a temp csv file
            file.close()
        except Exception as e:
            print(f"File write error or Decoding error: {e}")
            pass
    else:
        continue    # ignore bad packets or no data received

    time.sleep(0.01)    # wait a bit so CPU doesn't choke to def