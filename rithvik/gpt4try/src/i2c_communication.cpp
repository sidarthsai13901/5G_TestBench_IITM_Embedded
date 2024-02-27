#include <iostream>
#include <windows.h>
#include "ftd2xx.h"
#include "libMPSSE_i2c.h"

int main() {
    FT_STATUS status = FT_OK;
    FT_HANDLE handle;
    // DWORD channels = 0;
    // DWORD i2cChannel = 0; // Assuming the first channel is used
    // DWORD deviceAddress = 0x28; // Example I2C address, change as needed
    unsigned char writeData[] = {0x00, 0x00, 0xFF}; // Example data to write
    unsigned long channels = 0;
    unsigned char i2cChannel = 0; // Assuming the first channel is used
    unsigned char deviceAddress = 0x6C << 1; // Device address for I2C, left shift for write operation
    unsigned char registerAddress = 0x0B; // Register address you want to read from
    unsigned char readData[2]; // Buffer for read data
    DWORD bytesWritten, bytesRead;

    Init_libMPSSE();
    std::cout << "LibMPSSE initialized.\n";

    status = I2C_GetNumChannels(&channels);
    if (status != FT_OK || channels == 0) {
        std::cerr << "Failed to get number of channels or no channels available.\n";
        return 1;
    }   
    std::cout << "Channels: " << channels << "\n";

    status = I2C_OpenChannel(i2cChannel, &handle);
    if (status != FT_OK) {
        std::cerr << "Unable to open I2C channel.\n";
        return 1;
    }
    std::cout << "Channel opened.\n";

    ChannelConfig config = {
        I2C_CLOCK_STANDARD_MODE,
        2,
        I2C_DISABLE_3PHASE_CLOCKING
    };

    status = I2C_InitChannel(handle, &config);
    if (status != FT_OK) {
        std::cerr << "Unable to initialize I2C channel.\n";
        I2C_CloseChannel(handle);
        return 1;
    }

    status = I2C_DeviceWrite(handle, deviceAddress, sizeof(writeData), writeData, &bytesWritten, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT);
    if (status == FT_OK) {
        std::cout << "Write successful, bytes written: " << bytesWritten << "\n";
    } else {
        std::cerr << "I2C write operation failed.\n";
    }

    // Add I2C_DeviceRead operation here if needed

    // // Write the register address to the device (without STOP bit to indicate a repeated start condition)
    // status = I2C_DeviceWrite(handle, deviceAddress, 1, &registerAddress, &bytesWritten, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_BREAK_ON_NACK);
    // if (status != FT_OK || bytesWritten != 1) {
    //     std::cerr << "Failed to write register address.\n";
    //     return 1;
    // }

    // Read from the specified register
    status = I2C_DeviceRead(handle, deviceAddress, sizeof(readData), readData, &bytesRead, I2C_TRANSFER_OPTIONS_START_BIT | I2C_TRANSFER_OPTIONS_STOP_BIT | I2C_TRANSFER_OPTIONS_NACK_LAST_BYTE);
    if (status != FT_OK) {
        std::cerr << "I2C read operation failed.\n";
        return 1;
    }

    // Output the read data
    std::cout << "Data read from register 0x" << std::hex << static_cast<int>(registerAddress) << ": ";
    for (unsigned long i = 0; i < bytesRead; ++i) {
        std::cout << "0x" << static_cast<int>(readData[i]) << " ";
    }
    std::cout << std::endl;

    // Close the channel and clean up
    I2C_CloseChannel(handle);
    Cleanup_libMPSSE();
    std::cout << "Operation completed.\n";
    return 0;
}

