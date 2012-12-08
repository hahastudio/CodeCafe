import socket
sock1 = socket.socket()
host1 = 'localhost'
port1 = 49999
sock1.bind((host1,port1))
sock1.listen(5)

sock2 = socket.socket()
host2 = 'localhost'
port2 = 50000
sock2.connect((host2,port2))

while 1:
	c,addr = sock1.accept()
	print 'got connection from',addr
	while 1:
		temp = c.recv(1024)
		if temp:
			print 'got fcode request'
			break
	sock2.sendall('FCODE:request')
	while 1:
		temp = sock2.recv(1024)
		if temp:
			print 'fcode received'
			break
	c.send(temp)
	break
noww = raw_input("done")


