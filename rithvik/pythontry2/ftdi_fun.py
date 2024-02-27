# Load the libraries
import ctypes
import Channel
libMPSSE = ctypes.cdll.LoadLibrary('./libmpsse.dll')
print('Loaded MPSSE library')
libD2XX = ctypes.cdll.LoadLibrary('./ftd2xx.dll')
print('Loaded D2XX library')

def status(ret_val):
    """Translate a FTD2XX FT_STATUS code into a human-readable string."""
    status_messages = {
        0: "FT_OK",
        1: "FT_INVALID_HANDLE",
        2: "FT_DEVICE_NOT_FOUND",
        3: "FT_DEVICE_NOT_OPENED",
        4: "FT_IO_ERROR",
        5: "FT_INSUFFICIENT_RESOURCES",
        6: "FT_INVALID_PARAMETER",
        7: "FT_INVALID_BAUD_RATE",
        # Add more mappings based on the ftd2xx.h definitions
        10: "FT_FAILED_TO_WRITE_DEVICE",
        # ...continue for other status codes
    }
    return status_messages.get(ret_val, f"Unknown error {ret_val}")












# list the channels available
print('Listing channels...')
libMPSSE.Init_libMPSSE()
channel_count = ctypes.c_int()
ret = libMPSSE.I2C_GetNumChannels(ctypes.byref(channel_count))
print(f'Found {channel_count.value} channels (status {status(ret)})')

# Open Channel B (index 0) for I2C
c = Channel('B', 0)
write_address = 0x04
mode = START_BIT | STOP_BIT | NACK_LAST_BYTE
channel_info = ChannelInfo()
print(f'Getting info for channel with index {c.index}...')
ret = libMPSSE.I2C_GetChannelInfo(c.index, ctypes.byref(channel_info))
print(f'Channel description: {channel_info.Description.decode()} (status {status(ret)})')
ret = libMPSSE.I2C_OpenChannel(c.index, ctypes.byref(c.handle))
print(f'Channel {c.name} opened with handle: 0x{c.handle.value:x} (status {status(ret)})')
channel_conf = ChannelConfig(400000, 25, 0) # 400KHz, 25ms latency timer, no options
ret = libMPSSE.I2C_InitChannel(c.handle, ctypes.byref(channel_conf))
print(f'InitChannel() {c.name} (status {status(ret)})')

# Open Channel A (index 1) for bit-bang
handle = ctypes.c_void_p()
ret = libD2XX.FT_Open(1, ctypes.byref(handle))
print(f'FT_Open() (status {status(ret)})')
# 9600 * 16 = 153600 bytes/sec, see FTDI AN_232R-01
ret = libD2XX.FT_SetBaudRate(handle, 9600);
print(f'FT_SetBaudRate() (status {status(ret)})')
# set all pins as inputs, 0x1 is async bit-bang mode
ret = libD2XX.FT_SetBitMode(handle, 0b00000000, 0x1);
print(f'FT_SetBitMode() (status {status(ret)})')

# Send a byte (0x42) over I2C
buf = ctypes.create_string_buffer(b'', 1)
buf[0] = 0x42
bytes_transfered = ctypes.c_int()
ret = libMPSSE.I2C_DeviceWrite(c.handle, write_address, len(buf), buf, ctypes.byref(bytes_transfered), mode)
print(f'Wrote {bytes_transfered.value} byte(s) (status {status(ret)})')

# Read a byte from the bit-bang pins
b = ctypes.c_ubyte()
ret = libD2XX.FT_GetBitMode(handle, ctypes.byref(b))
print(f'FT_GetBitMode() (status {status(ret)})')
print(f'Byte read: 0x{b.value:x} (0b{b.value:>08b})') # hopefully it's 0x42

# Close the channels
ret = libMPSSE.I2C_CloseChannel(c.handle)
print(f'CloseChannel() {c.name} (status {status(ret)})')
ret = libD2XX.FT_Close(handle)
print(f'FT_Close() (status {status(ret)})')
