#!/usr/bin/env python
# coding:utf-8
"""
微信公众平台管理界面
"""

import os
import requests,urllib2
import hashlib
import random
import json
import sys
reload(sys)
from config import *

sys.setdefaultencoding('utf-8')#wx only adapt utf-8 (no unicode,no encoding and stay what it looks like)


session=requests.session()
session.headers={
                'User-Agent':'Mozilla/5.0 (<a href="http://www.ttlsa.com/windows/" title="windows"target="_blank">Windows</a> NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                'Accept-Encoding': 'deflate',
                'DNT': '1',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': 'https://mp.weixin.qq.com/',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'
                }


def login(username,pwd,):
    """登录"""
    #正确响应：{"base_resp":{"ret":0,"err_msg":"ok"},"redirect_url":"\/cgi-bin\/home?t=home\/index&lang=zh_CN&token=898262162"}
    print "username",username,"<====>","pwd",pwd
    global token
    pwd=hashlib.md5(pwd).hexdigest()
    print "username",username,"<+++++++>","pwd",pwd
    url='https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
    data={'f':'json',
          'imgcode':'',
          'pwd':pwd,
          'username':username}
    res=session.post(url,data)
    print 'response: login',res.text
    j=json.loads(res.text)
    status=j['base_resp']['err_msg']
    if status=='ok':
        token=j['redirect_url'].split('=')[-1]
        return True
    return False






def getTokenIntime(CorpId,Secret):
    #从微信官方接口生成当前有效的token
    res = urllib2.urlopen('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s'%(CorpId,Secret))
    res_dict = json.loads(res.read())
    print "res_dict is:======>", res_dict
    token = res_dict.get('access_token')

    #print type(str(res_dict)), str(res_dict)
    print "token is====》", token
    if not token:
        with open(r'./log/wx_log.txt','ab') as f:
            f.write(str(res_dict))
    return token


def getToken():
    #从文件中读取有效的token
    with open(r'./log/wx_token.txt') as f:
        t = f.read()
    return t



def sendTxtMsg(token,content,to_user='@all',to_party='',to_tag='',application_id=1,safe=0):
    #发送信息
    try:
        data = {
           "touser": to_user,
           "toparty": to_party,
           "totag": to_tag,
           "msgtype": "text",
           "agentid": application_id,
           "text": {
               "content": content,
           },
           "safe":safe
        }

        data = json.dumps(data,ensure_ascii=False)
        if Debug:
            with open(r'./log/wx_data.txt','ab') as f:
                f.write(data+'\r\n')
        req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s'%(token,))
        resp = urllib2.urlopen(req,data)
        msg = u'返回值:' + resp.read()
    except Exception,ex:
        msg = u'异常:' + str(ex)
    finally:
        with open(r'./log/wx_log.txt','ab') as f:
            f.write(msg+'\r\n')



def sendNews(token,title,description,url,pic_url,to_user="@all",to_party="",to_tag="",application_id=0,safe=0):
    #发送新闻
    try:
        data = {
           "touser": to_user,
           "toparty": to_party,
           "totag": to_tag,
           "msgtype": "news",
           "agentid": application_id,
           "news": {
               "articles":[
                   {
                       "title": title,
                       "description": description,
                       "url": url,
                       "picurl": pic_url,
                   }
               ]
           }
        }

        data = json.dumps(data,ensure_ascii=False)
        if Debug:
            with open(r'./log/wx_data.txt','ab') as f:
                f.write(data+'\r\n')
        req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/message/send?debug=1&access_token=%s'%(token,))
        resp = urllib2.urlopen(req,data)
        msg = u'返回值:' + resp.read()
    except Exception,ex:
        msg = u'异常:' + str(ex)
    finally:
        with open(r'./log/wx_log.txt','ab') as f:
            f.write(msg + '\r\n')

def send_btn(token,application_id=0):
    try:
        req = urllib2.Request('https://qyapi.weixin.qq.com/cgi-bin/menu/create?access_token=%s&agentid=%s'%(token,application_id))
        data = {
           "button":[
               {
                   "type":"view",
                   "name":"search",
                   "url":"http://devop.cc",
               },

           ]
        }
        data = json.dumps(data,ensure_ascii=False)
        res = urllib2.urlopen(req,data)
        msg = u'返回值:'+res.read()
    except Exception,ex:
        msg = u'异常:'+str(ex)
    finally:
        with open(r'./log/wx_log.txt','ab') as f:
            f.write(msg + '\r\n')


def generate_token(CorpID,Secret):
    with open(r'./log/wx_token.txt','wb') as f:
        if save_token:

            print (getTokenIntime(CorpID,Secret)),"run getTokenIntime "
            f.write(str(getTokenIntime(CorpID,Secret)))

        else:
            getTokenIntime(CorpID,Secret)


def get_msg():
    with open(r'./log/wx_msg.txt') as f:
        txt = f.read()
    txt = txt.replace('\r\n','').replace('\r','').replace('\n','').replace('\t','')
    return txt


#======================================test ==========================

def test_txt(content):
    token = getToken()
    if token:
        sendTxtMsg(token, content)



def test_news():
    img_url = 'http://d.hiphotos.baidu.com/image/w%3D2048/sign=a29e35bb8813632715edc533a5b7a1ec/d8f9d72a6059252d676bb463369b033b5bb5b95d.jpg'
    token = getToken()
    if token:
        sendNews(token, u'测试新闻', get_msg(), 'http://news.baidu.com', img_url)

def test_bb():
    token = getToken()
    if token:
        send_btn(token,application_id=1)



if __name__=='__main__':
    save_token =True #False
    #test_txt()
    #test_news()
    #test_bb()