# -*- coding: utf-8 -*-
import cPickle
import hashlib
import os

expandUserLst = [
			{"username": "guyuhao", "password": "tbontb", "isAdmin": True},
			{"username": "linyiyang", "password": "123456", "isAdmin": True},
			{"username": "hongyan", "password": "hongyan", "isAdmin": False},
			{"username": "wanglang", "password": "wanglang", "isAdmin": False}
]
board = ""
appts = ""
#Initialize Users' Data
oriUserLst = []
if os.path.exists('userdata'):
	inf = open('userdata', 'rb')
	while 1:
		try:
			u = cPickle.load(inf)
			oriUserLst.append(u)
		except EOFError:
			break
	inf.close()
for user in expandUserLst:
	m = hashlib.md5()
	m.update(user["password"])
	m.update("salt")
	user["password"] = m.hexdigest()
UserLst = oriUserLst + expandUserLst
for u in UserLst:
	print u
ouf = open('userdata', 'wb')
for user in UserLst:
	cPickle.dump(user, ouf, 2)
ouf.close()

#Initialize Board & Appointments
ouf = open('boards', 'wb')
cPickle.dump(board, ouf, 2)
cPickle.dump(appts, ouf, 2)
ouf.close()
