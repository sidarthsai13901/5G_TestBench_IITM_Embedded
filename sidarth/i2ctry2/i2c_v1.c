#include <stdio.h>
#include <stdlib.h>
#include "ftd2xx.h"
#include <windows.h>
#include "libmpsse_i2c.h"

int main() {
    FT_STATUS status = FT_OK;
    FT_HANDLE ftHandle;
    ChannelConfig channelConf;
    DWORD numChannels = 0;
    unsigned char deviceAddress = 0x50; // Replace with your I2C device's address
    unsigned char registerAddress = 0x00; // Replace with the register you want to read
    unsigned char readData[1]; // Buffer to store the data read from the device
    DWORD bytesTransferred = 0;

    // Initialize the MPSSE
    Init_libMPSSE();
    printf("LibMPSSE initialized.\n");

    status = I2C_GetNumChannels(&numChannels);
    if (status != FT_OK) {
        printf("Failed to get the number of I2C channels.\n");
        return 1;
    }

    if (numChannels == 0) {
        printf("No I2C channels found.\n");
        return 1;
    }

    // Open the first available I2C channel
    status = I2C_OpenChannel(0, &ftHandle);
    if (status != FT_OK) {
        printf("Failed to open the I2C channel.\n");
        return 1;
    }
    printf("I2C channel opened.\n");

    // Configure the I2C channel
    channelConf.ClockRate = I2C_CLOCK_STANDARD_MODE;
    channelConf.LatencyTimer = 255;
    channelConf.Options = I2C_DISABLE_3PHASE_CLOCKING;
    status = I2C_InitChannel(ftHandle, &channelConf);
    if (status != FT_OK) {
        printf("Failed to initialize the I2C channel.\n");
        I2C_CloseChannel(ftHandle);
        return 1;
    }

    // Write the register address you want to read from
    status = I2C_DeviceWrite(ftHandle, deviceAddress, 1, &registerAddress, &bytesTransferred, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
    if (status != FT_OK) {
        printf("Failed to write the register address.\n");
        I2C_CloseChannel(ftHandle);
        return 1;
    }

    // Read from the register
    status = I2C_DeviceRead(ftHandle, deviceAddress, 1, readData, &bytesTransferred, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
    if (status != FT_OK) {
        printf("Failed to read from the device.\n");
        I2C_CloseChannel(ftHandle);
        return 1;
    }

    printf("Read data from register 0x%02X: 0x%02X\n", registerAddress, readData[0]);

    // Cleanup
    I2C_CloseChannel(ftHandle);
    Cleanup_libMPSSE();
    printf("Channel closed and MPSSE cleaned up.\n");

    return 0;
}
