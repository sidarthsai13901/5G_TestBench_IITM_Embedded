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
frame_container = Frame(root, width=    600, height=200)
frame_container.pack(side="bottom", fill="x", expand=True)


# Create a dictionary to hold the frames
frames = {}
options = ["UART READ", "UART WRITE", "I2C READ", "SPI READ"]
# for option in options:



#uart read
frame1 = Frame(frame_container, width=600, height=200)
# Add a label or any widgets you need inside this frame
label = Label(frame1, text="UART Read")

val= Entry(frame1)
label.pack()
val.pack()
frames["UART READ"] = frame1


#uart write
frame2 = Frame(frame_container, width=600, height=200)
# Add a label or any widgets you need inside this frame
label = Label(frame2, text="UART Write")
label.pack()
frames["UART WRITE"] = frame2



#i2c
frame3 = Frame(frame_container, width=600, height=200)
# Add a label or any widgets you need inside this frame
label = Label(frame3, text="I2C")
i2cslave=Entry(frame3)
regadd=Entry(frame3)
i2c_out=Label(frame3,text="OUTPUT")
i2c_out.pack()
label.pack()
i2cslave.pack()
regadd.pack()
frames["I2C READ"] = frame3


#spi
frame4 = Frame(frame_container, width=600, height=200)
# Add a label or any widgets you need inside this frame

in1= Entry(frame4)
in1.pack()
label = Label(frame4, text="SPI")
label.pack()
frames["SPI READ"] = frame4


# Dropdown menu text variable
clicked = StringVar()
clicked.set(options[0])  # Default set to first option or use "Select an option"

# Create the Dropdown menu
drop = OptionMenu(root, clicked, *options)
print(drop)
drop.pack()


# Create the button that changes the displayed frame
button = Button(root, text="Select", command=show)
print(button)
button.pack()

# Start the Tkinter loop
root.mainloop()