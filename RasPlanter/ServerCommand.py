#!/usr/bin/env python

#take in raw text values from server,
#parse into variables for main RasPlanter program
class ServerCommand:
	def __init__(self, raw_string):
		command = raw_string.split("::")
		self.command_type = command[0]
		self.command_data = command[1]
		
	def get_command_type(self):
		return self.command_type
	
	def get_command_data(self):
		return self.command_data
		