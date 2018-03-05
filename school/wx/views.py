#coding=utf-8
from flask import Blueprint, render_template, url_for, current_app, redirect,request,flash
from flask_wechatpy import wechat_required
from wechatpy.replies import TextReply,ArticlesReply,create_reply,ImageReply
from school.extensions import wechat
blueprint = Blueprint('wx', __name__, url_prefix='/wx')

#微信获取token
@blueprint.route('/token',methods=['GET'])
@wechat_required
def token_get():
    signature = request.args.get('signature','')
    timestamp = request.args.get('timestamp','')
    nonce = request.args.get('nonce','')
    echostr = request.args.get('echostr','')
    token = current_app.config['WECHAT_TOKEN']
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

    context_str = ''
    reply = TextReply(content=context_str, message=msg)
    

    #扫描二维码关注事件
    if msg.event == 'subscribe_scan':
        autoregister(msg.source)

        try:
            reply = TextReply(content=context_str, message=msg)
            #创建菜单
            # createmenu()
        except Exception, e:
            pass
    
        
    #关注事件
    if msg.event == 'subscribe':
        autoregister(msg.source)
        reply = TextReply(content=context_str, message=msg)
        #创建菜单
        # createmenu()
        
    #取消关注事件
    if msg.event == 'unsubscribe':
        try:
            pass
        except Exception, e:
            reply = ''
        reply = ''
        
            
    #定位事件
    if msg.event =='location': 
        try:
        	pass
        except Exception, e:
            user = []
        
    
        
    
    return reply


