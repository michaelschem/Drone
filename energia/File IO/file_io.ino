#include <WiFi.h>
#include <SLFS.h>

// just writing a text file to flash memory and reading it back

void setup()
{  
  char message[32] = "!-Hello World-!";
  int openok = -10;
  int filelengthWritten = -10;
  int readStatus = -10;
  
  Serial.begin(9600);

  // Initiate SimpleLink API and DMA channels
  SerFlash.begin();

  // Create new file, allocate 1024 bytes
  openok = SerFlash.open("myfile.txt", FS_MODE_OPEN_CREATE(1024, _FS_FILE_OPEN_FLAG_COMMIT));
  SerFlash.close();
  Serial.println("-----------------------------");
  Serial.print("File Created: ");
  Serial.println(openok);

  // Open file
  openok = SerFlash.open("myfile.txt", FS_MODE_OPEN_WRITE);
  Serial.print("File Opened: ");
  Serial.println(openok);
  // Write to file
  filelengthWritten = SerFlash.write(message);
  Serial.print("Length of and Message Written: ");
  Serial.print(filelengthWritten);
  Serial.print(" ");
  Serial.println(message);
  Serial.println("-----------------------------");
  // Close file
  SerFlash.close();

  // Open for reading, note that you will have to re-write file because it will be erased once you reopen it, or so I'm told
  readStatus = SerFlash.open("myfile.txt", FS_MODE_OPEN_READ);
  Serial.print("File Opened: ");
  Serial.println(readStatus);
  Serial.print("Message Read: ");
  // Create buffer
  char bffr;
  int n = 0;
  int next_byte = 0;
  do
  {
    next_byte = SerFlash.read();
    if (next_byte != -1)
    {
      bffr = (char)next_byte;
      Serial.print(bffr);
      n++; 
    }
  }
  while (next_byte != -1);
  SerFlash.close();
  Serial.println();
  Serial.println("-----------------------------");
}

void loop()
{
}

