#include <stdio.h>
#include "FTD2XX.H"

#define SPI_CLOCK_DIVISOR   2 // Adjust as needed to set the SPI clock frequency
#define SPI_MODE            0x02 // SPI mode 0
#define SPI_CS              0x01 // Bitmask for CS pin (AD0) - adjust as needed


int main(void) {
    FT_HANDLE ftHandle;
    FT_STATUS ftStatus;

    // Open device by serial number or description
    ftStatus = FT_OpenEx((PVOID)"FTDIBUS0", FT_OPEN_BY_DESCRIPTION, &ftHandle);
    if (ftStatus != FT_OK) {
        printf("Failed to open device\n");
        return 1;
    }

    // Configure MPSSE for SPI
    ftStatus = FT_SetBitMode(ftHandle, 0x0, 0x02); // Enable MPSSE
    if (ftStatus != FT_OK) {
        printf("Failed to enable MPSSE\n");
        FT_Close(ftHandle);
        return 1;
    }

    // Set clock divisor for SPI
    ftStatus = FT_SetDivisor(ftHandle, SPI_CLOCK_DIVISOR);
    if (ftStatus != FT_OK) {
        printf("Failed to set clock divisor\n");
        FT_Close(ftHandle);
        return 1;
    }

    // Configure SPI mode
    ftStatus = FT_SetDataCharacteristics(ftHandle, 0x00, 0x00, SPI_MODE);
    if (ftStatus != FT_OK) {
        printf("Failed to set data characteristics\n");
        FT_Close(ftHandle);
        return 1;
    }

    // CS Low (assert CS)
    unsigned char chipSelectValue = 0x01; 

    ftStatus = FT_Write(ftHandle, &chipSelectValue, 1, NULL);
    if (ftStatus != FT_OK) {
        printf("Failed to assert CS\n");
        FT_Close(ftHandle);
        return 1;
    }

    // Transmit data (example: sending 0xAA)
    unsigned char TxData[] = {0xAA};
    DWORD BytesWritten;
    ftStatus = FT_Write(ftHandle, TxData, sizeof(TxData), &BytesWritten);
    if (ftStatus != FT_OK) {
        printf("Failed to write data\n");
        FT_Close(ftHandle);
        return 1;
    }

    // CS High (deassert CS)
    unsigned char SPI_CS_high = 0x00;
    ftStatus = FT_Write(ftHandle, &SPI_CS_high, 1, NULL);
    if (ftStatus != FT_OK) {
        printf("Failed to deassert CS\n");
        FT_Close(ftHandle);
        return 1;
    }

    // Close device
    FT_Close(ftHandle);

    return 0;
}
