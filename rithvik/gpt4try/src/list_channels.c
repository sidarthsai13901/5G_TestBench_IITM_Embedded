#include <stdio.h>
#include <stdlib.h>
#include "ftd2xx.h"
#include "libMPSSE_i2c.h"
#include <windows.h>

int main(void) {
    FT_STATUS status;
    DWORD numChannels;

    // Initialize the MPSSE library
    Init_libMPSSE();
    status = I2C_GetNumChannels(&numChannels);

    if (status == FT_OK) {
        printf("Number of available I2C channels: %lu\n", numChannels);
    } else {
        printf("Failed to get the number of I2C channels\n");
    }

    // Finalize the MPSSE library
    Cleanup_libMPSSE();

    return 0;
}
