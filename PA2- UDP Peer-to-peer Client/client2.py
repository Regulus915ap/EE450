#!/usr/bin/python
# Programming Assignment 2
# Server: steel.isi.edu (128.9.160.71)

import argparse
import socket
import select
import sys

# Part 1
def register(s):
  try:
    msg1 = b'SRC:000;DST:999;PNUM:1;HCT:1;MNUM:###;VL:;MESG:register'
    print("Message: " + msg1)
    s.connect((UDP_IP, UDP_PORT))
    s.sendto(msg1, (UDP_IP, UDP_PORT))
    s.settimeout(3)
    print("Message Sent!")
    print("Receiving...")
    while True:
      print("Loading...")
      data, address = s.recvfrom(1024) # buffer size is 1024 bytes
      data = data.decode('utf-8')
      if not data:
        break
      print("Completed")
      data = data[61:64]
      data1 = data[47:52]
      if str(data1) == "Error":
        print(data1)
        exit()
      print("Successfully registered. My ID is: " + data)
      return data
  except socket.timeout:
    print("Timeout. Retrying...")
    register(s)
    return
  except Exception as e:
    print("ERROR DETECTED")
    print(e)
    return None

# Send datagram
def send(s, message):
  try:
    s.connect((UDP_IP, UDP_PORT))
    s.sendto(message, (UDP_IP, UDP_PORT))
    s.settimeout(3)
    print("Message Sent!")
    return 1
  except socket.timeout:
    print("Timeout. Please try again")
    return -1
  except Exception as e:
    print("ERROR DETECTED")
    print(e)
    return -1

def receive(s):
  try:
    s.connect((UDP_IP, UDP_PORT))
    s.settimeout(3)
    print("Receiving...")
    while True:
      print("Loading...")
      data, address = s.recvfrom(1024) # buffer size is 1024 bytes
      data = data.decode('utf-8')
      if not data:
        break
      print("Completed")
      PNUM = data[21]
      data1 = data[47:52]
      data = data[47:]
      if str(data1) == "Error":
        print(data1)
        exit()
      return data
  except socket.timeout:
    print("Timeout. Please try again")
    return -1
  except Exception as e:
    print("ERROR DETECTED")
    print(e)
    return -1

# Receive Code and Respond
def receiveSendACK(s, idNum):
  try:
     s.connect((UDP_IP, UDP_PORT))
     s.settimeout(3)
     while True:
       print("Loading...")
       data, address = s.recvfrom(1024) # buffer size is 1024 bytes
       data = data.decode('utf-8')
       if not data:
         break
       print("Completed")
       PNUM = data[21]
       MNUM = data[34:37]
       HCT = data[27]
       HCT = int(HCT)
       VL = data[41:44]
       sender = data[12:15]
       receiver = data[4:7]
       data1 = data[47:52]
       data = data[47:]
       if str(data1) == "Error":
         print(data1)
         exit()
       print(data)         
       if PNUM == "3":
         reply = "SRC:" + sender + ";DST:" + receiver + ";PNUM:4;HCT:1;MNUM:" + MNUM + ";VL:;MESG:ACK"
         send(s,reply)
         if (sender != idNum):
           if HCT == 0:
             print("********************")
             print("Dropped message from " + receiver + " to " + sender + " - hop count exceeded")
             print("MESG: " + data)
           elif HCT > 0:
             if VL == idNum:
               print("********************")
               print("Dropped message from " + receiver + " to " + sender + " - hop count exceeded")
               print("MESG: " + data)
             else:
               command = 'SRC:' + idNum + ';DST:999;PNUM:5;HCT:1;MNUM:' + idNum + ';VL:;MESG:get map'
               command = command.encode('ascii')
               send(s, command)
               data6 = receive(s)
               data6Array = data6.split('and')
               data6Array1 = data6Array[0][4:]
               data6Array2 = data6Array1.split(',')
               for people in data6Array2:
                 if people != idNum:
                   count = 0
                   HCT = HCT - 1
                   command = 'SRC:' + idNum + ';DST:' + data + ';PNUM:7;HCT:1;MNUM:' + idNum + ';VL:;MESG:' + mesgCheck
                   command = command.encode('ascii')
                   print(command)
                   reply = -1
                   ack = "false"
                   while (count < 5) and (reply == -1) and (ack != "ACK"):
                     reply = "SRC:" + receiver + ";DST:" + people + ";PNUM:3;HCT:" + str(HCT) + ";MNUM:" + MNUM + ";VL:;MESG:" + data
                     send(s,reply)
                     ack = receive(s)
                     count = count + 1
                     if count >= 5:
                       print("********************")
                       print("ERROR: Gave up sending to " + data)
                       print("********************")
       elif PNUM == "7":
         print("********************")
         print("SRC:" + receiver + " broadcasted:")
         print(data)
         reply = "SRC:" + sender + ";DST:" + receiver + ";PNUM:8;HCT:1;MNUM:" + MNUM + ";VL:;MESG:ACK"
         send(s,reply)
     return
  except socket.timeout:
    print("Timeout. Please try again")
    return -1
  except Exception as e:
    print("ERROR DETECTED")
    print(e)
    return -1
   
