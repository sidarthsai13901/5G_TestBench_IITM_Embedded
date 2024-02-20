#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <ftd2xx.h> 


int set_interface_attribs(int fd, int speed) {
  struct termios tty;

  if (tcgetattr(fd, &tty) < 0) {
    printf("Error from tcgetattr: %s\n", strerror(errno));
    return -1;
  }

  cfsetospeed(&tty, (speed_t)speed);
  cfsetispeed(&tty, (speed_t)speed);

  tty.c_cflag |= (CLOCAL | CREAD);    /* ignore modem controls */
  tty.c_cflag &= ~CSIZE;
  tty.c_cflag |= CS8;         /* 8-bit characters */
  tty.c_cflag &= ~PARENB;     /* no parity bit */
  tty.c_cflag &= ~CSTOPB;     /* 1 stop bit */
  tty.c_cflag &= ~CRTSCTS;    /* no hardware flowcontrol */

  /* setup for non-canonical mode */
  tty.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON);
  tty.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
  tty.c_oflag &= ~OPOST;

  /* fetch bytes as they become available */
  tty.c_cc[VMIN] = 1;
  tty.c_cc[VTIME] = 1;

  if (tcsetattr(fd, TCSANOW, &tty) != 0) {
    printf("Error from tcsetattr: %s\n", strerror(errno));
    return -1;
  }
  return 0;
}
int main() {
  char *portname = "/dev/ttyUSB0";
  int fd;
  DWORD bytesRead; // For FTDI Read

  FT_HANDLE ftHandle;
  FT_STATUS ftStatus = FT_Open(0, &ftHandle);
  if (ftStatus != FT_OK) {
      printf("Error opening FTDI device: %d\n", (int)ftStatus);
      return -1;
  }

  ftStatus = set_interface_attribs(ftHandle, B115200); 
  if (ftStatus != FT_OK) {
      printf("Error setting serial attributes\n");
      FT_Close(ftHandle);
      return -1;
  }

  char read_buffer[256]; 

  while (1) { 
      ftStatus = FT_Read(ftHandle, read_buffer, sizeof(read_buffer), &bytesRead);
      if (ftStatus == FT_OK && bytesRead > 0) {
          read_buffer[bytesRead] = '\0'; // Null-terminate
          printf("Data received: %s\n", read_buffer);
      } else if (ftStatus != FT_OK) {
          printf("Error reading from serial port\n");
      } 
  }

  FT_Close(ftHandle);
  return 0;
}
