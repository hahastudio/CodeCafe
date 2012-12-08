import socket, time  
import os
import threading
class MyClient:    
    fcode = 123
    modcode = 999987
    def __init__(self):   
        print 'Prepare for connecting...'   
    
    def connect(self):   
        #fileserver
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        sock.connect(('localhost', 50000))   
        sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        sock2.connect(('localhost', 49999)) 
        #sock.sendall('Hi, server')   
        #self.response = sock.recv(8192)   

        #sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #print 'Server:', self.response   

        
        
        
  

        while True:            
            sock2.sendall('request:fcode')
            while 1:
                self.response2 = sock2.recv(8192)
                if self.response2:
                    break
            self.fcode = int(self.response2)
            print 'got fcode'
            transcode = self.fcode % self.modcode
            sock.sendall('ANSWERFCODE:'+str(transcode))
            while 1:
                self.response = sock.recv(8192)
                if self.response:
                    break
            print self.response
            if self.response != 'valid':
                print 'connection to chatserver is down!'
                continue
            print 'connection ok!'

            self.name = raw_input('Server: input our name:')   
            sock.sendall('LOGINNAME:'+self.name)
            while 1:
                self.response = sock.recv(8192)
                if self.response:
                    break
            if self.response != 'valid':
                continue

            self.s = raw_input("downloadfile(D),uploadfile(U),deletefile(R): ")
            if self.s.startswith('D'):                 
                self.downloadpath = raw_input("input downloadpath: ")            
                self.localpath = raw_input("input localpath: ")
                self.CheckD = raw_input('sure?(Y/N): ')    
                if self.CheckD != "Y":
                    continue
                while True:                  
                    DownloardF = open(self.localpath, 'wb')
                    sock.sendall('D '+self.downloadpath)
                    while True:   
                        data = sock.recv(1024)   
                        if data == 'EOF':   
                            break  
                        DownloardF.write(data)                                  
                    DownloardF.flush()   
                    DownloardF.close()   
  
                    print 'download finished'   
                    break  
            elif self.s.startswith('U'):
                self.uploadpath = raw_input("input uploadpath: ")
                self.localpath = raw_input("input localpath: ")
                self.CheckU = raw_input('sure?(Y/N)')
                if self.CheckU !="Y":
                    continue

                sock.sendall('U '+self.uploadpath)
                UploadF = open(self.localpath,'rb')                                
                while True: 
                    data2 = UploadF.read(1024)  
                    print len(data2)                  
                    if not data2:
                        break
                    while len(data2) > 0:   
                            intSent = sock.send(data2)   
                            data2 = data2[intSent:]   
                    #time.sleep(3)   
                sock.sendall('EOF')
                print 'ik'
                UploadF.close()

            elif self.s.startswith('R'):
                self.removepath = raw_input("input removepath: ")
                sock.sendall('R '+self.removepath)

            elif self.s.startwith('EXIT'):
                sock.sendall(self.s)
  


                       
  
        sock.sendall('bye')   
        sock.close()   
        print 'Disconnected'   
  
if __name__ == '__main__':   
    client = MyClient()   
    client.connect()
