#coding=utf-8
from flask import Blueprint, render_template, url_for, current_app, redirect,request,flash
from flask_wechatpy import wechat_required
from wechatpy.replies import TextReply,ArticlesReply,create_reply,ImageReply
from school.extensions import csrf_protect,wechat,db

import datetime as dt
from ..public.models import AskLeave
from ..user.models import User

blueprint = Blueprint('wx', __name__, url_prefix='/wechat')



def createmenu():
    wechat.menu.create({"button":[
        {"type":"view","name":u"请假","sub_button":[
            {
                "type":"view",
                "name":u"发起请假",
                "url":"http://school.anaf.cn/users/send_leave"
            },
        ]},\

        {"type":"view","name":u"用户服务","sub_button":[
            {
                "type":"view",
                "name":u"个人中心",
                "url":'http://school.anaf.cn/users'
            },
            {
                "type":"view",
                "name":u"平台简介",
                "url":'http://school.anaf.cn/'
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

        event_str = msg.content[0:2]
        leave_id = msg.content[2:]

        user = User.query.filter_by(wechat_id=msg.source).first() 

        #同意请假
        if event_str == 'ag':

            ask_leave = AskLeave.query.get(leave_id)

            if not ask_leave:
                reply=TextReply(content=u'输入请假编号不正确。', message=msg)
                return reply

            if user != ask_leave.charge_ask_user or ask_leave.charge_state!=0:
                reply=TextReply(content=u'操作不正确', message=msg)
                return reply

            ask_leave.update(charge_state=1,charge_time=dt.datetime.now())
            reply=TextReply(content=u'您已同意该请假申请。', message=msg)
            return reply

        #不同意
        if event_str == 're':
            
            ask_leave = AskLeave.query.get(leave_id)

            if not ask_leave:
                reply=TextReply(content=u'输入请假编号不正确。', message=msg)
                return reply

            if user != ask_leave.charge_ask_user or ask_leave.charge_state!=0:
                reply=TextReply(content=u'操作不正确', message=msg)
                return reply
            #2拒绝
            ask_leave.update(charge_state=2,charge_time=dt.datetime.now())
            reply=TextReply(content=u'您已拒绝该请假申请。', message=msg)
            return reply

        #修改用户名
        if event_str == 'un':
            user.update(username=leave_id)
            reply=TextReply(content='用户名已修改。', message=msg)
            return reply

        #修改密码
        if event_str == 'pd':
            user.set_password(password=leave_id)
            db.session.add(user)
            db.session.commit()
            reply=TextReply(content=u'密码已修改。', message=msg)
            return reply



        reply=TextReply(content=u'您说什么我不懂耶。', message=msg)
    try:
        msg.event
    except Exception as e:
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
    





