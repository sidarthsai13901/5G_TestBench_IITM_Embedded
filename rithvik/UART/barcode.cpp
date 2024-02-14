#include <stdio.h>
#include <stdlib.h>
#include "FTD2XX.H" 

FT_STATUS ftStatus;
FT_HANDLE ftHandle;
FT_DEVICE_LIST_INFO_NODE *devInfo;
DWORD numDevs;
DWORD Flags;
DWORD ID;
DWORD Type;
char SerialNumber[16];
char Description[64];
DWORD lComPortNumber;

// Data to be written
const char dataToWrite []= "Hello from the device!";
DWORD bytesToWrite = strlen(dataToWrite); 

int main (void) {

    ftStatus = FT_CreateDeviceInfoList(&numDevs);

    if (ftStatus == FT_OK) {
        printf("Found %d device", numDevs);
        if (numDevs > 1 || numDevs == 0) {
            printf("s:\n");
        } else {
            printf(":\n");
        }
    }

    if (numDevs > 0) {
        devInfo = (FT_DEVICE_LIST_INFO_NODE*)malloc(sizeof(FT_DEVICE_LIST_INFO_NODE)*numDevs);
        ftStatus = FT_GetDeviceInfoList(devInfo,&numDevs);
        if (ftStatus == FT_OK) {
            for (int i = 0; i < numDevs; i++) {
                printf("Device %d:\n",i);
                printf("   Flags=0x%x\n",devInfo[i].Flags);
                printf("   Type=0x%x\n",devInfo[i].Type);
                printf("   ID=0x%x\n",devInfo[i].ID);
                printf("   SerialNumber=%s\n",devInfo[i].SerialNumber);
                printf("   Description=%s\n",devInfo[i].Description);
            }
        }
    }

    // Open the first available device
    ftStatus = FT_Open(1,&ftHandle);
    if (ftStatus != FT_OK) {
        printf("FT_Open failed with error %d\n", ftStatus);
        return 1;  // Exit on error
    }

    ftStatus = FT_SetBaudRate(ftHandle, 9600); // Set baud rate to 115200
    if (ftStatus != FT_OK) {
        printf("FT_SetBaudRate Failed with error %d\n", ftStatus);
        FT_Close(ftHandle);
        return 1;
    }

    ftStatus = FT_GetComPortNumber(ftHandle,&lComPortNumber);
    if (ftStatus != FT_OK) {
        printf("FT_GetComPortNumber FAILED! with error %d\n", ftStatus);
        FT_Close(ftHandle);
        return 1;
    } else if (lComPortNumber == -1) {
        printf("No COM port assigned\n");
    } else {
        printf("COM port assigned with number %ld\n", lComPortNumber);
    }

    // ----- Writing Data -----
    DWORD bytesWritten;
    ftStatus = FT_Write(ftHandle, dataToWrite, bytesToWrite, &bytesWritten);
    if (ftStatus != FT_OK) {
        printf("FT_Write failed with error %d\n", ftStatus);
        FT_Close(ftHandle);
        return 1;
    } else if (bytesWritten != bytesToWrite) {
        printf("FT_Write failed: Not all bytes were written\n");
        FT_Close(ftHandle);
        return 1;
    } else {
        printf("Data written successfully!\n");
    }

    // ----- Reading Data -----
    DWORD rxBytesAvailable;
    DWORD bytesReceived;
    char rxBuffer[256]; // Assume a maximum of 256 bytes to read

    do {
        ftStatus = FT_GetStatus(ftHandle, &rxBytesAvailable, &TxBytes, &EventDWord);
        if (ftStatus != FT_OK) {
            printf("FT_GetStatus failed with error %d\n", ftStatus);
            break;
        }

        if (rxBytesAvailable > 0) {
            ftStatus = FT_Read(ftHandle, rxBuffer, rxBytesAvailable, &bytesReceived);
            if (ftStatus != FT_OK) {
                printf("FT_Read failed with error %d\n", ftStatus);
                break;
            }

            rxBuffer[bytesReceived] = '\0'; // Null-terminate for safety
            printf("Received data: %s\n", rxBuffer);
        }

    } while (rxBytesAvailable > 0);

    FT_Close(ftHandle);
    return 0; 
} 
