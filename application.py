from socket import *
import argparse

def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", action="store_true", help="Run as a server")
    parser.add_argument("-c", "--client", action="store_true", help="Run as a client")
    parser.add_argument("-i", "--ip", type=str, default="127.0.0.1", help="IP-address")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port number")
    parser.add_argument("-f", "--file", type=str, help="The file you have to send")
    parser.add_argument("-w", "--window", type=int, default=3, help="Sliding window size")
    parser.add_argument("-d", "--discard", type=int, default=99999999, help="Discard packet with seq")

    args = parser.parse_args()
    return args

def start_server(serverIp, serverPort, discard_seq):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverIp, serverPort))
    print ('The server is ready to receive')
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(),clientAddress)

def start_client():


if __name__ == "__main__":
