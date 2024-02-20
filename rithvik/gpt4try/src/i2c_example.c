#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include "ftd2xx.h"
#include "libMPSSE_i2c.h"

int main()
{
    FT_STATUS status = FT_OK;
    DWORD channels = 0; // Use DWORD directly
    FT_HANDLE ftHandle;

    // Initialize the MPSSE
    Init_libMPSSE();

    status = I2C_GetNumChannels(&channels);
    if (status != FT_OK)
    {
        printf("Failed to get the number of channels\n");
        return 1;
    }

    if (channels > 0)
    {
        // Open the first available channel
        status = I2C_OpenChannel(0, &ftHandle);
        if (status != FT_OK)
        {
            printf("Failed to open the channel\n");
            return 1;
        }

        // Configure the I2C channel
        ChannelConfig channelConf;
        channelConf.ClockRate = I2C_CLOCK_STANDARD_MODE; // Or use I2C_CLOCK_FAST_MODE
        channelConf.LatencyTimer = 2;
        channelConf.Options = I2C_DISABLE_3PHASE_CLOCKING;

        status = I2C_InitChannel(ftHandle, &channelConf);
        if (status != FT_OK)
        {
            printf("Failed to initialize the channel\n");
            return 1;
        }

        // Write to an I2C device
        UCHAR address = 0x50;                // Use UCHAR directly for address
        UCHAR buffer[] = {0x00, 0x01, 0x02}; // Data to write
        DWORD bytesToWrite = sizeof(buffer); // Use DWORD directly
        DWORD bytesWritten = 0;              // Use DWORD directly

        status = I2C_DeviceWrite(ftHandle, address, bytesToWrite, buffer, &bytesWritten, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
        printf("Operation status: %d\n", status); // Corrected line to print the status code
        if (status != FT_OK)
        {
            printf("Failed to write to the device\n");
        }
        else
        {
            printf("Wrote %lu bytes\n", bytesWritten); // Use %lu for DWORD
        }

        // Close the channel
        I2C_CloseChannel(ftHandle);
    }

    Cleanup_libMPSSE();
    return 0;
}
