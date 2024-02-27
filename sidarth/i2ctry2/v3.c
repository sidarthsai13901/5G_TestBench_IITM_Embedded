#include <stdio.h>
#include <stdlib.h>
#include "ftd2xx.h"
#include "libMPSSE_i2c.h"

int main() {
    FT_STATUS status = FT_OK;
    FT_DEVICE_LIST_INFO_NODE *devInfo = NULL;
    DWORD numDevs = 0;
    int i;
    FT_HANDLE ftHandle = NULL;

    // Initialize the MPSSE
    Init_libMPSSE();
    printf("LibMPSSE initialized.\n");

    status = FT_CreateDeviceInfoList(&numDevs);
    if (status != FT_OK) {
        printf("Failed to get the number of devices.\n");
        return 1;
    }
    printf("Number of devices is %d\n",numDevs);

    if (numDevs > 0) {
        // Allocate storage for device list
        devInfo = (FT_DEVICE_LIST_INFO_NODE*)malloc(sizeof(FT_DEVICE_LIST_INFO_NODE)*numDevs);
        status = FT_GetDeviceInfoList(devInfo,&numDevs);
        if (status == FT_OK) {
            for (i = 0; i < numDevs; i++) {
                printf("Dev %d:\n",i);
                printf(" Flags=0x%x\n",devInfo[i].Flags);
                printf(" Type=0x%x\n",devInfo[i].Type);
                printf(" ID=0x%x\n",devInfo[i].ID);
                printf(" LocId=0x%x\n",devInfo[i].LocId);
                printf(" SerialNumber=%s\n",devInfo[i].SerialNumber);
                printf(" Description=%s\n",devInfo[i].Description);
                printf(" ftHandle=0x%x\n",devInfo[i].ftHandle);
                // Check for a specific device by description, serial number, or location ID
                // For example, to open the first device (assuming it's the one you want to use):
                if (i == 0) { // Adjust this condition to match your specific device selection criteria
                    status = I2C_OpenChannel(i, &ftHandle);
                    if (status != FT_OK) {
                        printf("Failed to open channel %d.\n", i);
                        return 1;
                    }
                    printf("Channel %d opened.\n", i);
                    break; // Exit the loop once the desired device is opened
                }
            }
        }
        if (ftHandle == NULL) {
            printf("No suitable device found.\n");
            return 1;
        }
    } else {
        printf("No devices found.\n");
        return 1;
    }

    // Continue with the rest of your code here
    // For example, configuring the channel, communicating with the I2C device, etc.

    // Don't forget to free the device info list
    if (devInfo) free(devInfo);

    // Cleanup
    if (ftHandle != NULL) {
        I2C_CloseChannel(ftHandle);
    }
    Cleanup_libMPSSE();
    printf("Cleanup done.\n");

    return 0;
}
