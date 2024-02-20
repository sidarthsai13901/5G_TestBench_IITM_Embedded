#include <stdio.h>
#include <stdlib.h>
#include <stdint.h> // Include this header
#include "ftd2xx.h"
#include "libMPSSE_i2c.h"
#include <windows.h>

#define I2C_DEVICE_ADDRESS 0x40 // Change this to your I2C device address
#define I2C_CLOCK_RATE 9600 // This should probably be higher, like 100000 for standard 100kHz I2C clock

int main() {
    FT_STATUS status = FT_OK;
    FT_HANDLE ftHandle;
    ChannelConfig channelConf;
    uint8_t address = I2C_DEVICE_ADDRESS; // Use uint8_t here
    uint8_t data[] = { 'h', 'e', 'l', 'l', 'o', 0 }; // Define as byte array, not string
    uint32_t channels = 0; // Use uint32_t here
    uint32_t bytesWritten = 0; // Use uint32_t here

    // Initialize the MPSSE for I2C communication
    Init_libMPSSE();

    status = I2C_GetNumChannels(&channels);
    if (status != FT_OK || channels == 0) {
        printf("Failed to get number of channels (status=%d, channels=%u)\n", status, channels);
        return 1;
    }

    // Open the first available channel
    status = I2C_OpenChannel(0, &ftHandle);
    if (status != FT_OK) {
        printf("Failed to open channel (status=%d)\n", status);
        return 1;
    }

    // Configure the I2C channel
    channelConf.ClockRate = I2C_CLOCK_RATE;
    channelConf.LatencyTimer = 2;
    channelConf.Options = I2C_DISABLE_3PHASE_CLOCKING;
    status = I2C_InitChannel(ftHandle, &channelConf);
    if (status != FT_OK) {
        printf("Failed to initialize channel (status=%d)\n", status);
        return 1;
    }

    // Write "hello" to the I2C device
    status = I2C_DeviceWrite(ftHandle, address, sizeof(data) - 1, data, &bytesWritten, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
    if (status != FT_OK) {
        printf("Failed to write data to device (status=%d)\n", status);
    } else {
        printf("Wrote %u bytes to device\n", bytesWritten); // Use %u for unsigned int format specifier
    }

    // Close the channel
    status = I2C_CloseChannel(ftHandle);
    if (status != FT_OK) {
        printf("Failed to close channel (status=%d)\n", status);
    }

    Cleanup_libMPSSE();
    return 0;
}
