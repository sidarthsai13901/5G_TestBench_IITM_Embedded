from tkinter import *
import serial
import threading
from pyftdi.i2c import I2cController
from customFTDI import Ftdi
# Global variable for UART reading thread control
stop_threads = False

def show():
    for frame in frames.values():
        frame.pack_forget()
    frame = frames[clicked.get()]
    frame.pack(fill='both', expand=True)


    
#Scan device url Functionality  
def scan_dev():
    lis1=Ftdi.show_devices()
    lis2=[]
    if len(lis2)==0:
        return ["no device found"]
    for i in lis1:
        lis2.append(i[0])
    return lis2

    
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
    slave_addr_str = i2c_slave_entry.get()
    print(slave_addr_str)
    register_addr_str = i2c_reg_entry.get()
    print(register_addr_str)
    bytes_num=i2c_bytes.get()
    print(bytes_num)
    board_add_val = slave_addr_var.get()

    # Convert the hexadecimal string inputs to integers
    try:
        slave_addr = int(slave_addr_str, 16)
        register_addr = int(register_addr_str, 16)

        i2c = I2cController()
        try:
            i2c.configure(board_add_val)
            slave = i2c.get_port(slave_addr)
            slave.write([register_addr], False)
            data = slave.read(int(bytes_num))
            str1=""
            for i in range(int(bytes_num)):
                # print(str(hex(data[i])))
                str1+=str(hex(data[i]))
            str1=str1.replace('0x','')
            res1="0x"+str1
            i2c_output_label.config(text=res1)
            

            # i2c_output_label.config(text=f"Read from register {hex(register_addr)}: {str(hex(data[0]))+str(hex(data[1])[2:])}")
        except Exception as e:
            i2c_output_label.config(text=f"Error: {str(e)}")
        finally:
            i2c.terminate()
    except ValueError:
        i2c_output_label.config(text="Invalid input for slave or register address")

    finally:
        i2c.terminate()

# def i2c_read():
#     i2c = I2cController()

#     i2c_slave_str = i2c_slave_entry.get()
#     i2c_reg_str = i2c_reg_entry.get()
#     bytes_num=i2c_bytes.get()
#     board_add_val = slave_addr_var.get()
#     print(board_add_val)
#     try:
        
#         i2c.configure(board_add_val)
#         slave = i2c.get_port(i2c_slave_str)
#         print(slave)
#         slave.write([i2c_reg_str], False)
#         data = slave.read(bytes_num)
#         print(data)
        # print(f"Read from register {hex(i2c_reg_str)}: {str(hex(data[0]))+str(hex(data[1])[2:])}")
    


    # i2c = I2cController()
    # try:
    #     i2c.configure(board_add_val)  # Modify as needed
    #     slave = i2c.get_port(i2c_slave_str)
    #     slave.write([i2c_slave_str], False)
    #     data = slave.read(bytes_num)  # Modify based on expected data length
    #     print(bytes_num)
    #     i2c_output_label.config(text=f"Read: {data}")
    # except Exception as e:
    #     i2c_output_label.config(text=f"Error: {str(e)}")
    # finally:
    #     i2c.terminate()

#I2C Write functionality
def i2c_write():
    i2c_slave_str = i2c_slave_entry_write.get()
    i2c_reg_str = i2c_reg_entry_write.get()
    data_to_write_str = i2c_data_entry.get()  # Assuming there's an entry for data input
    board_add_val = scan_button2.get()
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
    


# spi needs:
        
        # mode : 0, 1, 2, 3   #the master and slave should be in the same mode to work, so maybe a dropdown

def spi_read():
    spi_output_label.config(text="SPI Read function not implemented")

# # Instantiate a SPI controller
# # We need want to use A*BUS4 for /CS, so at least 2 /CS lines should be
# # reserved for SPI, the remaining IO are available as GPIOs.
# spi = SpiController(cs_count=2)

