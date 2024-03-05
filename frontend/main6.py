# I2C Write Functionality
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
options.append("I2C WRITE")
drop = OptionMenu(root, clicked, *options)
drop.pack()

# Ensure to place the new frame into the show() function and update accordingly
