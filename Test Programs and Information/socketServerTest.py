
def handler(clientsock,addr):
    while  True:
        data = clientsock.recv(BUFSIZ)
        if not data:
            break
        msg = "echoed:..." + data
        clientsock.send(msg)
    clientsock.close()

if __name__=='__main__':
    HOST = 'localhost'
    port = 5555
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    serverstock = socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.bind(ADDR)
    serversock.listen(2)

    while True:
        print 'waiting for connection...'
        clientsock, addr = serversock.accept()
        print '...connected from:', addr
        thread.start_new_thread(handler, (clientsock, addr))
