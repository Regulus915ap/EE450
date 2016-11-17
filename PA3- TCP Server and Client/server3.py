#!/usr/bin/python
# Programming Assignment 3 (Server Code)

import argparse
import socket
import sys
from thread import *

# Connects to the server and returns a socket object.
# You should not have to modify this function.
def listenPort():
  HOST, PORT = "localhost", 9999
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket Created")
    sock.bind((HOST,PORT))
    print("Socket Bind Complete")
    return sock
  except Exception as e:
    print("ERROR: Bind Failed")
    print(e)
    return None

# Takes in a socket and a string (message) and attempts to send to the server.
def send(s, message):
  try:
    s.sendall(message.encode('utf-8'))
  except Exception as e: 
    print(e)

#Function for handling connections. This will be used to create threads
def clientthread(conn):
  while True:
    #Receiving from client
    data = conn.recv(1000000)
    if not data: 
      break
    # Send back the right message
    if data == "Hi":
      conn.send("Hello")
    elif data == "Done":
      conn.send("Received")
    elif data == "Bye":
      print("Client (%s, %s) has disconnected" % addr)
      break
    elif len(data) > 1000:
      TotalCount = 0
      count = len(data)
      while count > 0:
         count = count - 1000
         TotalCount = TotalCount + 1000
         print("Received 1000 bytes from client " + str(clientNum) + ". Total: " + str(TotalCount))
      count = -count
      TotalCount = TotalCount + count
      print("Received " + str(count) + " bytes from client " + str(clientNum) + ". Total: " + str(TotalCount))
    else:
      print("Error: Incorrect/Unknown Response")
  conn.close()

# Main Code

# Initialize bind
state = "Idle"
clientNum = -1
s = listenPort();
s.listen(10)
if s == None:
  exit()
state = "Active"
 
#now keep talking with the client
while 1:
  clientNum = clientNum + 1
  #wait to accept a connection - blocking call
  conn, addr = s.accept()
  print 'Connected with ' + addr[0] + ':' + str(addr[1])
  start_new_thread(clientthread ,(conn,))
 
s.close()

state = "Idle"
server_socket.close()
