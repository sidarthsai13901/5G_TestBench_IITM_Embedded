from argparse import ArgumentParser, FileType
from logging import Formatter, StreamHandler, getLogger, DEBUG, ERROR
from sys import modules, stderr
from traceback import format_exc
from pyftdi import FtdiLogger
from pyftdi.ftdi import Ftdi
from pyftdi.i2c import I2cController, I2cNackError
from pyftdi.misc import add_custom_devices


class I2cBusScanner:
    """Class to scan an I2C bus and detect slave devices."""

    SMB_READ_RANGE = list(range(0x30, 0x38)) + list(range(0x50, 0x60))
    HIGHEST_I2C_SLAVE_ADDRESS = 0x78

    @classmethod
    def scan(cls, url: str, smb_mode: bool = True, force: bool = False):
        """Scans an I2C bus to detect slave devices."""
        i2c = I2cController()
        slaves = []
        getLogger('pyftdi.i2c').setLevel(ERROR)
        i2c.set_retry_count(1)
        i2c.force_clock_mode(force)
        i2c.configure(url)

        for addr in range(cls.HIGHEST_I2C_SLAVE_ADDRESS + 1):
            port = i2c.get_port(addr)
            try:
                if smb_mode and addr in cls.SMB_READ_RANGE or not smb_mode:
                    port.read(0)
                    slaves.append('R')
                else:
                    port.write([])
                    slaves.append('W')
            except I2cNackError:
                slaves.append('.')

        i2c.terminate()

        # Display scan results
        columns = 16
        print('   %s' % ''.join(' %01X ' % col for col in range(columns)))
        for row in range(0, len(slaves), columns):
            chunk = slaves[row:row + columns]
            print(' %1X:' % (row // columns), '  '.join(chunk))


def main():
    """Main function to execute I2C bus scan."""
    parser = ArgumentParser(description=modules[__name__].__doc__)
    parser.add_argument('-P', '--vidpid', action='append', required=True,
                        help='specify custom VID:PID device ID, required')

    args = parser.parse_args()

    # Setup logger
    loglevel = ERROR  # Keep logging minimal, adjust as needed
    formatter = Formatter('%(message)s')
    FtdiLogger.log.addHandler(StreamHandler(stderr))
    FtdiLogger.set_formatter(formatter)
    FtdiLogger.set_level(loglevel)

    # This block is needed only if you are handling VID:PID pairs
    try:
        add_custom_devices(Ftdi, args.vidpid, force_hex=True)
    except ValueError as exc:
        parser.error(str(exc))

    # Assuming you need to call some function with the VID:PID pairs
    # For example, if you had a function to scan devices based on these IDs
    # scan_devices(args.vidpid)  # Hypothetical function

if __name__ == '__main__':
    main()
