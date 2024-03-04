### UART Functions

#### 1. `uart_read()`
This function is designed to handle the reading of data from a UART interface. It operates as follows:

- It first retrieves the COM port and baud rate specified by the user through the GUI entries `com_port_entry_read` and `baud_rate_entry_read`.
- The function attempts to convert the baud rate from string to integer, displaying an error on the GUI if the conversion fails.
- It then tries to open a serial port using the `serial.Serial` class with the provided COM port and baud rate. If successful, it continuously reads data from this port in a loop until `stop_threads` is set to `True`.
- Data read from the serial port is decoded from bytes to a UTF-8 string and displayed in the GUI's `uart_read_output` label.
- If there are issues opening the serial port or during reading, an error is displayed in the GUI.
- The serial port is closed properly when exiting the function to avoid resource leaks.

#### 2. `start_uart_read()`
This function is a simple trigger for starting the UART read thread:

- It resets the `stop_threads` flag to `False`.
- It creates and starts a new daemon thread targeting the `uart_read` function, allowing the main program to exit even if the thread is running.

#### 3. `stop_uart_read()`
This function stops the UART reading process:

- It sets the `stop_threads` flag to `True`, which causes the loop in `uart_read` to terminate.
- It updates the GUI to indicate that UART reading has been stopped.

#### 4. `uart_write()`
This function handles sending data over UART:

- It collects the COM port and baud rate from the GUI, converting the baud rate to an integer.
- It retrieves the message to be sent from the `uart_write_entry` field, appending a newline character for transmission.
- It opens a serial connection using the provided parameters and sends the encoded message.
- It provides feedback in the GUI on the message sent or any errors encountered.
- It ensures the serial port is closed after the operation to prevent resource leaks.

### I2C Functions

#### 1. `i2c_read()`
This function is responsible for reading data from an I2C device:

- It retrieves the I2C slave address, register address, and the number of bytes to read from the GUI entries.
- These values are converted from strings to integers (with hexadecimal conversion for addresses).
- It initializes the `I2cController` and configures it with the specified board address.
- The function then communicates with the I2C device: it sends the register address and then reads the specified number of bytes from that address.
- The read data is displayed in the GUI's `i2c_output_label`.
- If any part of this process fails (e.g., due to invalid input or communication errors), an error message is displayed.
- Finally, it terminates the I2C controller to clean up resources.

These functions collectively provide the core functionality for interacting with UART and I2C interfaces through a GUI, allowing users to perform basic read and write operations on connected devices.



This script is a utility tool for scanning an I2C bus to detect slave devices using an FTDI-based USB to I2C converter. It uses the `pyftdi` library to communicate with the FTDI device and scan the I2C bus. Here's a detailed explanation of each part of the script:

### I2cBusScanner Class

1. **SMB_READ_RANGE and HIGHEST_I2C_SLAVE_ADDRESS**: These constants define the range of addresses to scan in SMBus mode and the highest possible I2C address, respectively.

2. **scan Method**: The core method of the `I2cBusScanner` class, responsible for scanning the I2C bus.
   - It initializes an `I2cController` object and sets the log level for the `pyftdi.i2c` logger to ERROR to minimize noise.
   - The I2C controller is configured with the provided URL (which specifies how to access the FTDI device).
   - The method iterates over all possible I2C addresses up to the defined maximum. For each address:
     - It creates a port using `get_port(addr)`.
     - It attempts to read from the address (or just write an empty list if not in SMBus mode). If a device acknowledges the transaction, the address is considered active.
     - If an `I2cNackError` is caught, it means no device acknowledged at the current address, and the scan moves on to the next.
   - Finally, it terminates the I2C controller to clean up resources.

### Main Script

1. **Argument Parsing**: The script uses `argparse` to handle command-line arguments, allowing the user to specify the FTDI device URL, operation mode, verbosity, etc.

2. **Logging Configuration**: Depending on the verbosity level set by the user, the log level for the `pyftdi.i2c` logger is set to either DEBUG or ERROR. A stream handler is added to direct log messages to `stderr`.

3. **Custom Device Addition**: If the user provides custom VID:PID pairs with the `-P` option, these are added to the I2cController to allow communication with non-standard FTDI devices.

4. **Bus Scanning**: The script calls the `scan` method of `I2cBusScanner`, passing the device URL, SMBus mode flag, and clock mode force flag based on the parsed arguments.

This utility is particularly useful for debugging or setting up systems where the connected I2C devices are unknown or need to be verified. By scanning the bus, users can identify which devices are present and responsive before attempting more complex operations or configurations.
