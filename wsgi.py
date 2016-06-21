#!/usr/bin/env python
#coding:utf-8
from flask import Flask
from flask import jsonify
from flask import request
import json
import weixin
app = Flask(__name__)

status = [
    {
        'status': 200,
        'info': 'send OK'
    }
]
errstatus = [
    {   
        'status': 201,
        'info': 'NO GET access'
    }
]


err_vliad = [
    {
        'status': 400,
        'info': 'request valid, NO token'
    }
]




@app.route('/', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        #获取用户提交的CorpID，Secret,content
        CorpID = request.form.get('CorpID')
        Secret = request.form.get('Secret')
        content = request.form.get('content')

	print "CorpID--->",CorpID,"   ","Secret-->",Secret,"   ","content--->",content
        #微信CorpID，Secret，content检查是否为空
        if  CorpID and Secret and content:
            #如果检查验证通过
            #生成token，获取token
            weixin.generate_token(CorpID,Secret)

            token = weixin.getToken()

            print "token IS :",token
            if  token!="None":
                 #发送消息
                weixin.sendTxtMsg(token, content)

                #发送新闻
                #weixin.test_news()

                #回调。。。。
                #weixin.test_bb()

                return jsonify({'response':status})

            else:

                return jsonify({'response':err_vliad})

    elif request.method == 'GET':
        return jsonify({'response':errstatus})
    else:
        return jsonify({'response':'unknown method'})


if __name__ == '__main__':
    app.run(port=5000,host='0.0.0.0',debug=True)

