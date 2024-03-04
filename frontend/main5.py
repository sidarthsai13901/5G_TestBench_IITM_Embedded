from tkinter import *
import serial
import threading
from pyftdi.i2c import I2cController, I2cNackError

# Global variable for UART reading thread control
stop_threads = False

def show():
    for frame in frames.values():
        frame.pack_forget()
    frame = frames[clicked.get()]
    frame.pack(fill='both', expand=True)

# UART Read Functionality
def uart_read():
    global stop_threads
    com_port = com_port_entry_read.get()
    baud_rate_str = baud_rate_entry_read.get()
    try:
        baud_rate = int(baud_rate_str)
    except ValueError:
        uart_read_output.config(text="Invalid baud rate")
        return

    try:
        ser = serial.Serial(com_port, baud_rate, timeout=1)
        uart_read_output.config(text="Listening for incoming data...")
        while not stop_threads:
            data_in = ser.readline()
            if data_in:
                message = data_in.decode('utf-8').rstrip('\r\n')
                uart_read_output.config(text=f"Received: {message}")
    except serial.SerialException as e:
        uart_read_output.config(text=f"Error: {str(e)}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

def start_uart_read():
    global stop_threads
    stop_threads = False
    threading.Thread(target=uart_read, daemon=True).start()

def stop_uart_read():
    global stop_threads
    stop_threads = True
    uart_read_output.config(text="UART Read stopped.")

# UART Write Functionality
def uart_write():
    com_port = com_port_entry_write.get()
    baud_rate_str = baud_rate_entry_write.get()
    try:
        baud_rate = int(baud_rate_str)
    except ValueError:
        uart_write_output.config(text="Invalid baud rate")
        return

    message = uart_write_entry.get() + "\n"
    try:
        ser = serial.Serial(com_port, baud_rate)
        ser.write(message.encode('utf-8'))
        uart_write_output.config(text=f"Sent: {message}")
    except serial.SerialException as e:
        uart_write_output.config(text=f"Error: {str(e)}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

# I2C Scan and Read Functionality
def i2c_scan_read():
    i2c_reg_str = i2c_reg_entry.get()
    bytes_num = int(i2c_bytes.get())
    selected_slave_addr = slave_addr_var.get()

    if not selected_slave_addr:
        i2c_output_label.config(text="No I2C address selected")
        return

    try:
        slave_addr = int(selected_slave_addr, 16)
        register_addr = int(i2c_reg_str, 16)
    except ValueError:
        i2c_output_label.config(text="Invalid address or register")
        return

    i2c = I2cController()
    try:
        i2c.configure('ftdi://ftdi:232h:FT9Q27K3/1')
        slave = i2c.get_port(slave_addr)
        slave.write([register_addr], False)
        data = slave.read(bytes_num)
        i2c_output_label.config(text=f"Read: {data}")
    except Exception as e:
        i2c_output_label.config(text=f"Error: {str(e)}")
    finally:
        i2c.terminate()

def i2c_scan():
    i2c = I2cController()
    address_list = []
    try:
        i2c.configure('ftdi://ftdi:232h:FT9Q27K3/1')
        for addr in range(0x08, 0x78):  # Valid 7-bit addresses
            port = i2c.get_port(addr)
            try:
                port.read(1)
                address_list.append(f"0x{addr:02X}")
            except I2cNackError:
                continue
    finally:
        i2c.terminate()

    # Update the dropdown menu with found addresses
    slave_addr_menu['menu'].delete(0, 'end')
    for address in address_list:
        slave_addr_menu['menu'].add_command(label=address, command=lambda value=address: slave_addr_var.set(value))
    if address_list:
        slave_addr_var.set(address_list[0])
    else:
        i2c_output_label.config(text="No I2C devices found")

# Main GUI Setup
root = Tk()
root.geometry("600x400")

frame_container = Frame(root, width=600, height=200)
frame_container.pack(side="bottom", fill="x", expand=True)

frames = {}
options = ["UART READ", "UART WRITE", "I2C READ", "SPI READ"]

# UART READ Frame Setup
frame1 = Frame(frame_container, width=600, height=200)
com_port_label_read = Label(frame1, text="COM Port:")
com_port_entry_read = Entry(frame1)
baud_rate_label_read = Label(frame1, text="Baud Rate:")
baud_rate_entry_read = Entry(frame1)
uart_read_button = Button(frame1, text="Start Read", command=start_uart_read)
uart_read_stop_button = Button(frame1, text="Stop Read", command=stop_uart_read)
uart_read_output = Label(frame1, text="No data received yet")
com_port_label_read.pack()
com_port_entry_read.pack()
baud_rate_label_read.pack()
baud_rate_entry_read.pack()
uart_read_button.pack()
uart_read_stop_button.pack()
uart_read_output.pack()
frames["UART READ"] = frame1

# UART WRITE Frame Setup
frame2 = Frame(frame_container, width=600, height=200)
com_port_label_write = Label(frame2, text="COM Port:")
com_port_entry_write = Entry(frame2)
baud_rate_label_write = Label(frame2, text="Baud Rate:")
baud_rate_entry_write = Entry(frame2)
uart_write_label = Label(frame2, text="Data to send:")
uart_write_entry = Entry(frame2)
uart_write_button = Button(frame2, text="Send Data", command=uart_write)
uart_write_output = Label(frame2, text="No data sent yet")
com_port_label_write.pack()
com_port_entry_write.pack()
baud_rate_label_write.pack()
baud_rate_entry_write.pack()
uart_write_label.pack()
uart_write_entry.pack()
uart_write_button.pack()
uart_write_output.pack()
frames["UART WRITE"] = frame2

# I2C READ Frame Setup with Scan Functionality
frame3 = Frame(frame_container, width=600, height=200)
i2c_label = Label(frame3, text="I2C Read Parameters")
i2c_scan_button = Button(frame3, text="Scan I2C Bus", command=i2c_scan)
slave_addr_var = StringVar(root)
slave_addr_menu = OptionMenu(frame3, slave_addr_var, "No address")
i2c_slave_label = Label(frame3, text="Select I2C Slave Address:")
i2c_reg_label = Label(frame3, text="Register Address (hex):")
i2c_reg_entry = Entry(frame3)
i2c_bytes_label = Label(frame3, text="Number of Bytes to Read:")
i2c_bytes = Entry(frame3)
i2c_read_button = Button(frame3, text="Read I2C", command=i2c_scan_read)
i2c_output_label = Label(frame3, text="No data read yet")
i2c_label.pack()
i2c_scan_button.pack()
i2c_slave_label.pack()
slave_addr_menu.pack()
i2c_reg_label.pack()
i2c_reg_entry.pack()
i2c_bytes_label.pack()
i2c_bytes.pack()
i2c_read_button.pack()
i2c_output_label.pack()
frames["I2C READ"] = frame3

# SPI READ Frame Setup remains the same...

clicked = StringVar()
clicked.set(options[0])  # Default set to first option

drop = OptionMenu(root, clicked, *options)
drop.pack()

button = Button(root, text="Select", command=show)
button.pack()

root.mainloop()
