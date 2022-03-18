#import socket module
from email import message
from socket import *
import sys # In order to terminate the program
import os
import atexit
import itertools
import threading
import time

# Source
# https://www.codementor.io/@joaojonesventura/building-a-basic-http-server-from-scratch-in-python-1cedkg0842
# https://www.geeksforgeeks.org/python-os-path-join-method/
# https://docs.python.org/3/library/atexit.html
# https://stackoverflow.com/questions/22029562/python-how-to-make-simple-animated-loading-while-process-is-running

# graceful exit in case of crash or other disruption
def graceful_exit():
    serverSocket.close()
    print("Closing Server")
    sys.exit()#Terminate the program
atexit.register(graceful_exit)

animating = False
# animation function
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if animating:
                print('\r     Waiting ' + c, end="")
                time.sleep(0.25)
def stopAnimating():
        global animating
        animating=False
        print('\r                               \r', end="")
# Create animation thread
t = threading.Thread(target=animate, daemon=True)
t.start()

# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8080

serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # what does this line do?
serverSocket.bind((SERVER_HOST, SERVER_PORT))
serverSocket.listen(1)
ServerName = "HTTP Server"
print(ServerName + " is now ONLINE")
print('Listening on %s:%s ...' % (SERVER_HOST, SERVER_PORT))
print("")

while True:
    #Establish the connection
    print('Listening for requests ...')
    animating = True
    # Wait for client connections
    connectionSocket, addr = serverSocket.accept()
    stopAnimating()
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
        animating = True
    except IOError:
        stopAnimating()
        #Send response message for file not found
        response = 'HTTP/1.1 404 NOT FOUND\n\nFile not found'
        connectionSocket.send(response.encode())
        #Close client socket
        connectionSocket.close()
        print("ERROR: File Not Found")
        print("User requested " + filename)
        print("")
        animating = True
graceful_exit()