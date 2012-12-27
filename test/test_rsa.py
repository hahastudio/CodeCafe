# -*- coding: utf-8 -*-
import unittest
from code.MessageServer import rsa

class TestRSA(unittest.TestCase):
    values=('hello','world','1','2012','yanhong')
    def test_rsa(self):
        r=rsa.RSA()
        for v in self.values:
            result = r.decrypt(r.encrypt(v))
            self.assertEqual(v, result)

if __name__ == '__main__':
    main()
