# -*- coding: utf-8 -*-

"""
Required Modules
"""
from asyncore import dispatcher
from asynchat import async_chat
import socket
import asyncore
import time
import cPickle
import threading
import re
from rsa import RSA

"""
global variables
"""
PORT = 50000
FSPORT = 49999
NAME = "CodeCafe"

UserLst = []
usrDB = open("userdata", "rb")
while 1:
    try:
        UserLst.append(cPickle.load(usrDB))
    except EOFError:
        break
usrDB.close()
UserDict = dict([(u["username"], u) for u in UserLst])

RSAEncryptor = RSA()

fLock = threading.RLock()
fcode = ""

usrdatLock = threading.RLock()
boardLock = threading.RLock()

def writeUserData(userlst):
    """
    Persistance for userdate
    """
    with usrdatLock:
        ouf = open("userdata", "wb")
        for user in userlst:
            cPickle.dump(user, ouf, 2)
        ouf.close()

def getip():
    """
    getip()
    使用socket模块中的gethostbyname_ex(hostname)函数，
    返回非192开头的ipv4地址。
    """
    names, aliases, ips = socket.gethostbyname_ex(socket.gethostname())
    for ip in ips :
        if not re.match('^192', ip):
            return ip
    return ips[0]

class FSThread(threading.Thread):
    """
    Thread for communicate with File Server
    """
    def __init__(self):
        super(FSThread, self).__init__()
        self.s = None

    def run(self):
        global fcode
        self.s = socket.socket()
        self.s.bind(("localhost", FSPORT))
        self.s.listen(5)
        fs, addr = self.s.accept()
        while 1:
            fs.sendall("filerequest\r\n")
            c = fs.recv(1024)
            if c:
                c = c.strip()
                if c != fcode:
                    with fLock:
                        fcode = c
            time.sleep(1)

class EndSession(Exception):
    pass

class CommandHandler(object):
    """
    Simple command handler similar to cmd.Cmd
    """
    def unknown(self, session, cmd):
        session.push("Unknown command: %s\r\n" % cmd)

    def handle(self, session, line):
        """
        Handle a received line from a given session
        """
        if not line.strip():
            return
        parts = line.split(' ', 1)
        cmd = parts[0]
        try:
            line = parts[1].strip()
        except IndexError:
            line = ''
        method = getattr(self, 'do_'+cmd, None)
        try:
            method(session, line)
        except TypeError:
            self.unknown(session, cmd)

class Room(CommandHandler):
    """
    A generic environment that may contain one or more users
    (sessions). It takes care of basic command handling and
    broadcasting.
    """

    def __init__(self, server):
        self.server = server
        self.sessions = []

    def add(self, session):
        """
        A session (user) has entered the room
        """
        self.sessions.append(session)

    def remove(self, session):
        """
        A session (user) has left the room
        """
        self.sessions.remove(session)

    def broadcast(self, line):
        """
        Send a line to all sessions in the room
        """
        for session in self.sessions:
            session.push(line)

    def do_logout(self, session, line):
        """
        Respond to the logout command
        """
        raise EndSession

class LoginRoom(Room):
    """
    A room meant for a single person who has just connected.
    """

    def add(self, session):
        Room.add(self, session)
        #self.broadcast("Welcome to %s\r\n" % self.server.name)

    def unknown(self, session, cmd):
        session.push("Please log in.\r\n")

    def do_login(self, session, line):
        name, pwd = line.strip().split(' ')
        if name in UserDict and UserDict[name]["password"] == pwd:
            if not name in self.server.users:
                session.user = UserDict[name]
                session.push("success login\r\n")
                session.push("Welcome, %s!\r\n" % name)
                session.push("account %s\r\n" % cPickle.dumps(session.user, 2))
                session.push("encrypt %s\r\n" % cPickle.dumps(RSAEncryptor, 2))
                session.enter(self.server.main_room)
            else:
                session.push("The user %s is already online!\r\n" % name)
        else:
            session.push("error Unknown user name or bad password.\r\n")

