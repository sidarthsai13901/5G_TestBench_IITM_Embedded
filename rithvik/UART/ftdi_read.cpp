#include "ftd2xx.h"
#include <iostream>
#include <string>
#include <windows.h> // Required for Sleep()
#include "FTD2XX.H"

int main() {
    FT_HANDLE ftHandle;
    FT_STATUS ftStatus;
    DWORD RxBytes = 10;
    DWORD BytesReceived;
    char RxBuffer[256];

    // Open the FTDI device
    ftStatus = FT_Open(0, &ftHandle);
    if(ftStatus != FT_OK) {
        // FT_Open failed
        printf("FT_Open failed!\n");
        return 1;
    }

     // 2. Configure the device - optional (adjust baud rate if needed)
  ftStatus = FT_SetBaudRate(ftHandle, 9600);
  if (ftStatus != FT_OK) {
    std::cerr << "Error setting baud rate: " << ftStatus << std::endl;
    FT_Close(ftHandle);
    return 1;
  }

    // Set read timeouts (5 seconds timeout, 0 milliseconds polling interval)
    FT_SetTimeouts(ftHandle, 5000, 0);

    // Read data from the FTDI device
    ftStatus = FT_Read(ftHandle, RxBuffer, RxBytes, &BytesReceived);
    if (ftStatus == FT_OK) {
        if (BytesReceived == RxBytes) {
            // FT_Read successful
            printf("Read %d bytes successfully.\n", BytesReceived);
        }
        else {
            // FT_Read Timeout
            printf("Timeout while reading data.\n");
        }
    }
    else {
        // FT_Read Failed
        printf("FT_Read failed!\n");
    }

    // Close the FTDI device
    FT_Close(ftHandle);

    return 0;
}
