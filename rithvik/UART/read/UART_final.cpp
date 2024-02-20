#include <stdio.h>
#include <stdlib.h>
#include "FTD2XX.h"

#define BUFFER_SIZE 128 // Define buffer size for read and write operations

FT_STATUS ftStatus;
FT_HANDLE ftHandle;

int main(void)
{
    DWORD BytesReceived;
    char RxBuffer[BUFFER_SIZE];

    // Open the first available FTDI device
    ftStatus = FT_Open(0, &ftHandle); // Adjust the device index if needed

    if (ftStatus == FT_OK)
    {
        printf("FT_Open succeeded.\n");

        // Set baud rate
        ftStatus = FT_SetBaudRate(ftHandle, 9600);
        if (ftStatus == FT_OK)
        {
            printf("FT_SetBaudRate succeeded.\n");

            // Main loop for reading
            while (1)
            {
                printf("Trying to read...\n");

                // Read data from the device
                ftStatus = FT_Read(ftHandle, RxBuffer, BUFFER_SIZE, &BytesReceived);
                if (ftStatus == FT_OK)
                {
                    if (BytesReceived > 0)
                    {
                        printf("FT_Read succeeded. Received %d bytes: %s\n", BytesReceived, RxBuffer);
                    }
                    else
                    {
                        printf("No data available.\n");
                    }
                }
                else
                {
                    printf("FT_Read failed with error code %d.\n", ftStatus);
                    break; // Exit the loop on error
                }
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
