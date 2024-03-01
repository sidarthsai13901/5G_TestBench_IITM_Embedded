from tkinter import *
from pyftdi.i2c import I2cController

def i2c_read():
    slave_addr_str = i2c_slave_entry.get()
    register_addr_str = regadd_entry.get()

    # Convert the hexadecimal string inputs to integers
    try:
        slave_addr = int(slave_addr_str, 16)
        register_addr = int(register_addr_str, 16)

        i2c = I2cController()
        try:
            i2c.configure('ftdi://ftdi:232h:0:ff/1')
            slave = i2c.get_port(slave_addr)
            slave.write([register_addr], False)
            data = slave.read(2)
            i2c_out.config(text=f"Read from register {hex(register_addr)}: {str(hex(data[0]))+str(hex(data[1])[2:])}")
        except Exception as e:
            i2c_out.config(text=f"Error: {str(e)}")
        finally:
            i2c.terminate()
    except ValueError:
        i2c_out.config(text="Invalid input for slave or register address")


def show():
    for frame in frames.values():
        frame.pack_forget()
    frame = frames[clicked.get()]
    frame.pack(fill='both', expand=True)

# Create the main window
root = Tk()
root.geometry("600x400")

frame_container = Frame(root, width=600, height=200)
frame_container.pack(side="bottom", fill="x", expand=True)

frames = {}
options = ["UART READ", "UART WRITE", "I2C READ", "SPI READ"]

# I2C READ
frame3 = Frame(frame_container, width=600, height=200)
i2c_label = Label(frame3, text="I2C Read Parameters")
i2c_slave_label = Label(frame3, text="I2C Slave Address (hex)")
i2c_reg_label = Label(frame3, text="Register Address (hex)")
i2c_slave_entry = Entry(frame3)
regadd_entry = Entry(frame3)
i2c_read_button = Button(frame3, text="Read", command=i2c_read)  # Button to trigger i2c_read
i2c_out = Label(frame3, text="OUTPUT")
i2c_label.pack()
i2c_slave_label.pack()
i2c_slave_entry.pack()
i2c_reg_label.pack()
regadd_entry.pack()
i2c_read_button.pack()  # Packing the read button into the frame
i2c_out.pack()
frames["I2C READ"] = frame3

clicked = StringVar()
clicked.set(options[0])

drop = OptionMenu(root, clicked, *options)
drop.pack()

button = Button(root, text="Select", command=show)
button.pack()

root.mainloop()
