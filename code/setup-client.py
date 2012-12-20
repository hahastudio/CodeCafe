#coding=utf-8  
from distutils.core import setup  
import py2exe  
setup(windows=[{'script':'Client.py'}],options={'py2exe':{'includes':['sip','PyQt4']}})
