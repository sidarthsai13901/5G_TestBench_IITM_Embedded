#include<windows.h>
#include<stdio.h>

int main()
{
    HANDLE hComm;
    BOOL Status;
    DCB dcbSerialParams={0};
    COMMTIMEOUTS timeouts={0};
    char SerialBuffer[64]={0};
    DWORD BytesWritten=0;
    DWORD dWEventMask;
    char ReadData;
    DWORD NoBytesRead;
    wchar_t PortNo[20]={L"COM7"};
    int loopCounter=1;

    printf("USB_COM7\n\n");

    hComm = CreateFileW(PortNo, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
    if(hComm == INVALID_HANDLE_VALUE)
    {
        printf("Could not open serial port");
        return 0;
    }
    else
    {
        printf("Serial port open\n");
    }

    // Set serial port parameters
    dcbSerialParams.DCBlength = sizeof(dcbSerialParams);
    Status = GetCommState(hComm, &dcbSerialParams);

    if (!Status)
    {
        printf("Error in GetCommState\n");
        CloseHandle(hComm);
        return 0;
    }

    dcbSerialParams.BaudRate = CBR_9600;  // Set your desired baud rate
    dcbSerialParams.ByteSize = 8;         // 8 bits per byte
    dcbSerialParams.StopBits = ONESTOPBIT; // 1 stop bit
    dcbSerialParams.Parity = NOPARITY;     // No parity

    Status = SetCommState(hComm, &dcbSerialParams);
    if (!Status)
    {
        printf("Error in SetCommState\n");
        CloseHandle(hComm);
        return 0;
    }

    // Set timeouts
    timeouts.ReadIntervalTimeout = MAXDWORD;
    timeouts.ReadTotalTimeoutConstant = 0;
    timeouts.ReadTotalTimeoutMultiplier = 0;
    timeouts.WriteTotalTimeoutConstant = 0;
    timeouts.WriteTotalTimeoutMultiplier = 0;

    Status = SetCommTimeouts(hComm, &timeouts);
    if (!Status)
    {
        printf("Error in SetCommTimeouts\n");
        CloseHandle(hComm);
        return 0;
    }

    // Writing data to the serial port
     char writeData[] = "Hello, USB device!";


    Status = WriteFile(hComm, writeData, sizeof(writeData), &BytesWritten, NULL);
    

    if (Status)
    {
        printf("Data written successfully %s\n",writeData);
    }
    else
    {
        printf("Error writing data to the serial port\n");
    }

    // Reading data from the serial port
    Status = ReadFile(hComm, &ReadData, sizeof(ReadData), &NoBytesRead, NULL);

    if (Status)
    {
        printf("Data read successfully: %s\n", ReadData);
    }
    else
    {
        printf("Error reading data from the serial port\n");
    }

    CloseHandle(hComm);

    return 0;
}

