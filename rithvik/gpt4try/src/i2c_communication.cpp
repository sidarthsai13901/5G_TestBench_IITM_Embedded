#include <iostream>
#include <windows.h>
#include "ftd2xx.h"
#include "libMPSSE_i2c.h"

int main() {
    FT_STATUS status = FT_OK;
    FT_HANDLE handle;
    unsigned long channels = 0;
    unsigned char i2cChannel = 0; // Assuming the first channel is used
    unsigned char deviceAddress = 0x50; // Device address for I2C
    unsigned char writeData[] = {0x00, 0x00, 0xFF}; // Data to write
    unsigned char readData[2]; // Buffer for read data
    unsigned long bytesWritten, bytesRead;

    // Initialize the MPSSE library
    Init_libMPSSE();
    std::cout << "LibMPSSE initialized.\n";

    // Get the number of available I2C channels and check for availability
    status = I2C_GetNumChannels(&channels);
    if (status != FT_OK || channels == 0) {
        std::cerr << "Failed to get number of channels or no channels available.\n";
        return 1;
    }

    // Open the first I2C channel
    status = I2C_OpenChannel(i2cChannel, &handle);
    if (status != FT_OK) {
        std::cerr << "Unable to open I2C channel.\n";
        return 1;
    }

    // Configuration for the I2C channel
    ChannelConfig config = {
        I2C_CLOCK_STANDARD_MODE, // Clock rate
        2,                       // Latency timer
        I2C_DISABLE_3PHASE_CLOCKING // Options
    };

    // Initialize the channel with the configuration
    status = I2C_InitChannel(handle, &config);
    if (status != FT_OK) {
        std::cerr << "Unable to initialize I2C channel.\n";
        return 1;
    }

    // Write to the I2C device
    status = I2C_DeviceWrite(handle, deviceAddress, sizeof(writeData), writeData, &bytesWritten, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
    if (status != FT_OK) {
        std::cerr << "I2C write operation failed.\n";
        return 1;
    }

    // Read from the I2C device
    status = I2C_DeviceRead(handle, deviceAddress, sizeof(readData), readData, &bytesRead, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
    if (status != FT_OK) {
        std::cerr << "I2C read operation failed.\n";
        return 1;
    }

    // Close the channel and clean up
    I2C_CloseChannel(handle);
    Cleanup_libMPSSE();

    std::cout << "Operation completed successfully.\n";
    return 0;
}
