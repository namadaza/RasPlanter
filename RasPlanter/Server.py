#!/usr/bin/env python
import socket
from ServerCommand import ServerCommand

#take values/raw data out of serverps


class Server:
	def __init__(self):
		self.HOST = 'localhost'
		self.PORT = 9876
		self.BUFSIZ = 1024
		self.backlog = 5
		ADDR = (self.HOST, self.PORT)
		self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serversock.bind(ADDR)
		self.serversock.listen(self.backlog)
	
	def read_socket(self):
		clientsock, addr = self.serversock.accept()
		data = clientsock.recv(self.BUFSIZ)
		
		if (data):
			serverCommand = ServerCommand(data)
			return serverCommand
		else:
			print "Error, could not establish connection to server"
	
	def write_to_socket(self, user_input):
		clientsock, addr = self.serversock.accept()
		data = clientsock.recv(self.BUFSIZ)
		if data:
			clientsock.send(user_input)
		else:
			print "Could not send data"
		
		