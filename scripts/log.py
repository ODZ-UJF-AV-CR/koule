#!/usr/bin/python3

import time
import serial
import threading
import serial.tools.list_ports;

def handle_data(data, fn):
    print(data)
    datafname = fn + '.log'
    with open(datafname, "a") as nbf:
        nbf.write(data)
    nbf.close()

def read_from_port(ser, fn):
	while True:
		try:
			reading = ser.readline().decode().rstrip()
			if (len(reading) > 0):
				handle_data(str(time.time()) + ' ' + reading + '\n', fn)
		except:
			pass

for port in serial.tools.list_ports.comports():
	print(port.device, port.vid)

	baud = 9600
	name = 'koule_' + port.name
	if (port.vid == 1155):
	    print('skipped')    # strip detector skipped
	    continue

	if (port.vid == 6790):
		baud = 115200
		name = 'CosmicWatch_' + port.name

	serial_port = serial.Serial(port.device, baud)

	thread = threading.Thread(target=read_from_port, args=(serial_port,name))
	thread.start()
