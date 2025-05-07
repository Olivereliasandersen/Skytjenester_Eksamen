from socket import *
from struct import *
import argparse
import time
from datetime import datetime

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

#Application
def application():
    args

#Header#
header_format = '!HHHH'

def create_packet(seq, ack, flags, win, data):
    header = pack (header_format, seq, ack, flags, win)
    packet = header + data
    print (f'packet containing header + data of size {len(packet)}') #just to show the length of the packet
    return packet

def parse_header(header):
    header_from_msg = unpack(header_format, header)
    return header_from_msg

def parse_flags(flags):
    syn = flags & (1 << 3)
    ack = flags & (1 << 2)
    fin = flags & (1 << 1)
    return syn, ack, fin

#SERVER#
def startServer(serverIp, serverPort, discard_seq):
    flags = 0
    sequence_number = 0
    acknowledgment_number = 1
    window = 0

    file_data = {}

    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverIp, serverPort))
    print ('The server is ready to receive')
    while True:
        message, clientAddress = serverSocket.recvfrom(2048)

        if message == b"SYN":
            print("SYN packet is received")
            flags = 8
            serverSocket.sendto(b"SYN-ACK", clientAddress)
            print("SYN-ACK packet is sent")
            continue
        elif message == b"ACK":
            print("ACK packet is received")
            flags = 4
            print("Connection established")
            start_time = time.time()
            continue
        elif message == b"FIN":
            print("FIN packet is received")
            flags = 2
            serverSocket.sendto(b"FIN-ACK", clientAddress)
            print("FIN ACK packet is sent")
            break
        
        
#CLIENT#
def startClient(serverIp, serverPort, windowSize):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    serverAddress = (serverIp, serverPort)
    print("Connection Establishment Phase:\n")
    print("SYN packet is sent")
    clientSocket.sendto(b"SYN", serverAddress)

    sequence_number = 0
    acknowledgment_number = 0
    flags = 0
    window = 0
    slidingWindow = []

    try:
        with open(file, "rb") as f:
            data_file = f.read()
    except:
        print(f"{file} is not a file")
        return

    chunk = 992

    while True:
        try:
            response, serverAddress = clientSocket.recvfrom(2048)
            if response == b"SYN-ACK":
                print("SYN-ACK packet is received")
                clientSocket.sendto(b"ACK", serverAddress)
                print("ACK packet is sent")
                print("Connection established\n")
                print("Data Transfer")
                break
        except timeout:
            print("Timeout waiting for SYN-ACK. Retrying...")
            clientSocket.sendto(b"SYN", serverAddress)

    while True: #HUSK Å LEGGE TIL EN MÅTE BREAK
        data = data_file[sequence_number*chunk:(sequence_number+1)*chunk]
        msg = create_packet(sequence_number, acknowledgment_number, flags, window, data)
        slidingWindow.append(sequence_number)
        if len(slidingWindow) > window:
            slidingWindow = slidingWindow[1:]
        print(f"{datetime.now} -- packet with seq = {sequence_number} is sent, sliding window = {slidingWindow}")
        sequence_number += 1


if __name__ == "__main__":
    syn, ack, fin = parse_flags(13)
    print (f'syn_flag = {syn}, fin_flag={fin}, and ack_flag={ack}')