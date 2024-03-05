from tkinter import *
import serial
import threading
from pyftdi.i2c import I2cController

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

# I2C Read Functionality
def i2c_read():
    i2c_slave_str = i2c_slave_entry.get()
    i2c_reg_str = i2c_reg_entry.get()
    bytes_num=i2c_bytes.get()
    board_add_val=board_add.get()
    # print(board_add_val)
    try:
        slave_addr = int(i2c_slave_str, 16)
        register_addr = int(i2c_reg_str, 16)
    except ValueError:
        i2c_output_label.config(text="Invalid address")
        return

    i2c = I2cController()
    try:
        i2c.configure(board_add_val)  # Modify as needed
        slave = i2c.get_port(slave_addr)
        slave.write([register_addr], False)
        data = slave.read(bytes_num)  # Modify based on expected data length
        i2c_output_label.config(text=f"Read: {data}")
    except Exception as e:
        i2c_output_label.config(text=f"Error: {str(e)}")
    finally:
        i2c.terminate()

def i2c_write():
    i2c_slave_str = i2c_slave_entry_write.get()
    i2c_reg_str = i2c_reg_entry_write.get()
    data_to_write_str = i2c_data_entry.get()  # Assuming there's an entry for data input
    board_add_val = board_add_write.get()
    try:
        slave_addr = int(i2c_slave_str, 16)
        register_addr = int(i2c_reg_str, 16)
        data_to_write = [int(x, 16) for x in data_to_write_str.split()]  # Converting string of hex values to list of ints
    except ValueError:
        i2c_write_output_label.config(text="Invalid input")
        return

    i2c = I2cController()
    try:
        i2c.configure(board_add_val)
        slave = i2c.get_port(slave_addr)
        slave.write([register_addr] + data_to_write)
        i2c_write_output_label.config(text="Write successful")
    except Exception as e:
        i2c_write_output_label.config(text=f"Error: {str(e)}")
    finally:
        i2c.terminate()

# SPI Read Functionality (Placeholder - Implement your SPI logic)
def spi_read():
    spi_output_label.config(text="SPI Read function not implemented")

# Main GUI Setup
root = Tk()
root.geometry("600x400")

frame_container = Frame(root, width=600, height=200)
frame_container.pack(side="bottom", fill="x", expand=True)

frames = {}
options = ["UART READ", "UART WRITE", "I2C READ","I2C WRITE", "SPI READ"]

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

# I2C READ Frame Setup
frame3 = Frame(frame_container, width=600, height=200)
board_label=Label(frame3,text="enter the board address")
board_add=Entry(frame3)
bytes_label=Label(frame3, text="Enter number of bytes to read")
i2c_label = Label(frame3, text="I2C Read Parameters")
i2c_slave_label = Label(frame3, text="I2C Slave Address (hex):")
i2c_reg_label = Label(frame3, text="Register Address (hex):")
i2c_slave_entry = Entry(frame3)
i2c_reg_entry = Entry(frame3)
i2c_read_button = Button(frame3, text="Read I2C", command=i2c_read)
i2c_output_label = Label(frame3, text="No data read yet")
i2c_bytes=Entry(frame3)
i2c_label.pack()

board_label.pack()
board_add.pack()

bytes_label.pack()
i2c_bytes.pack()

i2c_slave_label.pack()
i2c_slave_entry.pack()
i2c_reg_label.pack()
i2c_reg_entry.pack()
i2c_read_button.pack()
i2c_output_label.pack()
frames["I2C READ"] = frame3

# I2C WRITE Frame Setup
frame5 = Frame(frame_container, width=600, height=200)
board_label_write = Label(frame5, text="Board Address:")
board_add_write = Entry(frame5)
i2c_label_write = Label(frame5, text="I2C Write Parameters")
i2c_slave_label_write = Label(frame5, text="I2C Slave Address (hex):")
i2c_reg_label_write = Label(frame5, text="Register Address (hex):")
i2c_data_label = Label(frame5, text="Data to Write (hex):")
i2c_slave_entry_write = Entry(frame5)
i2c_reg_entry_write = Entry(frame5)
i2c_data_entry = Entry(frame5)
i2c_write_button = Button(frame5, text="Write I2C", command=i2c_write)
i2c_write_output_label = Label(frame5, text="No data written yet")

i2c_label_write.pack()
board_label_write.pack()
board_add_write.pack()
i2c_slave_label_write.pack()
i2c_slave_entry_write.pack()
i2c_reg_label_write.pack()
i2c_reg_entry_write.pack()
i2c_data_label.pack()
i2c_data_entry.pack()
i2c_write_button.pack()
i2c_write_output_label.pack()
frames["I2C WRITE"] = frame5

# Update options list and drop menu to include I2C WRITE

# Ensure to place the new frame into the show() function and update accordingly


# SPI READ Frame Setup (Placeholder - Adjust according to your SPI setup)
frame4 = Frame(frame_container, width=600, height=200)
spi_label = Label(frame4, text="SPI Read Data")
spi_read_button = Button(frame4, text="Read SPI", command=spi_read)
spi_output_label = Label(frame4, text="No data read yet")
spi_label.pack()
spi_read_button.pack()
spi_output_label.pack()
frames["SPI READ"] = frame4

clicked = StringVar()
clicked.set(options[0])  # Default set to first option

drop = OptionMenu(root, clicked, *options)
drop.pack()

button = Button(root, text="Select", command=show)
button.pack()

root.mainloop()
