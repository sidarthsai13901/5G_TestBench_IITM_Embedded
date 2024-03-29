// ft2232spi.cpp : Defines the entry point for the console application.
//

#ifdef _WIN32
#include "stdafx.h"
#endif

/* Standard C libraries */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <iostream>
#include "libMPSSE_spi.h"

// #include "libMPSSE.lib"
/* OS specific libraries */
#ifdef _WIN32
#include <windows.h>
#pragma comment(lib, "ftd2xx.lib")
#pragma comment(lib, "libMPSSE.lib")
#else
#include <unistd.h>
#define Sleep sleep
#endif

/* Include D2XX header*/
#include "FTD2XX.H"

/* Include libMPSSE header */
#include "libMPSSE_spi.h"

/* Helper macros */

#define APP_CHECK_STATUS(exp)                              \
	{                                                      \
		if (exp != FT_OK)                                  \
		{                                                  \
			printf("%s:%d:%s(): status(0x%x) \
!= FT_OK\n",                                               \
				   __FILE__, __LINE__, __FUNCTION__, exp); \
			exit(1);                                       \
		}                                                  \
		else                                               \
		{                                                  \
			;                                              \
		}                                                  \
	};
#define CHECK_NULL(exp)                               \
	{                                                 \
		if (exp == NULL)                              \
		{                                             \
			printf("%s:%d:%s():  NULL expression \
encountered \n",                                      \
				   __FILE__, __LINE__, __FUNCTION__); \
			exit(1);                                  \
		}                                             \
		else                                          \
		{                                             \
			;                                         \
		}                                             \
	};

/* Definitions */
#define PROG_BUFFER_SIZE 4000000
#define SPI_DEVICE_BUFFER_SIZE 256
#define SPI_WRITE_COMPLETION_RETRY 100
#define SPI_OPTS SPI_TRANSFER_OPTIONS_SIZE_IN_BYTES | SPI_TRANSFER_OPTIONS_CHIPSELECT_ENABLE | SPI_TRANSFER_OPTIONS_CHIPSELECT_DISABLE
#define GPIO_INIT GPIO_DIR /* Everything that's an output should be set high */

using namespace std;

void printUsage()
{
	printf("spi-prog <programming file> [--chan #] [--cs {3,4,5,6,7}] [--mode {1,2,3,4}]\r\n\t--chan Specifies the channel to use, default 0\r\n\t--cs specifies the chip select line on the FT2232, default 4\r\n\t--mode Specifies the SPI mode\r\n");
}

char *getOpt(const string &flag, const bool arg, char *args[], const int argc)
{
	for (int i = 0; i < argc; ++i)
	{
		if (flag.compare(args[i]) == 0)
		{
			if (arg)
			{
				if (i < (argc - 1))
					return args[i + 1];
				else
					continue;
			}
			else
				return args[i];
		}
	}
	return NULL;
}

void userPause()
{
#ifdef _WIN32
	system("pause");
#else
	char key;
	printf("Press any key to continue...\r\n");
	fgets(&key, 1, stdin);
#endif
}

