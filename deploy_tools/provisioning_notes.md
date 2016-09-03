配置新网站
========

## 需要安装的包

* nignx
* Python 3
* Git
* pip
* virtualenv

以Ubuntu为例，可以执行一下的命令安装

    sudo apt-get install nginx git python3 python3-pip
    sudo pip3 install virtualenv

## 配置nginx主机

* 参考nginx.template.conf
* 把SITENAME替换成所需要的域名，例如lala.lala.com

## Upstart任务

* 参考gunicorn-upstart.template.conf
* 把SITENAME替换成所需的域名，例如lala.lala.com

## 文件夹结构

.home/username
.....sites
.........SITENAME
.............database
.............source
.............static
.............virtualenv
