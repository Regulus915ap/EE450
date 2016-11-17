#!/usr/bin/python
# Programming Assignment 3 (Client Code)

import argparse
import socket
import select
import sys

# Connects to the server and returns a socket object.
# You should not have to modify this function.
def connect():
  HOST, PORT = "localhost", 9999
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST,PORT))
    return sock
  except Exception as e:
    print("ERROR: Server Down")
    print(e)
    return None

# Takes in a socket and a string (message) and attempts to send to the server.
def send(s, message):
  try:
    s.sendall(message.encode('utf-8'))
  except Exception as e: 
    print(e)

# Takes a socket object, attempts to read a message from the server.
def recv(s):
  try:
    data = s.recv(1024)
    return data.decode('utf-8')
  except socket.timeout:
    print("No messages received from the server.")
    print("Maybe the server *did not* get your message!")
    print("Or maybe you sent a non-protocol message and the server has no response.")
    return "TIMEOUT"
  except Exception as e:
    print(e)
    return "ERROR"
    
# Main Code

# Initilize first state vaules
state = "Idle"

# Initialize connection
s = connect()
if s == None:
  exit()

# Send start signal "hi"
send(s, "Hi")
data = recv(s)

# Resend if timeout
count = 0
while data != "Hello":
  send(s, "Hi")
  data = recv(s)
  count = count + 1
  if count == 3:
    print("TIMEOUT ERROR")
    send(s, "Bye")
    state = "ERROR"
    exit()
    
state = "Transmit"
print(data)
print(state)
count = 0
while(state == "Transmit"):
  from bitarray import bitarray
  message = bitarray(20000)
  s.sendall(message)
  s.send("Done")
  data = recv(s)
  if(data == "Received"):
    break
  count = count + 1
  if count == 3:
    print("TIMEOUT ERROR")
    send(s, "Bye")
    state = "ERROR"
    exit()

# Send final termination message to server before exiting
send(s, "Bye")
state = "Finish"
print(state)
exit()
