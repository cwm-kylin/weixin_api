# 基于flask框架的微信发送报警信息api
这个api就是通过微信的企业号发送消息。
## 安装方法
我们使用virtualenv来管理Python环境，yum安装需切到root账号
```bash
yum install -y python-virtualenv

$ cd /path/to/weixin_api/
$ virtualenv ./env

$ ./env/bin/pip install -r install_requirements.txt
```
## 配置方法
```bash
vim config.py

Debug = True (开启Debug模式)
save_token = True  （保存token）

```
请求示例
```bash
curl 192.168.0.39:5000 -d 'CorpID=ID&Secret=secret&content=message'
```

## 进程管理
统一使用的minos的管理工具control
```bash
./weixinserver start 启动进程
./weixinserver stop 停止进程
./weixinserver restart 重启进程
./weixinserver status 查看进程状态
./weixinserver tail 用tail -f的方式查看var/app.log
```
###log文件是微信接口相关日志文件 相关flash框架的日志文件在安装好的虚拟环境下var目录下。
