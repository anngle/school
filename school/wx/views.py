#coding=utf-8
from flask import Blueprint, render_template, url_for, current_app, redirect,request,flash
from flask_wechatpy import wechat_required
from wechatpy.replies import TextReply,ArticlesReply,create_reply,ImageReply
from school.extensions import csrf_protect,wechat

blueprint = Blueprint('wx', __name__, url_prefix='/wechat')



def createmenu():
    wechat.menu.create({"button":[
        {"type":"view","name":u"请假","sub_button":[
            {
                "type":"view",
                "name":u"我要请假",
                "url":'http://car.anaf.cn/usercenter/show_order'
            },
            {
                "type":"view",
                "name":u"代请假",
                "url":'http://car.anaf.cn/driver/add_post'
            },
            ]},\
        
        {"type":"view","name":u"用户服务","sub_button":[
            
            {
                "type":"view",
                "name":u"平台简介",
                "key":'contact_us'
            },
            {
                "type":"view",
                "name":u"个人中心",
                "url":'http://car.anaf.cn/usercenter'
            },
            ]},\
        ]})



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



#微信token信息提交
@csrf_protect.exempt
@blueprint.route('/token',methods=['POST'])
@wechat_required
def token_post():
    msg = request.wechat_msg
    reply=''
    if msg.type == 'text':
        reply=TextReply(content=u'哈哈哈哈或或恍恍惚惚', message=msg)
    try:
        msg.event
    except Exception, e:
        return reply

    #关注事件
    if msg.event == 'subscribe':
        createmenu()
        reply = TextReply(content=u'欢迎关注。O(∩_∩)O哈！', message=msg)
    #扫描二维码关注事件
    if msg.event == 'subscribe_scan':
        createmenu()
        reply = TextReply(content=u'欢迎关注。O(∩_∩)O哈！', message=msg)


    
    return reply
    