# Main Code
UDP_IP = "128.9.160.71"
UDP_PORT = 63682
print("UDP target IP: " + UDP_IP)
print("UDP target port: " + str(UDP_PORT))
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
idNum = register(s)
quit = 0

inputs = [s, sys.stdin]

while(quit == 0):
  print("Please enter a command:")
  inputsReady, outputsReady, exceptionReady = select.select(inputs, [], [])
  if inputsReady:
    for value in inputsReady:
      if value == sys.stdin:
        mesg = value.readline().strip()
        
        #Part 2
        if mesg == 'get map':
          command = 'SRC:' + idNum + ';DST:999;PNUM:5;HCT:1;MNUM:' + idNum + ';VL:;MESG:' + mesg
          command = command.encode('ascii')
          send(s, command)
          data6 = receive(s)
          data6Array = data6.split('and')
          data6Array1 = data6Array[0][4:]
          data6Array2 = data6Array[1].split(',')
         
          print('********************')
          print('Recently Seen Peers:')
          print(data6Array1)
          print(' ')
          print('Known addresses:')
          for data in data6Array2:
            dataArray = data.split('@')
            print(dataArray[0][0:3] + "  " + dataArray[0][4:] + "  " + dataArray[1])
          print('********************')
        
        #Part 3
        elif mesg[0:3] == "msg":
          count = 0
          mesgCheck = mesg[8:]
          if len(mesgCheck) > 200:
            mesgCheck = mesg[8:208]
          command = 'SRC:' + idNum + ';DST:' + mesg[4:7] + ';PNUM:3;HCT:1;MNUM:' + idNum + ';VL:;MESG:' + mesgCheck
          command = command.encode('ascii')
          data3 = -1
          while (count < 5) and (data3 == -1):
              data3 = send(s, command)
              count = count + 1
              if count >= 5:
                print("********************")
                print("ERROR: Gave up sending to " + mesg[4:7])
                print("********************")
           
        elif mesg[0:3] == 'all':
          mesgCheck = mesg[4:]
          if len(mesgCheck) > 200:
            mesgCheck = mesg[8:208]
            command = 'SRC:' + idNum + ';DST:999;PNUM:5;HCT:1;MNUM:' + idNum + ';VL:;MESG:get map'
            command = command.encode('ascii')
            send(s, command)
            data6 = receive(s)
            data6Array = data6.split('and')
            data6Array1 = data6Array[0][4:]
            data6Array2 = data6Array1.split(',')
            for data in data6Array2:
              count = 0
              command = 'SRC:' + idNum + ';DST:' + data + ';PNUM:7;HCT:1;MNUM:' + idNum + ';VL:;MESG:' + mesgCheck
              command = command.encode('ascii')
              print(command)
              data3 = -1
              ack = "false"
              while (count < 5) and (data3 == -1) and (ack != "ACK"):
                  data3 = send(s, command)
                  ack = receive(s)
                  count = count + 1
                  if count >= 5:
                    print("********************")
                    print("ERROR: Gave up sending to " + data)
                    print("********************")
        
      elif value == s:
        receiveSendACK(s, idNum)
exit()
