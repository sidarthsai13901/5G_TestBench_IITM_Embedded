from sys import stderr  # Make sure this import is included

import sys
from argparse import ArgumentParser
from logging import getLogger, StreamHandler, DEBUG, ERROR
from io import StringIO
from pyftdi.i2c import I2cController
from pyftdi.misc import add_custom_devices

class I2cBusScanner:
    """Scan I2C bus to find slave devices."""
    SMB_READ_RANGE = list(range(0x30,0x60))
    HIGHEST_I2C_SLAVE_ADDRESS = 0x78

    @classmethod
    def scan(cls, url: str, smb_mode: bool = True, force: bool = False) -> list:
        urls = []
        i2c = I2cController()
        getLogger('pyftdi.i2c').setLevel(ERROR)

        # Redirect stdout to capture output URLs
        old_stdout = sys.stdout
        redirected_output = StringIO()
        sys.stdout = redirected_output

        i2c.configure(url)

        # Reset stdout
        sys.stdout = old_stdout

        # Extract URLs
        output = redirected_output.getvalue()
        for line in output.split('\n'):
            if line.startswith('  ftdi://'):
                urls.append(line.strip())

        i2c.set_retry_count(1)
        i2c.force_clock_mode(force)

        for addr in range(cls.HIGHEST_I2C_SLAVE_ADDRESS + 1):
            port = i2c.get_port(addr)
            try:
                if smb_mode and addr in cls.SMB_READ_RANGE or not smb_mode:
                    port.read(0)
                else:
                    port.write([])
            except:
                continue

        i2c.terminate()
        return urls

parser = ArgumentParser(description="I2C bus scanner utility.")
parser.add_argument('device', nargs='?', default='ftdi:///?', help='Serial port device name')
parser.add_argument('-S', '--no-smb', action='store_true', help='Use regular I2C mode')
parser.add_argument('-P', '--vidpid', action='append', help='Specify a custom VID:PID ID')
parser.add_argument('-v', '--verbose', action='count', default=0, help='Increase verbosity')
parser.add_argument('-F', '--force', action='store_true', help='Force clock mode')
args = parser.parse_args()

loglevel = DEBUG if args.verbose else ERROR
getLogger('pyftdi.i2c').setLevel(loglevel)
getLogger('pyftdi.i2c').addHandler(StreamHandler(sys.stderr))  # Corrected to sys.stderr

if args.vidpid:
    add_custom_devices(I2cController, args.vidpid)

# Capture and print URLs
urls = I2cBusScanner.scan(args.device, not args.no_smb, args.force)
print("Detected URLs:")
for url in urls:
    print(url)
