import serial
import time

def send_command(ser, command, sleep=1):
	ser.write(b'\r\n')
	time.sleep(sleep)
	ser.write((command + '\r\n').encode('utf-8'))
	time.sleep(sleep)
	ser.flush()
	time.sleep(sleep)
	output = []
	while ser.in_waiting > 0:
		line = ser.readline().decode('utf-8').strip()
		output.append(line)
	return output

def main():
	print("starter automatisering")
	serial_port = '/dev/ttyS5'
	baud_rate = 9600
	ser = serial.Serial(
		port=serial_port,
		baudrate=baud_rate,
		bytesize=serial.EIGHTBITS,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		timeout=5
	)
	print("opprettet serial")
	time.sleep(2)
	initial_output = ser.read_all().decode('utf-8')

	#output = send_command(ser, 'no')
	#time.sleep(5)
	#output = send_command(ser, 'yes')
	#time.sleep(5)
	send_command(ser, 'enable')
	time.sleep(2)
	send_command(ser, 'terminal length 0')
	output = send_command(ser, 'show version')
	print(output)
	#output = send_command(ser, 'interface gig0/0/0')
	#print(output)
	#output = send_command(ser, 'switchport mode trunk')

	print("Dette er nå ferdig")


	ser.close()
if __name__ == '__main__':

	main()
