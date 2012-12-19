import cPickle
import hashlib

UserLst = [
			{"username": "guyuhao", "password": "tbontb", "isAdmin": True},
			{"username": "linyiyang", "password": "123456", "isAdmin": True},
			{"username": "hongyan", "password": "hongyan", "isAdmin": False},
			{"username": "wanglang", "password": "wanglang", "isAdmin": False}
]

ouf = open('userdata', 'wb')
for user in UserLst:
	m = hashlib.md5()
	m.update(user["password"])
	m.update("salt")
	user["password"] = m.hexdigest()
	cPickle.dump(user, ouf, 2)
ouf.close()

inf = open('userdata', 'rb')
while 1:
	try:
		a = cPickle.load(inf)
		print a
	except EOFError:
		break
inf.close()