# -*- coding: utf-8 -*-

import datetime
import requests
import json
import ast
from  wxQCode_const import TM_TWO_HOURS, APP_ID, APP_SECRETE, TEMPLATE_ID


class WeChat():
    def __init__(self, openid, name, phone, content):
        self.openid = openid
        self.name = name
        self.phone = phone
        self.data = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.content = content

    def set_token(self):
        payload = {
            'grant_type': 'client_credential',
            'appid': APP_ID,   #公众号appid,按自己实际填写
            'secret': APP_SECRETE,   #待按自己实际填写
        }
        url="https://api.weixin.qq.com/cgi-bin/token?"

        try:
            respone = requests.get(url, params=payload, timeout=50)
            access_token = respone.json().get('access_token')
            content = ("{\"access_token\":\"%s\",\"time\":\"%s\"}"
                       % (access_token, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))

            #写入文件
            with open('access_token.txt', 'w') as fw:
                fw.write(content)

            print('set_token', access_token)
        except Exception as e:
            print(e)

    def get_token(self):
        try:
            print('open txt\n')
            with open('access_token.txt', 'r') as f:
                print('file read')
                content = f.read()
                print('content:', content, '\ntype:', type(content), '\n')
                data_dict = ast.literal_eval(content)
                print('data_dict: ', data_dict)
                time = datetime.datetime.strptime(data_dict['time'], '%Y-%m-%d %H:%M:%S')

            if (datetime.datetime.now() - time).seconds < TM_TWO_HOURS:
                print('未到两小时，从文件读取')
                return data_dict['access_token']
            else:
                #超过两小时，重新获取
                print('超过两小时，重新获取')
                payload = {
                    'grant_type': 'client_credential',
                    'appid': APP_ID,   #公众号appid,按自己实际填写
                    'secret': APP_SECRETE,   #待按自己实际填写
                }
                url="https://api.weixin.qq.com/cgi-bin/token?"

                try:
                    respone = requests.get(url, params=payload, timeout=50)
                    access_token = respone.json().get('access_token')
                    content="{'access_token':"+str(access_token)+",'time':"+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+"}"

                    #写入文件
                    with open('access_token.txt', 'w') as fw:
                        fw.write(content)

                    print('get_token', access_token)
                    return access_token
                except Exception as e:
                    print(e)
        except Exception as e:
            print("get_token,file",e)

    def get_tempate_id(self):
        token = self.get_token()
        url = 'https://api.weixin.qq.com/cgi-bin/template/api_add_template?access_token=' + token
        data = {
            'template_id_short' : 'TM00015'
        }

    def post_data(self):
        data={
            'touser' : self.openid,
            'template_id' : TEMPLATE_ID, #模板ID
            'data' : {
                'first': {
                    'value' : '有新的客户预约，请及时处理！',
                    'color' : '#173177'
                },
                'keyword1' : {
                    'value' : self.name,
                    'color' : '#173177'
                },
                'keyword2' : {
                    'value' : self.phone,
                    'color' : '#173177'
                },
                'keyword3' : {
                    'value' : self.data,
                    'color' : '#173177'
                },
                'keyword4' : {
                    'value' : self.content,
                    'color' : '#173177'
                },
                'remark' :{
                    'value' : '点击跳转处理！',
                    'color' : '#173177'
                }
            }
        }

        json_template = json.dumps(data)
        access_token = self.get_token()
        print('access_token--', access_token)
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token

        try:
            respone = requests.post(url, data=json_template, timeout=50)
            #拿到返回值
            errcode = respone.json().get("errcode")
            print('test--', respone.json())
            if(errcode == 0):
                print("模板消息发送成功")
            else:
                print("模板消息发送失败")
        except Exception as e:
            print("test++", e)
