#import socket module
from email import message
from socket import *
import sys # In order to terminate the program
import os

# Source https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
# https://www.geeksforgeeks.org/python-os-path-join-method/

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
#serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # what does this line do?
serverSocket.bind((SERVER_HOST, SERVER_PORT))
serverSocket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    #Establish the connection
    print('Ready to serve...')
    # Wait for client connections
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        print(message)
        filename = message.split()[1]
        with open(os.path.join("./", filename[1:])) as f:
            outputdata = f.read()
        #Send one HTTP header line into socket
        response = 'HTTP/1.0 200 OK\n\n'
        connectionSocket.send(response.encode())
        #Send the content of the requested file to the client
        connectionSocket.send(outputdata.encode())
        connectionSocket.close()
        '''
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        '''
    except IOError:
        #Send response message for file not found
        #Fill in start
        #Fill in end
        #Close client socket
        #Fill in start
        #Fill in end
        print("ERROR")
serverSocket.close()
sys.exit()#Terminate the program after sending the corresponding dat