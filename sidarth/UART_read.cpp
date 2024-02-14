#include <stdio.h>
#include <stdlib.h>
#include "FTD2XX.H"

#define BUFFER_SIZE 128 // Define buffer size for read and write operations

FT_STATUS ftStatus;
FT_HANDLE ftHandle;
FT_DEVICE_LIST_INFO_NODE *devInfo;
DWORD numDevs;
DWORD Flags;
DWORD ID;
DWORD Type;
char SerialNumber[16];
char Description[64];

int main(void)
{
    // Initialize FTDI devices
    ftStatus = FT_CreateDeviceInfoList(&numDevs);

    // if (ftStatus == FT_OK)
    // {
    //     printf("Found %d device", numDevs);
    //     if (numDevs > 1 || numDevs == 0)
    //     {
    //         printf("s:\n");
    //     }
    //     else
    //     {
    //         printf(":\n");
    //     }
    // }

    // if (numDevs > 0) {
    //     devInfo = (FT_DEVICE_LIST_INFO_NODE *)malloc(sizeof(FT_DEVICE_LIST_INFO_NODE) * numDevs);
    //     ftStatus = FT_GetDeviceInfoList(devInfo, &numDevs);
    //     if (ftStatus == FT_OK) {
    //         for (int i = 0; i < numDevs; i++) {
    //             printf("Device %d:\n", i);
    //             printf("   Flags=0x%x\n", devInfo[i].Flags);
    //             printf("   Type=0x%x\n", devInfo[i].Type);
    //             printf("   ID=0x%x\n", devInfo[i].ID);
    //             printf("   SerialNumber=%s\n", devInfo[i].SerialNumber);
    //             printf("   Description=%s\n", devInfo[i].Description);
    //         }
    //     }
    // }

    // Open the first available FTDI device
    ftStatus = FT_Open(2, &ftHandle);
    if (ftStatus == FT_OK)
    {
        printf("FT_Open succeeded.\n");

        // Set baud rate
        ftStatus = FT_SetBaudRate(ftHandle, 9600);
        if (ftStatus == FT_OK)
        {
            printf("FT_SetBaudRate succeeded.\n");

            // Data buffers for write and read
            char TxBuffer[] = "Hello from FTDssssssssssssssssssssssssssssssssssssssssssI!";
            char RxBuffer[BUFFER_SIZE];
            DWORD BytesWritten, BytesReceived;

            // Write data to the device
            // ftStatus = FT_Write(ftHandle, TxBuffer, sizeof(TxBuffer), &BytesWritten);
            // if (ftStatus == FT_OK)
            // {
            //     printf("FT_Write succeeded. Sent %d bytes.\n", BytesWritten);

                // Read data from the device
                // Read data from the device
                printf("Trying to read");
                ftStatus = FT_Read(ftHandle, RxBuffer, sizeof(RxBuffer), &BytesReceived);
                if (ftStatus == FT_OK)
                {
                    printf("FT_Read succeeded. Received %d bytes: %s\n", BytesReceived, RxBuffer);
                }
                else
                {
                    printf("FT_Read failed.\n");
                }
            }
            else
            {
                printf("FT_Write failed.\n");
            }
        }
        else
        {
            printf("FT_SetBaudRate failed.\n");
        }
    }
    else
    {
        printf("FT_Open failed.\n");
    }

    // Close the handle to the device
    FT_Close(ftHandle);

    return 0;
}
