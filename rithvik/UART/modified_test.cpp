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

     ftStatus = FT_Open(0,&ftHandle);
        if (ftStatus == FT_OK) {
        // FT_Open OK, use ftHandle to access device
        }
else {
        // FT_Open failed
}
ftStatus = FT_SetBaudRate(ftHandle, 9600); // Set baud rate to 115200
if (ftStatus == FT_OK) {
// FT_SetBaudRate OK
}
else {
// FT_SetBaudRate Failed
}
ftStatus = FT_GetComPortNumber(ftHandle,&lComPortNumber);
if (ftStatus == FT_OK) {
if (lComPortNumber == -1) {
// No COM port assigned
}
else {
// COM port assigned with number held in lComPortNumber
}
}
else {
// FT_GetComPortNumber FAILED!
}
ftStatus = FT_Write(ftHandle, TxBuffer, sizeof(TxBuffer), &BytesWritten);
if (ftStatus == FT_OK) {
// FT_Write OK
}
else {
// FT_Write Failed
}
//FT_Close(ftHandle);/ FT_Open failed

FT_GetStatus(ftHandle,&RxBytes,&TxBytes,&EventDWord);
if (RxBytes > 0) {
ftStatus = FT_Read(ftHandle,RxBuffer,RxBytes,&BytesReceived);
if (ftStatus == FT_OK) {
// FT_Read OK
}
else {
// FT_Read Failed
}
}
FT_Close(ftHandle);
