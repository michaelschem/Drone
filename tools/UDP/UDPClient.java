import java.io.*;
import java.net.*;

class UDPClient
{
	public static void main(String args[]) throws Exception
	{
		while(true) {
			BufferedReader inFromUser =
			new BufferedReader(new InputStreamReader(System.in));

			DatagramSocket clientSocket = new DatagramSocket();

			InetAddress IPAddress = InetAddress.getByName("127.0.0.1");
      //InetAddress IPAddress = InetAddress.getByName("localhost");
			System.out.println(IPAddress.toString());

			byte[] sendData = new byte[1024];
			byte[] receiveData = new byte[1024];

			String sentence = inFromUser.readLine();

			sendData = sentence.getBytes();

			DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, 42679);

			clientSocket.send(sendPacket);

       //Uncomment to wait for server ack
      //DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);

      //clientSocket.receive(receivePacket);

      //String modifiedSentence = new String(receivePacket.getData());
      //System.out.println("FROM SERVER:" + modifiedSentence);

			clientSocket.close();
		}
	}
}
