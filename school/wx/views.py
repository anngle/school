#coding=utf-8
from flask import Blueprint, render_template, url_for, current_app, redirect,request,flash
from flask_wechatpy import wechat_required
from wechatpy.replies import TextReply,ArticlesReply,create_reply,ImageReply
# from school.extensions import wechat


blueprint = Blueprint('wx', __name__, url_prefix='/wechat')


#微信获取token
@blueprint.route('/token',methods=['GET'])
@wechat_required
def token_get():
    signature = request.args.get('signature','')
    timestamp = request.args.get('timestamp','')
    nonce = request.args.get('nonce','')
    echostr = request.args.get('echostr','')
    token = current_app.config['SCHOOL_WECHAT_TOKEN']
    sortlist = [token, timestamp, nonce]
    sortlist.sort()
    sha1 = hashlib.sha1()
    map(sha1.update, sortlist)
    hashcode = sha1.hexdigest()
    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    return echostr



#微信调用 位置和token等其他相关
@blueprint.route('/token',methods=['POST'])
@wechat_required
def token_post():
    msg = request.wechat_msg
    reply = TextReply(content='欢迎关注调度猿.\
           \n如果您是司机想要拉货，<a href="http://car.anaf.cn/consignor">请点击这里</a>.\
           \n如果您是货主想要找车，<a href="http://car.anaf.cn/driver">请点击这里</a>.', message=msg)
    return reply
    