int main(int argc, char *argv[])
{
	FT_HANDLE ftHandle;
	uint8 *wBuffer = NULL;
	FILE *fileHandle;
	size_t fileSize;
	FT_STATUS status = FT_OK;
	ChannelConfig channelConf = {0};
	uint32 chipSelect = SPI_CONFIG_OPTION_CS_DBUS4;
	uint32 spiMode = SPI_CONFIG_OPTION_MODE0;
	string filePathName;
	char *arg;
	uint32 channels = 0;
	uint32 channelToOpen = 0;
	uint32 sizeTransferred;

	if ((argc < 2) || getOpt("-h", false, argv, argc))
	{
		printUsage();
		exit(0);
	}

	string wFPN = string(argv[1]);
	filePathName = string(wFPN.begin(), wFPN.end()); // This is a dumb convert that will fail on non ASCII file path name input

	arg = getOpt("--chan", true, argv, argc);
	if (arg)
	{
		channelToOpen = atoi(arg);
	}

	arg = getOpt("--cs", true, argv, argc);
	if (arg)
	{
		const int csNum = atoi(arg);
		switch (csNum)
		{
		case 3:
			chipSelect = SPI_CONFIG_OPTION_CS_DBUS3;
			break;
		case 4:
			chipSelect = SPI_CONFIG_OPTION_CS_DBUS4;
			break;
		case 5:
			chipSelect = SPI_CONFIG_OPTION_CS_DBUS5;
			break;
		case 6:
			chipSelect = SPI_CONFIG_OPTION_CS_DBUS6;
			break;
		case 7:
			chipSelect = SPI_CONFIG_OPTION_CS_DBUS7;
			break;
		default:
			printf("Invalid chip select %d, must be 3-7\r\n", csNum);
			exit(1);
		}
	}

	arg = getOpt("--mode", true, argv, argc);
	if (arg)
	{
		const int modeNum = atoi(arg);
		switch (modeNum)
		{
		case 0:
			spiMode = SPI_CONFIG_OPTION_MODE0;
			break;
		case 1:
			spiMode = SPI_CONFIG_OPTION_MODE1;
			break;
		case 2:
			spiMode = SPI_CONFIG_OPTION_MODE2;
			break;
		case 3:
			spiMode = SPI_CONFIG_OPTION_MODE3;
			break;
		default:
			printf("Invalid mode number %d specified, must be 0-3\r\n", modeNum);
			exit(1);
		}
	}

	channelConf.ClockRate = 3000000;
	channelConf.LatencyTimer = 255;
	channelConf.configOptions = spiMode | chipSelect | SPI_CONFIG_OPTION_CS_ACTIVELOW;
	channelConf.Pin = 0x80B080B0; // FinalVal-FinalDir-InitVal-InitDir (for dir 0=in, 1=out). Magic number to make lattice on ultra breakout board work
	channelConf.reserved = 0;

	/* init library */
#ifdef _MSC_VER
	Init_libMPSSE();
#endif
	status = SPI_GetNumChannels(&channels);
	APP_CHECK_STATUS(status);

	if (channels < channelToOpen)
	{
		printf("Channel %d not available, only %d channels detected\r\n", channelToOpen, channels);
		exit(1);
	}

	/* Open the first available channel */
	status = SPI_OpenChannel(channelToOpen, &ftHandle);
	APP_CHECK_STATUS(status);

	printf("Opened channel %d\r\n", channelToOpen);

	channelConf.Pin = 0x80B080B0; // Reset the IOs
	status = SPI_InitChannel(ftHandle, &channelConf);
	APP_CHECK_STATUS(status);
	Sleep(1);
	status = SPI_CloseChannel(ftHandle);
	APP_CHECK_STATUS(status);
	printf("Put the chip into programming mode\r\n");
	userPause();

	status = SPI_OpenChannel(channelToOpen, &ftHandle);
	channelConf.Pin = 0xF0B0F0B0; // Reset the IOs

	status = SPI_InitChannel(ftHandle, &channelConf);
	APP_CHECK_STATUS(status);

	fileHandle = fopen(filePathName.c_str(), "rb");
	if (fileHandle == NULL)
	{
		printf("Couldn't open programming file \"%s\"\r\n", filePathName.c_str());
		exit(1);
	}
	fseek(fileHandle, 0, SEEK_END);
	fileSize = ftell(fileHandle);
	printf("Programming file is %ld bytes\r\n", fileSize);
	fseek(fileHandle, 0, SEEK_SET);

	wBuffer = new uint8[fileSize + 50];

	sizeTransferred = fread(wBuffer, sizeof(uint8), fileSize, fileHandle);
	if (sizeTransferred != fileSize)
	{
		printf("Didn't read full programming file %u < %ld\r\n", sizeTransferred, fileSize);
		exit(1);
	}
	for (int i = 0; i < 50; ++i)
		wBuffer[sizeTransferred++] = 0; // Add dummy bytes

	status = SPI_Write(ftHandle, wBuffer, sizeTransferred, &sizeTransferred, SPI_OPTS);
	APP_CHECK_STATUS(status);

	Sleep(50);

	status = SPI_CloseChannel(ftHandle);
	APP_CHECK_STATUS(status);

	delete wBuffer;

#ifdef _MSC_VER
	Cleanup_libMPSSE();
#endif

	return 0;
}
