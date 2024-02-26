#include <stdio.h>
#include <stdlib.h>
#include <windows.h> // Ensure this is included before FTD2XX and LibMPSSE headers
#include "ftd2xx.h"
#include "libMPSSE_i2c.h"

int main() {
    FT_STATUS status = FT_OK;
    FT_HANDLE handle;
    ChannelConfig config;
    DWORD channels = 0;
    DWORD i2cChannel = 0; // Typically, channel 0 is used for I2C

    // Initialize the MPSSE library
    Init_libMPSSE();
    printf("LibMPSSE initialized.\n");

    status = I2C_GetNumChannels(&channels);
    if (status != FT_OK || channels == 0) {
        fprintf(stderr, "No available channels found.\n");
        return 1;
    }

    // Configuration for the I2C channel
    config.ClockRate = I2C_CLOCK_STANDARD_MODE; // Or I2C_CLOCK_FAST_MODE
    config.LatencyTimer = 2;
    config.Options = I2C_DISABLE_3PHASE_CLOCKING;

    status = I2C_OpenChannel(i2cChannel, &handle);
    if (status != FT_OK) {
        fprintf(stderr, "Unable to open I2C channel.\n");
        return 1;
    }
    printf("I2C channel opened.\n");

    status = I2C_InitChannel(handle, &config);
    if (status != FT_OK) {
        fprintf(stderr, "Unable to initialize I2C channel.\n");
        return 1;
    }

    unsigned char deviceAddress = 0x6C; // Device address without shifting
    unsigned char registerAddress = 0x0B;
    unsigned char readBuffer[1]; // Assuming you want to read 1 byte
    DWORD bytesToTransfer = 1;
    DWORD bytesTransferred;

    // // Write the register address you want to read from
    // status = I2C_DeviceWrite(handle, deviceAddress << 1, bytesToTransfer, &registerAddress, &bytesTransferred, I2C_TRANSFER_OPTIONS_START_BIT);
    // if (status != FT_OK) {
    //     fprintf(stderr, "Failed to write register address.\n");
    //     return 1;
    // }

    // Read from the register
    status = I2C_DeviceRead(handle, 0x6C, bytesToTransfer, readBuffer, &bytesTransferred, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT | I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE);
    if (status != FT_OK) {
        fprintf(stderr, "Failed to read from register %d.\n",deviceAddress);
        return 1;
    }

    printf("Read from register 0x0B: 0x%02X\n", readBuffer[0]);

    // Cleanup
    I2C_CloseChannel(handle);
    Cleanup_libMPSSE();
    printf("Channel closed and library cleaned up.\n");

    return 0;
}
