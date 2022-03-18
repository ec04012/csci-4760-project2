#import socket module
from email import message
from socket import *
import sys # In order to terminate the program
import os

# Source
# https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
# https://www.geeksforgeeks.org/python-os-path-join-method/

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # what does this line do?
serverSocket.bind((SERVER_HOST, SERVER_PORT))
serverSocket.listen(1)
ServerName = "HTTP Server"
print(ServerName + " is now ONLINE")
print('Listening on port %s ...' % SERVER_PORT)
print("")
while True:
    #Establish the connection
    print('Listening for requests ...')
    # Wait for client connections
    connectionSocket, addr = serverSocket.accept()
    print("Connected to Client")
    try:
        message = connectionSocket.recv(1024).decode()
        #print(message)
        filename = message.split()[1]
        with open(os.path.join("./", filename[1:])) as f:
            outputdata = f.read()
        #print(outputdata)
        print("User requested " + filename)
        #Send one HTTP header line into socket
        response = 'HTTP/1.1 200 OK\n\n'
        connectionSocket.send(response.encode())
        print("Sent Header")
        #Send the content of the requested file to the client
        connectionSocket.send(outputdata.encode())
        connectionSocket.send("\r\n".encode())
        print("Sent Content")
        # Close client socket
        connectionSocket.close()
        print("")
    except IOError:
        #Send response message for file not found
        response = 'HTTP/1.1 404 NOT FOUND\n'
        connectionSocket.send(response.encode())
        #Close client socket
        connectionSocket.close()
        print("ERROR: File Not Found")
        print("User requested " + filename)
        print("")
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding dat