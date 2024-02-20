#include <iostream>
#include <string>
#include <windows.h> // Required for Sleep()
#include "FTD2XX.H"
#include "ftd2xx.h"
#include <iostream>
#include <string>
#include <windows.h> // Required for Sleep()
#include "FTD2XX.H"

int main() {
  FT_STATUS ftStatus;
  FT_HANDLE ftHandle;

  // Data to send
  const char* dataToWrite = "10101";

  // Buffer for received data (if you expect a response)
  char readBuffer[256];
  DWORD bytesRead = 0;

  // 1. Open the FTDI device (update VID/PID as needed)
  ftStatus = FT_Open(2, &ftHandle); // Use device index 0 (might need to adjust)
  // which port or which ftdi device?
  if (ftStatus != FT_OK) {
    std::cerr << "Error opening FTDI device: " << ftStatus << std::endl;
    return 1;
  }

  // 2. Configure the device - optional (adjust baud rate if needed)
  ftStatus = FT_SetBaudRate(ftHandle, 9600);
  if (ftStatus != FT_OK) {
    std::cerr << "Error setting baud rate: " << ftStatus << std::endl;
    FT_Close(ftHandle);
    return 1;
  }

  // 3. Write data to the device

  while(1){
  DWORD bytesWritten = 0; // Use DWORD for Windows compatibility
  ftStatus = FT_Write(ftHandle, (LPVOID)dataToWrite, strlen(dataToWrite), &bytesWritten);
  if (ftStatus != FT_OK) {
    std::cerr << "Error writing to FTDI device: " << ftStatus << std::endl;
    FT_Close(ftHandle);
    return 1;  
  }
  std::cout << "Bytes written: " << bytesWritten << std::endl;
  
  // 4. Read data (optional - only if you expect a response)
  bytesRead = 0; // Reset bytesRead
  ftStatus = FT_Read(ftHandle, (LPVOID)readBuffer, sizeof(readBuffer), &bytesRead);
  if (ftStatus != FT_OK) {
    std::cerr << "Error reading from FTDI device: " << ftStatus << std::endl;
  } else {
    std::cout << "Bytes read: " << bytesRead << std::endl;
    std::cout << "Received data: " << readBuffer << std::endl;
  }
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
  // 5. Close the FTDI device
  FT_Close(ftHandle);
  return 0;
}
 