import SocketServer, time  
import socket
import os  
import random
import threading
import fcode
import cPickle
class fcodethread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        nowms = time.strftime('%M-%S',time.localtime(time.time()))
        fcode.fcode = 999900
        while 1:
            if time.strftime('%M-%S',time.localtime(time.time())) == '00-00':
                fcode.fcode = random.randint(0,999988)

class connectmessageserver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.sockettoMS = socket.socket()
        self.host = 'localhost'
        self.port = 49999
        print 'running49999'
        self.sockettoMS.connect((self.host,self.port))
        print 'cc'
        """
        self.sockettoMS.send('connect to MS')
        while 1:
            temp = self.sockettoMS.recv(1024)
            if temp:
                print 'connection to MS is OK'                
                break
        """
        while 1:
            temp = self.sockettoMS.recv(1024)
            print temp
            if temp.startswith('filerequest'):
                self.sockettoMS.send(str(fcode.fcode)+'\r\n')

class MyServer(SocketServer.BaseRequestHandler):   
    localAddr = "D:/test2/"   
    modcode = 999987 
    
            
    def handle(self):   
        
        FileRefresh = open('FileRefresh.txt','wb')
          
        def VisitDir(arg,dirname,name):
            for filespath in name:
                if os.path.isfile(os.path.join(dirname,filespath)):
                    FileRefresh.write(filespath+'\r\n')


        print 'Connected from', self.client_address                                
        while True:   

            receivedData = self.request.recv(1024)
            #print receivedData
            if not receivedData:   
                continue          
            if receivedData.startswith('fileaccess'):
                temp = receivedData.split(' ')[-1]
                if int(temp) % MyServer.modcode == fcode.fcode % MyServer.modcode:
                    print "Fcode permitted"
                    self.request.send('info validation\r\n')
                else:
                    self.request.send('error fcode mismatch!\r\n')
                    continue
            else:
                print 'wrong format'
                continue
            """
            receivedData = self.request.recv(1024)

            if receivedData.startswith('LOGINNAME'):
                self.clientName = receivedData.split(':')[-1]
                self.request.send('valid')
                print self.clientName+' log in'
            else:
                print 'dont exist'
                continue
            """
            receivedData = self.request.recv(1024)
            
            
            if receivedData.startswith('download'):                    
                today = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
                splitanswer = receivedData.split(' ')
                nowaddr = splitanswer[1]+'_'+splitanswer[2]+'_'+splitanswer[3][:-2]
                print nowaddr
                if not os.path.exists(nowaddr):
                    print 'file does not exists'
                    self.request.send('error no such file!\r\n')
                else:
                    print 'file exists'
                    self.request.sendall('start\r\n')
                    
                sfile = open(nowaddr, 'rb')   
                while True:                       
                    data = sfile.read(1024)                                         
                    if not data:   
                        break  
                    while len(data) > 0:   
                        intSent = self.request.send(data)   
                        data = data[intSent:]   
  
                self.request.sendall('EOF\r\n')   
                sfile.close()     

            elif receivedData.startswith('upload'):
                print "upload"
                today = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
                splitanswer = receivedData.split(' ')

                nowaddr = splitanswer[1]+'_'+today+'_'+splitanswer[2].strip()
                vernum = 0
                if os.path.exists(nowaddr):
                    vernum = 1
                    while 1:
                        if os.path.exists(splitanswer[1]+'_'+today+'('+str(vernum)+')_'+splitanswer[2][:-2]):
                            vernum+=1
                        else:
                            nowaddr = splitanswer[1]+'_'+today+'('+str(vernum)+')_'+splitanswer[2][:-2]
                            break
                if not os.path.exists('refresh.txt'):
                    firstdumpf = open('refresh.txt','wb')
                    tempp = []
                    cPickle.dump(tempp,firstdumpf,2)
                    firstdumpf.close()
                filenameDump = open('refresh.txt','rb')
                filedump = cPickle.load(filenameDump)
                dumpflag = 0
                for tempfile in filedump:
                    if tempfile['filename'] == splitanswer[1] and tempfile['owner'] == splitanswer[2][:-2]:
                        dumpflag = 1
                        if vernum:
                            tempfile['date'].append(today+'('+str(vernum)+')')
                        else:
                            tempfile['date'].append(today)
                        break
                if dumpflag==0:
                    filedump.append({'filename':splitanswer[1],'date':[today],'owner':splitanswer[2][:-2]})
                filenameDump.close()
                filenameDump = open('refresh.txt','wb')
                cPickle.dump(filedump,filenameDump,2)
                filenameDump.close()

                uploadfile = open(nowaddr, 'wb')
                #print uploadfile
                while True:                           
                    receivedData = self.request.recv(1024)                                                           
                    if not receivedData:
                        break
                    #print receivedData
                    uploadfile.write(receivedData)                        
                #uploadfile.flush()   
                uploadfile.close()
                print 'upload finished'

            elif receivedData.startswith('delete'):
                splitanswer = receivedData.split(' ')
                nowaddr = splitanswer[2]+'_'+splitanswer[3]+'_'+splitanswer[4][:-2]
                print nowaddr
                if not os.path.exists(nowaddr):
                    print 'error no such file!\r\n'
                    self.request.sendall('error no such file!\r\n')
                else:
                    if splitanswer[4][:-2] == splitanswer[1]:
                        print 'info success!\r\n'
                        self.request.sendall('info success!\r\n')
                        print 22
                        os.remove(nowaddr)
                        filenameDump = open('refresh.txt','rb')
                        filedump = cPickle.load(filenameDump)
                        dumpflag = 0
                        for tempfile in filedump:
                            if tempfile['filename'] == splitanswer[2] and tempfile['owner'] == splitanswer[4][:-2]:
                                tempfile['date'].remove(splitanswer[3])
                            if tempfile['date']==[]:
                                filedump.remove(tempfile)                                                    
                        filenameDump.close()
                        filenameDump = open('refresh.txt','wb')
                        cPickle.dump(filedump,filenameDump,2)
                        filenameDump.close()
                    else:
                        print 'error permission denied!\r\n'
                        self.request.sendall('error permission denied!\r\n')

            elif receivedData.startswith('EXIT'):
                break
            elif receivedData.startswith('refresh'):
                if not os.path.exists('refresh.txt'):
                    firstdumpf = open('refresh.txt','wb')
                    tempp = []
                    cPickle.dump(tempp,firstdumpf,2)
                    firstdumpf.close()
                FileRefresh = open('refresh.txt','rb')
                dumpdata = cPickle.load(FileRefresh)
                dumpdatasend = cPickle.dumps(dumpdata,2)
                self.request.sendall(dumpdatasend)
                self.request.sendall('endlist\r\n')
                FileRefresh.close()
                        
        self.request.close()   
           
        print 'Disconnected from', self.client_address   
        
  
if __name__ == '__main__':   
    print 'Server is started\nwaiting for connection...\n' 
    threadForMS = connectmessageserver()
    threadForMS.start()
    threadForFcode = fcodethread()
    threadForFcode.start()
    srv = SocketServer.ThreadingTCPServer(('localhost', 50001), MyServer)   
    srv.serve_forever()
