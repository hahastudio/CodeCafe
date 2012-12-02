import socket, time  
  
class MyClient:   
  
    def __init__(self):   
        print 'Prepare for connecting...'   
  
    def connect(self):   
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        sock.connect(('localhost', 50000))   
  
        sock.sendall('Hi, server')   
        self.response = sock.recv(8192)   
        print 'Server:', self.response   
  
        self.s = raw_input("Server: Do you want get the 'thinking in python' file?(y/n):")   
        if self.s == 'y':   
            while True:   
                self.name = raw_input('Server: input our name:')   
                sock.sendall('name:' + self.name.strip())   
                self.response = sock.recv(8192)   
                if self.response == 'valid':   
                    break  
                else:   
                    print 'Server: Invalid username'   
  
            while True:   
                self.pwd = raw_input('Server: input our password:')   
                sock.sendall('pwd:' + self.pwd.strip())   
                self.response = sock.recv(8192)   
                if self.response == 'valid':   
                    print 'please wait...'   
  
                    f = open('b.pdf', 'wb')   
                    while True:   
                        data = sock.recv(1024)   
                        if data == 'EOF':   
                            break  
                        f.write(data)   
                           
                    f.flush()   
                    f.close()   
  
                    print 'download finished'   
                    break  
                else:   
                    print 'Server: Invalid password'   
                   
  
        sock.sendall('bye')   
        sock.close()   
        print 'Disconnected'   
  
if __name__ == '__main__':   
    client = MyClient()   
    client.connect()