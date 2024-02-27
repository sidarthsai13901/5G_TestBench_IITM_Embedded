import ctypes
from enum import Enum

class Channel():
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.handle = ctypes.c_void_p()

        
class ChannelConfig(ctypes.Structure):
    _fields_ = [('ClockRate', ctypes.c_int),
                ('LatencyTimer', ctypes.c_ubyte),
                ('Options', ctypes.c_int)]

    
class ChannelInfo(ctypes.Structure):
    _fields_ = [('Flags', ctypes.c_ulong),
                ('Type', ctypes.c_ulong),
                ('ID', ctypes.c_ulong),
                ('LocId', ctypes.c_ulong),
                ('SerialNumber', ctypes.c_char*16),
                ('Description', ctypes.c_char*64),
                ('ftHandle', ctypes.c_void_p)]
    
def __repr__(self):
        values = ', '.join(f'{name}={value}' for name, value in self._asdict().items())
        return f'<{self.__class__.__name__}: {values}>'
    
def _asdict(self):
        return {field[0]: getattr(self, field[0]) for field in self._fields_}
    
    
class FT_STATUS(Enum):
    FT_OK                             = 0
    FT_INVALID_HANDLE                 = 1
    FT_DEVICE_NOT_FOUND               = 2
    FT_DEVICE_NOT_OPENED              = 3
    FT_IO_ERROR                       = 4
    FT_INSUFFICIENT_RESOURCES         = 5
    FT_INVALID_PARAMETER              = 6
    FT_INVALID_BAUD_RATE              = 7
    FT_DEVICE_NOT_OPENED_FOR_ERASE    = 8
    FT_DEVICE_NOT_OPENED_FOR_WRITE    = 9
    FT_FAILED_TO_WRITE_DEVICE         = 10
    FT_EEPROM_READ_FAILED             = 11
    FT_EEPROM_WRITE_FAILED            = 12
    FT_EEPROM_ERASE_FAILED            = 13
    FT_EEPROM_NOT_PRESENT             = 14
    FT_EEPROM_NOT_PROGRAMMED          = 15
    FT_INVALID_ARGS                   = 16
    FT_NOT_SUPPORTED                  = 17
    FT_OTHER_ERROR                    = 18
    FT_DEVICE_LIST_NOT_READ           = 19
    
# Some constants for FTDI config...
START_BIT                   = 0x01
STOP_BIT                    = 0x02
BREAK_ON_NACK               = 0x04
NACK_LAST_BYTE              = 0x08
FAST_TRANSFER_BYTES         = 0x10
FAST_TRANSFER_BITS          = 0x20
FAST_TRANSFER               = 0x30
NO_ADDRESS                  = 0x40
I2C_DISABLE_3PHASE_CLOCKING = 0x01
I2C_ENABLE_DRIVE_ONLY_ZERO  = 0x02

def status(code):
    return FT_STATUS(code).name
