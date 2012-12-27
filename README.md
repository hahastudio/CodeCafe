#CodeCafe

Let's code in a cafe!

该项目是ColdCafe团队为课程CS362（软件工程实践）而做的课程设计。这是一个纯**Python**项目，我们使用了**PyQt4**作为图形库。

该项目允许小型开发团队的成员进行线上交流、发布信息和提交代码。

##Authors

ColdCafe Team:

* *Leader* 
    * [Alan haha](https://github.com/hahastudio)
* *Members*
    * [alanlyy](https://github.com/alanlyy)
    * [redswallow](https://github.com/redswallow)
    * [wlwlwl](https://github.com/wlwlwl)

##Deploy Message Server & File Server

如果您希望部署在一个长期运行的服务器上，我们建议您在服务器上安装**Python 2.6**，并对服务器脚本进行适当修改后部署。如果您使用Windows，只是想耍一耍这个小程序，或者您的机器上并没有**Python 2.6**的环境，您可以下载Windows对应的编译版本。但无论如何，请您读完下面两段。

在Message Server部署前，您需要先修改`userdatainit.py`，以添加、删除可以登录服务器的用户帐户。我们默认提供了一个用户名为`test`、密码亦为`test`的非管理员测试账户，请注意。修改后，请执行一次`userdatainit.py`。

如果您修改了服务器的端口，请同时修改`Client.py`的端口信息。如有需要，请重新编译。

##Compile with py2exe

**请先确保您安装了Python2.6，Py2exe**

编译`MessageServer.py`：请先转至`MessageServer.py`所在的目录，之后执行：

    > python setup-ms.py py2exe

编译`FileServer.py`：请先转至`FileServer.py`所在的目录，之后执行：

    > python setup-fs.py py2exe

**需要PyQt4**

编译`Client.py`：请先转折`Client.py`所在的目录，之后执行：

    > python setup-client.py py2exe

## Git Address

支持三种访问协议：

* HTTP协议: `https://github.com/hahastudio/CodeCafe.git` 。
* Git协议: `git://github.com/hahastudio/CodeCafe.git` 。
* SSH协议: `ssh://git@github.com:hahastudio/CodeCafe.git` 。

## How to clone our git

操作示例：

    $ git clone git://github.com/hahastudio/IM-haha.git
