from argparse import ArgumentParser
from logging import getLogger, StreamHandler, DEBUG, ERROR
from sys import stderr
from pyftdi.i2c import I2cController, I2cNackError
from pyftdi.misc import add_custom_devices

class I2cBusScanner:
    """Scan I2C bus to find slave devices."""
    SMB_READ_RANGE = list(range(0x30,0x60))
    HIGHEST_I2C_SLAVE_ADDRESS = 0x78

    @classmethod
    def scan(cls, url: str, smb_mode: bool = True, force: bool = False) -> list:
        i2c = I2cController()
        getLogger('pyftdi.i2c').setLevel(ERROR)
        i2c.configure(url)
        i2c.set_retry_count(1)
        i2c.force_clock_mode(force)

        for addr in range(cls.HIGHEST_I2C_SLAVE_ADDRESS + 1):
            port = i2c.get_port(addr)
            try:
                if smb_mode and addr in cls.SMB_READ_RANGE or not smb_mode:
                    port.read(0)
                else:
                    port.write([])
            except I2cNackError:
                continue

        i2c.terminate()

parser = ArgumentParser(description="I2C bus scanner utility.")
parser.add_argument('device', nargs='?', default='ftdi:///?', help='Serial port device name')
parser.add_argument('-S', '--no-smb', action='store_true', help='Use regular I2C mode')
parser.add_argument('-P', '--vidpid', action='append', help='Specify a custom VID:PID ID')
parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity')
parser.add_argument('-F', '--force', action='store_true', help='Force clock mode')
args = parser.parse_args()

loglevel = DEBUG if args.verbose else ERROR
getLogger('pyftdi.i2c').setLevel(loglevel)
getLogger('pyftdi.i2c').addHandler(StreamHandler(stderr))

if args.vidpid:
    add_custom_devices(I2cController, args.vidpid)
I2cBusScanner.scan(args.device, not args.no_smb, args.force)
