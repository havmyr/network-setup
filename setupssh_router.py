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

def setup_device(commands, hostname="Device", port='/dev/ttyS5', baud=9600):
    print(f"[+] Kobler til {hostname} via {port} ({baud} baud)")
    ser = serial.Serial(
        port=port,
        baudrate=baud,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=5
    )
    time.sleep(2)
    ser.read_all()  # Tøm bufferen

    print("[+] Starter konfigurasjon...")

    for cmd, delay in commands:
        print(f" -> Kjører: {cmd}")
        output = send_command(ser, cmd, sleep=delay)
        for line in output:
            print("   ", line)

    print(f"[✓] Ferdig med {hostname}")
    ser.close()
