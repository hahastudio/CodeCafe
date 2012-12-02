import SocketServer, time  
  
class MyServer(SocketServer.BaseRequestHandler):   
    userInfo = {   
        'yangsq'    : 'yangsq',   
        'hudeyong'  : 'hudeyong',   
        'mudan'     : 'mudan' }   
  
    def handle(self):   
        print 'Connected from', self.client_address   
           
        while True:   
            receivedData = self.request.recv(8192)   
            if not receivedData:   
                continue  
               
            elif receivedData == 'Hi, server':   
                self.request.sendall('hi, client')   
                   
            elif receivedData.startswith('name'):   
                self.clientName = receivedData.split(':')[-1]   
                if MyServer.userInfo.has_key(self.clientName):   
                    self.request.sendall('valid')   
                else:   
                    self.request.sendall('invalid')   
                       
            elif receivedData.startswith('pwd'):   
                self.clientPwd = receivedData.split(':')[-1]   
                if self.clientPwd == MyServer.userInfo[self.clientName]:   
                    self.request.sendall('valid')   
                    time.sleep(5)   
  
                    sfile = open('tiger.pdf', 'rb')   
                    while True:   
                        data = sfile.read(1024)   
                        if not data:   
                            break  
                        while len(data) > 0:   
                            intSent = self.request.send(data)   
                            data = data[intSent:]   
  
                    time.sleep(3)   
                    self.request.sendall('EOF')   
                else:   
                    self.request.sendall('invalid')   
                       
            elif receivedData == 'bye':   
                break  
  
        self.request.close()   
           
        print 'Disconnected from', self.client_address   
        print  
  
if __name__ == '__main__':   
    print 'Server is started/nwaiting for connection.../n'   
    srv = SocketServer.ThreadingTCPServer(('localhost', 50000), MyServer)   
    srv.serve_forever()