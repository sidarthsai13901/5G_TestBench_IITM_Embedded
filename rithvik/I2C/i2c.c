#include <stdio.h>
#include "FTCI2C.h" // Include the FTCI2C header file
#include <windows.h>

#define I2C_DEVICE_ADDRESS 0x12 // Example I2C device address

int main() {
    // Initialize FTC library
    FTC_STATUS status = FTC_Initialize();

    if (status != FTC_SUCCESS) {
        printf("FTC library initialization failed\n");
        return 1;
    }

    // Open a device
    FTC_HANDLE handle;
    status = FTC_Open(0, &handle);

    if (status != FTC_SUCCESS) {
        printf("Failed to open device\n");
        FTC_Close(handle);
        return 1;
    }

    // Set the device mode
    status = FTC_SetMode(handle, 1);

    if (status != FTC_SUCCESS) {
        printf("Failed to set mode\n");
        FTC_Close(handle);
        return 1;
    }

    // Write data
    unsigned char data[] = {0x01, 0x02, 0x03}; // Example data to write
    DWORD bytesWritten;
    status = FTC_Write(handle, I2C_DEVICE_ADDRESS, data, sizeof(data), &bytesWritten);

    if (status != FTC_SUCCESS) {
        printf("Failed to write data\n");
        FTC_Close(handle);
        return 1;
    }

    // Close the device
    FTC_Close(handle);

    return 0;
}
