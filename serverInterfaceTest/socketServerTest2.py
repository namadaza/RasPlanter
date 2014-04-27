#!/usr/bin/env python

"""
A simple echo server
"""

import socket
if __name__=='__main__':
    HOST = 'localhost'
    PORT = 5555
    BUFSIZ = 1024
    backlog = 5
    ADDR = (HOST, PORT)
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.bind(ADDR)
    serversock.listen(backlog)

    while True:
        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        data = clientsock.recv(BUFSIZ)
        if data:
            clientsock.send(data)
            print '...connected from:', addr
	    print "Data recieved: ", data
	    
	    #Will be either setDays, setLightcycle, setTemperature, setHumidity
	    parse_string = data.split("::")
	    for str in parse_string:
		    print str
	    command_type = parse_string[0]
	    command_data = parse_string[1]
	    print command_type
	    print command_data
	    
	    if command_type=="setDays":
		    print command_data
	    if command_type=="setLightcycle":
		    print command_data
	    if command_type=="setTemperature":
		    print command_data
	    if command_type=="setHumidity":
		    print command_data
 
        clientsock.close()
