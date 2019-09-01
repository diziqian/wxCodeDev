# coding:utf-8

from flask import Flask, request, render_template
from wechatpy import WeChatClient, parse_message
from wechatpy.replies import ImageReply
from wxQCode_const import TOKEN, APP_ID, APP_SECRETE, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DB
from wxQCode_func import get_update
from wxQCode_file import get_media_id, get_qcode
from wxQCode_templateInfo import WeChat
from wxQCode_db import DbMysql


token = TOKEN

CLIENT = WeChatClient(APP_ID, APP_SECRETE)
app = Flask(__name__)


def check_signature():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    check = get_update(token, timestamp, nonce)
    return True if check == signature else False

@app.route('/weixin', methods=['GET', 'POST'])
def weixinInterface():
    if check_signature:
        data = request.data
        msg = parse_message(data)
        path = get_qcode(request.args['openid'])
        md_id = get_media_id(CLIENT, path)
        reply = ImageReply(media_id=md_id, message=msg)
        xml = reply.render()
        return xml
    else:
        return 'signature error'

@app.route('/submit', methods=['GET', 'POST'])
def submitInterface():
    print(request.method)
    if request.method == 'GET':
        print(request.args)
        open_id = request.args['openid']
        print('\n',open_id)
        return render_template('submit.html', open_id=open_id)
    elif request.method == 'POST':
        # 待测试
        # open_id = request.args['open_id']
        # mobile_phone = request.args['mobilephone']
        # mydb = DbMysql(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DB)
        # mydb.insert(open_id, mobile_phone)
        # my_wechat = WeChat("aaa", "test", "13012345678", "测试程序")
        # my_wechat.post_data()
        return render_template('submit_success.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
