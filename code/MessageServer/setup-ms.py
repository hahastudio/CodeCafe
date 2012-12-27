#coding=utf-8  
from distutils.core import setup  
import py2exe

setup(console=[{
                "script": 'MessageServer.py',
               }],
      options={"py2exe":{
                         "optimize":2,
                         #打包成一个文件，加快读取速度
                         "compressed":1,
                         "bundle_files":2,
                         #少了个文件,不管它
                         "dll_excludes":["MSVCP90.dll"],
                         },
               },
      zipfile=None,)#一个文件