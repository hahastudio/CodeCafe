import SocketServer, time  
import socket
import os  
import random
import threading
import fcode
class fcodethread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        nowms = time.strftime('%M-%S',time.localtime(time.time()))
        fcode.fcode = 999900
        while 1:
            if time.strftime('%M-%S',time.localtime(time.time())) == '00-00':
                fcode.fcode = random.randint(999988)

class MyServer(SocketServer.BaseRequestHandler):   
    userInfo = {   
        'yangsq'    : 'yangsq',   
        'hudeyong'  : 'hudeyong',   
        'mudan'     : 'mudan' }   
    localAddr = "D:/testserver/"   
    modcode = 999987 
  
    def handle(self):   
        print 'Connected from', self.client_address 
        """
        while True:
            receivedData = self.request.recv(1024)
            if not receivedData:
                continue
            if receivedData.startswith('name'):   
                self.clientName = receivedData.split(':')[-1]   
                if MyServer.userInfo.has_key(self.clientName):   
                    self.request.sendall('valid')   
                else:   
                    self.request.sendall('invalid')   
                       
            elif receivedData.startswith('pwd'):   
                self.clientPwd = receivedData.split(':')[-1]   
                if self.clientPwd == MyServer.userInfo[self.clientName]:   
                    self.request.sendall('valid')
                    break
                    #time.sleep(5)  
        """                                   
        while True:   

            receivedData = self.request.recv(1024)
            #print receivedData
            if not receivedData:   
                continue  
            if receivedData.startswith('FCODE'):
                self.request.sendall(str(fcode.fcode))
            elif receivedData.startswith('ANSWERFCODE'):
                temp = receivedData.split(':')[-1]
                if int(temp) % MyServer.modcode == fcode.fcode % MyServer.modcode:
                    print "Fcode permitted"
                    self.request.send('valid')
                else:
                    self.request.send('bad')
                    continue
            else:
                print 'wrong format'
                continue

            receivedData = self.request.recv(1024)

            if receivedData.startswith('LOGINNAME'):
                self.clientName = receivedData.split(':')[-1]
                self.request.send('valid')
                print self.clientName+' log in'
            else:
                print 'dont exist'
                continue

            receivedData = self.request.recv(1024)
            
            if receivedData.startswith('D'):                    
                today = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
                if not os.path.exists(MyServer.localAddr+self.clientName):
                    os.makedirs(MyServer.localAddr+self.clientName)
                if not os.path.exists(MyServer.localAddr+self.clientName+'/'+today):
                    os.makedirs(MyServer.localAddr+self.clientName+'/'+today)
                nowaddr = MyServer.localAddr+self.clientName+'/'+today+'/'+receivedData.split(' ',1)[-1]
                sfile = open(nowaddr, 'rb')   
                while True:   
                    
                    data = sfile.read(1024)                                         
                    if not data:   
                        break  
                    while len(data) > 0:   
                        intSent = self.request.send(data)   
                        data = data[intSent:]   
  
                time.sleep(3)   
                self.request.sendall('EOF')   
                sfile.close()     

            elif receivedData.startswith('U'):
                today = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
                if not os.path.exists(MyServer.localAddr+self.clientName):
                    os.makedirs(MyServer.localAddr+self.clientName)
                if not os.path.exists(MyServer.localAddr+self.clientName+'/'+today):
                    os.makedirs(MyServer.localAddr+self.clientName+'/'+today)
                nowaddr = MyServer.localAddr+self.clientName+'/'+today+'/'+receivedData.split(' ',1)[-1]
                DownloardF = open(nowaddr, 'wb')
                #print DownloardF
                while True:                           
                    receivedData = self.request.recv(1024)                                      
                     
                    DownloardF.write(receivedData)    
                    if receivedData == 'EOF':   
                        break
                DownloardF.flush()   
                DownloardF.close()
                print 'upload finished'

            elif receivedData.startswith('R'):
                Removepath = receivedData.split(' ',1)[-1]
                shutil.rmtree(Removepath)

            elif receivedData.startswith('EXIT'):
                break


                
  
        self.request.close()   
           
        print 'Disconnected from', self.client_address   
        print  
  
if __name__ == '__main__':   
    print 'Server is started/nwaiting for connection.../n' 
    threadForFcode = fcodethread()
    threadForFcode.start()
    srv = SocketServer.ThreadingTCPServer(('localhost', 50000), MyServer)   
    srv.serve_forever()
