import serial.tools.list_ports

def find_ftdi_devices():
    ftdi_ports = []

    # Get the list of available serial ports
    ports = serial.tools.list_ports.comports()

    # Check each port for FTDI devices
    for port in ports:
        if "FTDI" in port.description.upper():
            ftdi_ports.append(port.device)

    return ftdi_ports

ftdi_devices = find_ftdi_devices()

if not ftdi_devices:
    print("No FTDI devices found.")
else:
    print("FTDI Devices:")
    for device in ftdi_devices:
        print(device)