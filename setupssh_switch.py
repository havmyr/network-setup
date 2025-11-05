import serial
import time

def send_command(ser, command, sleep=1):
    ser.write(b'\r\n')
    time.sleep(0.5)
    ser.write((command + '\r\n').encode('utf-8'))
    time.sleep(sleep)
    ser.flush()
    output = []
    while ser.in_waiting > 0:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        output.append(line)
    return output

def setup_device(commands):
    print(f"[+] Kobler til switch")
    ser = serial.Serial(
        port="/dev/ttyS1",
        baudrate=9600,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=5
    )
    time.sleep(2)
    ser.read_all()  # tøm buffer

    print(f"[+] Starter konfigurasjon for switch ...")

    for cmd, delay in commands:
        print(f" -> Kjører: {cmd}")
        output = send_command(ser, cmd, sleep=delay)
        for line in output:
            print("   ", line)

    print(f"[✓] Ferdig med switch")
    ser.close()

def main():
    switch_commands = [
        ('enable', 1),
        ('terminal length 0', 1),
        ('configure terminal', 1),
        ('hostname S1', 1),
        ('ip domain name test.local', 1),
        ('crypto key generate rsa', 3),
        ('2048', 2),
        ('username cisco privilege 15 secret cisco', 1),
        ('ip ssh version 2', 1),
        ('ip ssh authentication-retries 3', 1),
        ('vlan 10', 1),
        ('name Sales', 1),
        ('exit', 0.5),
        ('interface vlan 10', 1),
        ('ip address 192.168.1.100 255.255.255.0', 1),
        ('no shutdown', 1),
        ('exit', 0.5),
        ('ip default-gateway 192.168.10.1', 1),
        ('interface range fastEthernet 0/1 - 12', 1),
        ('switchport mode access', 1),
        ('switchport access vlan 10', 1),
        ('no shutdown', 1),
        ('exit', 0.5),
        ('line vty 0 4', 1),
        ('login local', 1),
        ('transport input ssh', 1),
        ('end', 0.5),
        ('write memory', 2)
    ]

    setup_device(switch_commands)

if __name__ == '__main__':
    main()
