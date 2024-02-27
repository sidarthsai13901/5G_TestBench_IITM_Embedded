#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include<windows.h>
#include <vector>
#include <cstdlib>
#include "ftd2xx.h"
#include "libMPSSE_i2c.h"

int main() {
    FT_STATUS status = FT_OK;
    FT_HANDLE ftHandle = nullptr;
    ChannelConfig channelConf;
    DWORD channels = 0;
    DWORD bytesRead = 0;
    DWORD bytesToRead = 1; // Adjust based on how many bytes you want to read
    std::vector<unsigned char> readBuffer(bytesToRead);
    unsigned char slaveAddress = 0x0B ; // Change to your slave device's address
    unsigned char registerAddress = 0x0B; // Register address you want to read from

    // Initialize channel configuration
    channelConf.ClockRate = I2C_CLOCK_STANDARD_MODE; // Or I2C_CLOCK_FAST_MODE
    channelConf.LatencyTimer = 255;
    channelConf.Options = I2C_DISABLE_3PHASE_CLOCKING;

    // Initialize the MPSSE for I2C communication
    Init_libMPSSE();
    status = I2C_GetNumChannels(&channels);
    if (status != FT_OK) {
        std::cerr << "Failed to get number of channels. Status: " << status << std::endl;
        return 1;
    }

    if (channels > 0) {
        // Open the first available channel
        status = I2C_OpenChannel(0, &ftHandle);
        if (status != FT_OK) {
            std::cerr << "Failed to open I2C channel. Status: " << status << std::endl;
            return 1;
        }

        // Initialize the channel
        status = I2C_InitChannel(ftHandle, &channelConf);
        if (status != FT_OK) {
            std::cerr << "Failed to initialize I2C channel. Status: " << status << std::endl;
            return 1;
        }

        // // Write the register address to the slave device
        // // status = I2C_DeviceWrite(ftHandle, slaveAddress, 1, &registerAddress, &bytesRead, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_BREAK_ON_NACK);
        // // if (status != FT_OK || bytesRead != 1) {
        //     // std::cerr << "Failed to write register address. Status: " << status << std::endl;
        //     return 1;
        // }

        // Read from the specified register
        status = I2C_DeviceRead(ftHandle, slaveAddress, bytesToRead, readBuffer.data(), &bytesRead, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT | I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE);
        if (status != FT_OK) {
            std::cerr << "Failed to read from register. Status: " << status << std::endl;
            return 1;
        }

        // Print the read data
        std::cout << "Data read from register 0x" << std::hex << static_cast<int>(registerAddress) << ": ";
        for(DWORD i = 0; i < bytesRead; i++) {
            std::cout << "0x" << static_cast<int>(readBuffer[i]) << " ";
        }
        std::cout << std::endl;

        // Close the channel
        status = I2C_CloseChannel(ftHandle);
    }

    Cleanup_libMPSSE();
    return 0;
}
