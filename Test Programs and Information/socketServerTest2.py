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
        clientsock.close()
