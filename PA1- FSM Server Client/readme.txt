RUN: 	Instructions are as such:
			%python3.2 client.py {LIST OF COMMANDS}
		Example:
			%python3.2 client.py b r b r g v f s d b
			
BUGS:	 I was unable to make the code cleaner. Had to repeat
		 most of my code get the command resending working. Tried
		 to use pass by reference to condense rules into a funciton,
		 but failed to do as such
		 
INFO:	 As for the main code itself, it has adeared to the requested
		 funcitons. It can compensate to handle errors by resending
		 the command that failed to go through and reporting that a
		 timeout has occurred. It can also ignore commands that do not
		 correspond to the rules of the current state, reporting said
		 incorrect commands to the command line as well. Done can be sent
		 at any state. If done or bye has not been sent, the process has 
		 been automated to do so to reset the FSM back to Idle. Incorrect
		 responses are also reported and the command repeated when it 
		 occurs. Timeouts are also able to be handled by resending
		 commands that do not receive a reply.