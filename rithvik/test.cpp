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
        devInfo =
(FT_DEVICE_LIST_INFO_NODE*)malloc(sizeof(FT_DEVICE_LIST_INFO_NODE)*numDevs);
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
}