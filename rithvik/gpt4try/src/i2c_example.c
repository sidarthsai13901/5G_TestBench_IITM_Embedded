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
        else
            printf("Opened the channel\n");

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
        else
            printf("Channel initialized\n");
        
        // Write to an I2C device
        UCHAR address = 0x6C;                // Device address
        UCHAR writeBuffer[] = {0x00, 0x01, 0x02}; // Data to write
        DWORD bytesToWrite = sizeof(writeBuffer); // Use DWORD directly
        DWORD bytesWritten = 0;                   // Use DWORD directly

        // status = I2C_DeviceWrite(ftHandle, address, bytesToWrite, writeBuffer, &bytesWritten, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
        // if (status != FT_OK)
        // {
        //     printf("Failed to write to the device\n");
        // }
        // else
        // {
        //     printf("Wrote %lu bytes\n", bytesWritten);
        // }

        // Read from an I2C device
        UCHAR readBuffer[16]; // Buffer for read data
        DWORD bytesToRead = sizeof(readBuffer);
        DWORD bytesRead = 0;

        status = I2C_DeviceRead(ftHandle, address, bytesToRead, readBuffer, &bytesRead, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT | I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE);
        if (status != FT_OK)
        {
            printf("Failed to read from the device\n");
        }
        else
        {
            printf("Read %lu bytes: ", bytesRead);
            for(DWORD i = 0; i < bytesRead; i++)
            {
                printf("%02X ", readBuffer[i]);
            }
            printf("\n");
        }

        // Close the channel
        I2C_CloseChannel(ftHandle);
    }

    Cleanup_libMPSSE();
    return 0;
}
