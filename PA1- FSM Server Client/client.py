# Programming Assignment 1

import argparse
import socket

# Connects to the server and returns a socket object.
# You should not have to modify this function.
def connect():
  HOST, PORT = "eig.isi.edu", 63681
  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST,PORT))
    sock.settimeout(3)
    return sock
  except Exception as e:
    print("Server may be down!! Please send email.")
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

# Determines state changes based on rules set in FSM
def stateChange(data,state):
  if len(data) == 0:
    print("Connection ended by server.")
    print("Recieved message from server: \"%s\""%(data))
    state = "Idle"
  elif (data == "hello")or(data == "red")or(data == "gold"):
    state = "C"
  elif data == "yellow":
    state = "C1"
  elif data == "green":
    state = "C2"
  elif (data == "purple")or(data == "blue"):
    state = "C3"
  elif data == "cya":
    state = "F"
  elif data == "TIMEOUT":
    state = "TIMEOUT"
  else:
    state = "ERROR"
    print("Error: Incorrect/Unknown Response")
  return state

if __name__ == "__main__":
  # Set up argument parsing.
  parser = argparse.ArgumentParser(description='EE450 Programming Assignment #1')
  parser.add_argument('commands',  nargs='+', help='Space deliminated commands')
  args = parser.parse_args()
  
  # Handle getting a socket. 
  #s = connect()
  #if s == None:
    #exit()
  
  # Example of a sending one protocol message and receiving one protocol message.
  #send(s, "test")
  #data = recv(s)
  #if len(data) == 0:
  #  print("Connection ended by server.")
  #print("Recieved message from server: \"%s\""%(data))

  
  # Example of how you can step through the argument commands one by one.
  #for command in args.commands:
    #print("Got command %s" % (command))

  # Main Code

  # Initilize first state vaules
  state = "Idle"
  error = 0

  # Initialize connection
  s = connect()
  if s == None:
    exit()

  # Send start signal "hi"
  send(s, "hi")
  data = recv(s)

  # Resend if timeout
  if data != "hello":
    while data != "hello":
      send(s, "hi")
      data = recv(s)
  state = stateChange(data,state)
  print(data)

  # Main loop for instuction inputs on command line
  for command in args.commands:
    # Set reset for timeouts and errors
    lastState = state

    # Print current command
    print("Got command %s" % (command))

    # Sets rules for valid commands during each state
    if (state == "C")and((command == "b")or(command == "g")or(command == "s")or(command == "d")):
      if command == "b":
        send(s, "banana")
      elif command == "g":
        send(s, "grass")
      elif command == "s":
        send(s, "sky")
      elif command == "d":
        send(s, "done")
      data = recv(s)
      state = stateChange(data,state)
    elif (state == "C1")and((command == "r")or(command == "d")):
      if command == "r":
        send(s, "rose")
      elif command == "d":
        send(s, "done")
      data = recv(s)
      state = stateChange(data,state)
    elif (state == "C2")and((command == "v")or(command == "d")):
      if command == "v":
        send(s, "violets")
      elif command == "d":
        send(s, "done")
      data = recv(s)
      state = stateChange(data,state)
    elif (state == "C3")and((command == "f")or(command == "d")):
      if command == "f":
        send(s, "fish")
      elif command == "d":
        send(s, "done")
      data = recv(s)
      state = stateChange(data,state)
    elif (state == "F")and(command == "b"):
      send(s, "bye")
      state = "Idle"
      print("Connection Ended")
      print(state)
      exit()

    # Error condition and flag
    else:
      print("ERROR: Wrong state for this command!")
      print("Command Ignored")
      error = 1

    # Avoid print if error detected due to repetition
    if error == 0:
      print(data)
    if (state != "TIMEOUT")and(state != "ERROR"):
      print(state)

    # Reset error flag
    error = 0

    # Error/Timeout correction
    if (state == "TIMEOUT")or(state == "ERROR"):
      # Repeat until error or timeout is corrected
      while (state == "TIMEOUT")or(state == "ERROR"):
        # Reset last state to redo command
        state = lastState
        print("Got command %s" % (command))

        # Sets rules for valid commands during each state
        if (state == "C")and((command == "b")or(command == "g")or(command == "s")or(command == "d")):
          if command == "b":
            send(s, "banana")
          elif command == "g":
            send(s, "grass")
          elif command == "s":
            send(s, "sky")
          elif command == "d":
            send(s, "done")
          data = recv(s)
          state = stateChange(data,state)
        elif (state == "C1")and((command == "r")or(command == "d")):
          if command == "r":
            send(s, "rose")
          elif command == "d":
            send(s, "done")
          data = recv(s)
          state = stateChange(data,state)
        elif (state == "C2")and((command == "v")or(command == "d")):
          if command == "v":
            send(s, "violets")
          elif command == "d":
            send(s, "done")
          data = recv(s)
          state = stateChange(data,state)
        elif (state == "C3")and((command == "f")or(command == "d")):
          if command == "f":
            send(s, "fish")
          elif command == "d":
            send(s, "done")
          data = recv(s)
          state = stateChange(data,state)
        elif (state == "F")and(command == "b"):
          send(s, "bye")
          state = "Idle"
          print("Connection Ended")
          print(state)
          exit()

        # Error condition and flag
        else:
          print("ERROR: Wrong state for this command!")
          print("Command Ignored")
          error = 1

        # Avoid print if error detected due to repetition
        if (state != "TIMEOUT")and(state != "ERROR"):
          print(data)
        if error == 0:
          print(state)

        # Reset error flag
        error = 0

  # Set auto terminate if command does not lead to reset of FSM
    # Sends the state back to Idle if not yet done
  if state == "F":
    send(s, "bye")
    state = "Idle"
    print("Auto terminate:")
    print("Got command b")
    print(state)
    exit()

  # Sends the states back to F then Idle if not yet done
  if (state != "F")or(state != "Idle"):
    print("Auto terminate:")
    print("Got command d")
    send(s, "done")
    data = recv(s)
    state = stateChange(data,state)

    # Limit print outs during error and timeout due to repetition
    if (state != "TIMEOUT")and(state != "ERROR"):
      print(data)
      print(state)

    # Error/Timeout Correction
    if (state == "TIMEOUT")or(state == "ERROR"):
      # Repeat until timeout or error is corrected
      while (state == "TIMEOUT")or(state == "ERROR"):
        # Reset last state to redo command
        state = lastState
        print("Got command %s" % (command))

        # Sets rules for valid commands during each state
        if (state == "C")and((command == "b")or(command == "g")or(command == "s")or(command == "d")):
          if command == "b":
            send(s, "banana")
          elif command == "g":
            send(s, "grass")
          elif command == "s":
            send(s, "sky")
          elif command == "d":
            send(s, "done")
          data = recv(s)
          state = stateChange(data,state)
        elif (state == "C1")and((command == "r")or(command == "d")):
          if command == "r":
            send(s, "rose")
          elif command == "d":
            send(s, "done")
          data = recv(s)
          state = stateChange(data,state)
        elif (state == "C2")and((command == "v")or(command == "d")):
          if command == "v":
            send(s, "violets")
          elif command == "d":
            send(s, "done")
          data = recv(s)
          state = stateChange(data,state)
        elif (state == "C3")and((command == "f")or(command == "d")):
          if command == "f":
            send(s, "fish")
          elif command == "d":
            send(s, "done")
          data = recv(s)
          state = stateChange(data,state)
        elif (state == "F")and(command == "b"):
          send(s, "bye")
          state = "Idle"
          print("Connection Ended")
          print(state)
          exit()

        # Error condition and flag
        else:
          print("ERROR: Wrong state for this command!")
          print("Command Ignored")
          error = 1

        # Avoid print if error detected due to repetition
        if (state != "TIMEOUT")and(state != "ERROR"):
          print(data)
        if error == 0:
          print(state)

        # Reset error flag
        error = 0

    # Send final termination message to server before exiting
    send(s, "bye")
    state = "Idle"
    print("Auto terminate:")
    print("Got command b")
    print(state)
    exit()