class ChatRoom(Room):
    """
    A room meant for multiple users who can chat with the others in
    the room.
    """

    def add(self, session):
        self.broadcast(session.user["username"]+ " has enter the room.\r\n")
        self.server.users[session.user["username"]] = session
        Room.add(self, session)

    def remove(self, session):
        Room.remove(self, session)
        self.broadcast(session.user["username"] + " has left the room.\r\n")

    def do_say(self, session, line):
        dst, msg = line.split(' ', 1)
        nowtime = time.strftime('%H:%M:%S')
        msgPkg = "say " + nowtime + ' ' + session.user["username"] + " to " + dst + ": \n" + msg + "\r\n"
        if dst == "-all":
            self.broadcast(msgPkg)
        else:
            dstSession = self.server.users.get(dst)
            if dstSession:
                dstSession.push(msgPkg)
                session.push(msgPkg)
            else:
                session.push("No such person online.\r\n")

    def do_editBoard(self, session, line):
        if session.user["isAdmin"]:
            self.server.board = line
            self.broadcast("board " + line + "\r\n")
            self.server.writeBoards()
        else:
            session.push("error You don't have permission.\r\n")

    def do_editAppointment(self, session, line):
        if session.user["isAdmin"]:
            self.server.appointment = line
            self.broadcast("appointment " + line + "\r\n")
            self.server.writeBoards()
        else:
            session.push("error You don't have permission.\r\n")

    def do_refresh(self, session, line):
        session.push("board " + self.server.board + "\r\n")
        session.push("appointment %s\r\n" % self.server.appointment)
        session.push("user " + ' '.join(name for name in self.server.users) + "\r\n")

    def do_setpwd(self, session, line):
        usrdata = cPickle.loads(line)
        if session.user["username"] == usrdata["username"]:
            session.user = usrdata
            UserDict[usrdata["username"]] = usrdata
            writeUserData(UserDict.values())
        else:
            session.push("error You can't set other user's password!\r\n")

    def do_filerequest(self, session, line):
        with fLock:
            session.push("fcode %s\r\n" % fcode)

    def do_look(self, session, line):
        session.push("The following are in this room:\r\n")
        for other in self.sessions:
            session.push(other.user["username"] + "\r\n")

    def do_who(self, session, line):
        session.push("The following are logged in:\r\n")
        for name in self.server.users:
            session.push(name + "\r\n")

    def do_logout(self, session, line):
        try:
            del self.server.users[session.user["username"]]
        except KeyError:
            pass        
        session.enter(session.loginroom)

class LogoutRoom(Room):
    """
    A simple room for a single user. Its sole purpose is to remove
    the user's name from the server.
    """

    def add(self, session):
        try:
            del self.server.users[session.user["username"]]
        except KeyError:
            pass

class ChatSession(async_chat):
    """
    A single session, which takes care of the communication with a
    single user.
    """

    def __init__(self, server, sock):
        async_chat.__init__(self, sock)
        self.server = server
        self.set_terminator("\r\n")
        self.data = []
        self.user = None
        self.loginroom = LoginRoom(server)
        self.enter(self.loginroom)

    def enter(self, room):
        try:
            cur = self.room
        except AttributeError:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)

    def collect_incoming_data(self, data):
        self.data.append(data)

    def found_terminator(self):
        line = ''.join(self.data)
        self.data = []
        try:
            self.room.handle(self, line)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))

class MessageServer(dispatcher):
    """
    A chat server with a single room.
    """

    def __init__(self, port, name):
        dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)
        self.name = name
        inf = open('boards', 'rb')
        self.board = cPickle.load(inf)
        self.appointment = cPickle.load(inf)
        inf.close()
        self.users = {}
        self.main_room = ChatRoom(self)
        print "Successfully initialize MessageServer."
        print "MessageServer's IP: %s, port: %d" % (getip(), PORT)

    def handle_accept(self):
        connetion, addr = self.accept()
        ChatSession(self, connetion)

    def writeBoards(self):
        with boardLock:
            ouf = open("boards", "wb")
            cPickle.dump(self.board, ouf, 2)
            cPickle.dump(self.appointment, ouf, 2)
            ouf.close()

if __name__ == '__main__':
    s = MessageServer(PORT, NAME)
    fsThread = FSThread()
    fsThread.start()
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print
