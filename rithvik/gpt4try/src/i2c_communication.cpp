#include <iostream>
#include <windows.h>
#include "ftd2xx.h"
#include "libMPSSE_i2c.h"

int main() {
    FT_STATUS status = FT_OK;
    FT_HANDLE handle;
    DWORD channels = 0;
    DWORD i2cChannel = 0; // Assuming the first channel is used
    DWORD deviceAddress = 0x28; // Example I2C address, change as needed
    unsigned char writeData[] = {0x00, 0x00, 0xFF}; // Example data to write
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

    I2C_CloseChannel(handle);
    Cleanup_libMPSSE();
    std::cout << "Operation completed.\n";
    return 0;
}
