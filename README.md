# ����flask��ܵ�΢�ŷ��ͱ�����Ϣapi
���api����ͨ��΢�ŵ���ҵ�ŷ�����Ϣ��
## ��װ����
����ʹ��virtualenv������Python������yum��װ���е�root�˺�
```bash
yum install -y python-virtualenv

$ cd /path/to/weixin_api/
$ virtualenv ./env

$ ./env/bin/pip install -r install_requirements.txt
```
## ���÷���
```bash
vim config.py

Debug = True (����Debugģʽ)
save_token = True  ������token��

```
����ʾ��
```bash
curl 192.168.0.39:5000 -d 'CorpID=ID&Secret=secret&content=message'
```

## ���̹���
ͳһʹ�õ�minos�Ĺ�����control
```bash
./weixinserver start ��������
./weixinserver stop ֹͣ����
./weixinserver restart ��������
./weixinserver status �鿴����״̬
./weixinserver tail ��tail -f�ķ�ʽ�鿴var/app.log
```
###log�ļ���΢�Žӿ������־�ļ� ���flash��ܵ���־�ļ��ڰ�װ�õ����⻷����varĿ¼�¡�
