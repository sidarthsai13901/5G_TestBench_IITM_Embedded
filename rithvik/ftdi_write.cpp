#include <iostream>
#include <string>
#include <windows.h> // Required for Sleep()
#include "FTD2XX.H"

int main() {
  FT_STATUS ftStatus;
  FT_HANDLE ftHandle;

  // Data to send
  const char* dataToWrite = "Hello from FTDI (Windows)!";

  // Buffer for received data (if you expect a response)
  char readBuffer[256];
  DWORD bytesRead = 0;

  // 1. Open the FTDI device (update VID/PID as needed)
  ftStatus = FT_Open(0, &ftHandle); // Use device index 0 (might need to adjust)
  // which port or which ftdi device?
  if (ftStatus != FT_OK) {
    std::cerr << "Error opening FTDI device: " << ftStatus << std::endl;
    return 1;
  }

  // 2. Configure the device - optional (adjust baud rate if needed)
  ftStatus = FT_SetBaudRate(ftHandle, 115200);
  if (ftStatus != FT_OK) {
    std::cerr << "Error setting baud rate: " << ftStatus << std::endl;
    FT_Close(ftHandle);
    return 1;
  }

  // 3. Write data to the device
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

  // 5. Close the FTDI device
  FT_Close(ftHandle);
  return 0;
}
 