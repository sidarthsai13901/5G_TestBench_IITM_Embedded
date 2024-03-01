from tkinter import *

# Function to show the selected frame
def show():
    # Clear the current frame view
    for frame in frames.values():
        frame.pack_forget()

    # Display the selected frame
    frame = frames[clicked.get()]
    frame.pack(fill='both', expand=True)
    
# Create the main window
root = Tk()
root.geometry("600x400")

# Create a frame container in the bottom half of the window
frame_container = Frame(root, width=600, height=200)
frame_container.pack(side="bottom", fill="x", expand=True)

# Create a dictionary to hold the frames
frames = {}
options = ["UART READ", "UART WRITE", "I2C READ", "SPI READ"]

# UART READ
frame1 = Frame(frame_container, width=600, height=200)
uart_read_label = Label(frame1, text="UART Read Data")
uart_read_entry = Entry(frame1)
uart_read_label.pack()
uart_read_entry.pack()
frames["UART READ"] = frame1

# UART WRITE
frame2 = Frame(frame_container, width=600, height=200)
uart_write_label = Label(frame2, text="UART Write Data")
uart_write_entry = Entry(frame2)
uart_write_label.pack()
uart_write_entry.pack()
frames["UART WRITE"] = frame2

# I2C READ
frame3 = Frame(frame_container, width=600, height=200)
i2c_label = Label(frame3, text="I2C Read Parameters")
i2c_slave_label = Label(frame3, text="I2C Slave Address")
i2c_reg_label = Label(frame3, text="Register Address")
i2c_slave_entry = Entry(frame3)
i2c_reg_entry = Entry(frame3)
i2c_output_label = Label(frame3, text="OUTPUT")
i2c_label.pack()
i2c_slave_label.pack()
i2c_slave_entry.pack()
i2c_reg_label.pack()
i2c_reg_entry.pack()
i2c_output_label.pack()
frames["I2C READ"] = frame3

# SPI READ
frame4 = Frame(frame_container, width=600, height=200)
spi_read_label = Label(frame4, text="SPI Read Data")
spi_read_entry = Entry(frame4)
spi_read_label.pack()
spi_read_entry.pack()
frames["SPI READ"] = frame4

# Dropdown menu text variable
clicked = StringVar()
clicked.set(options[0])  # Default set to first option

# Create the Dropdown menu
drop = OptionMenu(root, clicked, *options)
drop.pack()

# Create the button that changes the displayed frame
button = Button(root, text="Select", command=show)
button.pack()

# Start the Tkinter loop
root.mainloop()
