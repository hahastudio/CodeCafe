# -*- coding: utf-8 -*-
import unittest,re
from subprocess import Popen, PIPE
from code.FileServer import FileServer

class TestGetip(unittest.TestCase):
    def test_messageserver(self):
        ip=re.search('\d+\.\d+\.\d+\.\d+',Popen('ipconfig', stdout=PIPE).stdout.read()).group(0)
        result=FileServer.getip()
        self.assertEqual(ip, result) 

if __name__ == '__main__':
    main()