# # Configure the first interface (IF/1) of the FTDI device as a SPI master
# spi.configure('ftdi://ftdi:2232h/1')

# # Get a port to a SPI slave w/ /CS on A*BUS4 and SPI mode 2 @ 10MHz
# slave = spi.get_port(cs=1, freq=10E6, mode=2)

# # Synchronous exchange with the remote SPI slave
# write_buf = b'\x01\x02\x03'
# read_buf = slave.exchange(write_buf, duplex=True)



#SPI Write











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


#get this function to run when the i2c option is selected in the main menu or the program wont work when we want to use a pure uart device without i2c

lis_board_add=scan_dev()
slave_addr_var = StringVar(root)

scan_button =OptionMenu(frame3,slave_addr_var,*lis_board_add)
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
scan_button.pack()


bytes_label.pack()
i2c_bytes.pack()

i2c_slave_label.pack()
i2c_slave_entry.pack()
i2c_reg_label.pack()
i2c_reg_entry.pack()
i2c_read_button.pack()
i2c_output_label.pack()
frames["I2C READ"] = frame3

# # I2C WRITE Frame Setup
# frame5 = Frame(frame_container, width=600, height=200)
# board_label=Label(frame5,text="enter the board address")
# board_add=Entry(frame5)
# bytes_label=Label(frame5, text="Enter number of bytes to read")
# i2c_label = Label(frame5, text="I2C Read Parameters")
# i2c_slave_label = Label(frame5, text="I2C Slave Address (hex):")
# i2c_reg_label = Label(frame3, text="Register Address (hex):")
# i2c_slave_entry = Entry(frame3)
# i2c_reg_entry = Entry(frame3)
# i2c_read_button = Button(frame3, text="Read I2C", command=i2c_read)
# i2c_output_label = Label(frame3, text="No data read yet")
# i2c_bytes=Entry(frame3)
# i2c_label.pack()

# board_label.pack()
# board_add.pack()

# bytes_label.pack()
# i2c_bytes.pack()

# i2c_slave_label.pack()
# i2c_slave_entry.pack()
# i2c_reg_label.pack()
# i2c_reg_entry.pack()
# i2c_read_button.pack()
# i2c_output_label.pack()
# frames["I2C READ"] = frame3



# I2C WRITE Frame Setup
frame5 = Frame(frame_container, width=600, height=200)
i2c_label_write = Label(frame5, text="I2C Write Parameters")
lis_board_add2=scan_dev()
slave_addr_var2= StringVar(root)
scan_button2 =OptionMenu(frame5,slave_addr_var2,*lis_board_add2)


i2c_slave_label_write = Label(frame5, text="I2C Slave Address (hex):")
i2c_reg_label_write = Label(frame5, text="Register Address (hex):")
i2c_data_label = Label(frame5, text="Data to Write (hex):")
i2c_slave_entry_write = Entry(frame5)
i2c_reg_entry_write = Entry(frame5)
i2c_data_entry = Entry(frame5)
i2c_write_button = Button(frame5, text="Write I2C", command=i2c_write)
i2c_write_output_label = Label(frame5, text="No data written yet")

i2c_label_write.pack()
scan_button2.pack()
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




######## Bitfield size depends on the FTDI device: 4432H series use 8-bit GPIO ports, while 232H and 2232H series use wide 16-bit ports.



# SPI READ Frame Setup (Placeholder - Adjust according to your SPI setup)
frame4 = Frame(frame_container, width=600, height=200)
spi_label = Label(frame4, text="SPI Read Data")
spi_read_button = Button(frame4, text="Read SPI", command=spi_read)
spi_output_label = Label(frame4, text="No data read yet")
spi_label.pack()
spi_read_button.pack()
spi_output_label.pack()
frames["SPI READ"] = frame4


#SPI WRITE








clicked = StringVar()
clicked.set(options[0])  # Default set to first option

drop = OptionMenu(root, clicked, *options)
drop.pack()

button = Button(root, text="Select", command=show)
button.pack()

root.mainloop()
