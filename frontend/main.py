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

frame_container = Frame(root, width=600, height=200)
frame_container.pack(side="bottom", fill="x", expand=True)

# Create a dictionary to hold the frames
frames = {}
options = ["UART Read", "UART Write", "I2C", "SPI"]
# for option in options:


frame1 = Frame(frame_container, width=600, height=200)
# Add a label or any widgets you need inside this frame
label = Label(frame1, text="UART Read")
label.pack()
frames["UART Read"] = frame1


frame2 = Frame(frame_container, width=600, height=200)
# Add a label or any widgets you need inside this frame
label = Label(frame2, text="UART Write")
label.pack()
frames["UART Write"] = frame2


frame3 = Frame(frame_container, width=600, height=200)
# Add a label or any widgets you need inside this frame
label = Label(frame3, text="I2C")
label.pack()
frames["I2C"] = frame3


frame4 = Frame(frame_container, width=600, height=200)
# Add a label or any widgets you need inside this frame

in1= Entry(frame_container)
in1.pack()
label = Label(frame4, text="SPI")
label.pack()
frames["SPI"] = frame4





# Dropdown menu text variable
clicked = StringVar()
clicked.set(options[0])  # Default set to first option or use "Select an option"

# Create the Dropdown menu
drop = OptionMenu(root, clicked, *options)
print(drop)
drop.pack()

# Create the button that changes the displayed frame
button = Button(root, text="Click Me", command=show)
print(button)
button.pack()

# Start the Tkinter loop
root.mainloop()