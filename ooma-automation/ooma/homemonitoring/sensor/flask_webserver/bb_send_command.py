import socket
import sys

UDP_IP = '127.0.0.1'
UDP_PORT = 888


def send_command(cmd):
    #Establish TCP Socket Connection
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Establish UDP Socket Connection
    sockaddr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockaddr.connect((UDP_IP, UDP_PORT))

    try:
        sockaddr.send(cmd)
        sockaddr.close()
        return "pass"
    except socket.error:
        print "Failed to send the GPIO Command"
        return IOError