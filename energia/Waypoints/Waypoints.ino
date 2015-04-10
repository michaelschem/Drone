#include <WiFi.h>
#include <SLFS.h>

// just writing a text file to flash memory and reading it back

void setup()
{  
  char waypoint_one[10] = "11223333\n";
  char waypoint_two[10] = "22334444\n";
  char waypoint_three[10] = "33445555\n";
  char waypoint_four[10] = "44556666\n";
  char waypoint_five[9] = "55667777";
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
  filelengthWritten = SerFlash.write(waypoint_one);
  filelengthWritten += SerFlash.write(waypoint_two);
  filelengthWritten += SerFlash.write(waypoint_three);
  filelengthWritten += SerFlash.write(waypoint_four);
  filelengthWritten += SerFlash.write(waypoint_five);  
  Serial.print("Length of Written: ");
  Serial.println(filelengthWritten);
  Serial.println("-----------------------------");
  // Close file
  SerFlash.close();

  // Open for reading, note that you will have to re-write file because it will be erased once you reopen it, or so I'm told
  readStatus = SerFlash.open("myfile.txt", FS_MODE_OPEN_READ);
  Serial.print("Read Status: ");
  Serial.println(readStatus);
  Serial.print("Waypoints Read: ");
  char bffr;
  int n = 0;
  int next_byte = 0;
  do
  {
    next_byte = SerFlash.read();
    bffr = (char)next_byte;
    if (next_byte != -1 && bffr != '\n')
    {
      if (n < 8)
      {
        // waypoint 1
        waypoint_one[n] = bffr;
      }
      else if (n > 8 && n < 17)
      {
        // waypoint 2
        waypoint_two[n-9] = bffr;
      }
      else if (n > 17 && n < 26)
      {
        // waypoint 3
         waypoint_three[n-18] = bffr;
      }
      else if (n > 26 && n < 35)
      {
        // waypoint 4
         waypoint_four[n-27] = bffr;
      }
      else if (n > 35 && n < 44)
      {
        // waypoint 5
         waypoint_five[n-36] = bffr;
      }
//      Serial.print(n); 
    }
    n++;
  }
  while (next_byte != -1);
  SerFlash.close();
  Serial.println();
  Serial.print(waypoint_one);
  Serial.print(waypoint_two);
  Serial.print(waypoint_three);
  Serial.print(waypoint_four);
  Serial.println(waypoint_five);
  Serial.println("-----------------------------");
}

void loop()
{
}

