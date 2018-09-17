#coding=utf-8
from flask import Blueprint, render_template, url_for, current_app, redirect,request,flash
from flask_wechatpy import wechat_required
from wechatpy.replies import TextReply,ArticlesReply,create_reply,ImageReply

from school.extensions import csrf_protect,wechat,db
from school.auth.views import autoregister

import datetime as dt
from ..public.models import AskLeave
from ..user.models import User
from .enum import commands

import re

blueprint = Blueprint('wx', __name__, url_prefix='/wechat')


#关注公众号创建的菜单
def createmenu():
    wechat.menu.create({"button":[
        {"type":"view","name":u"平台主页",\
            "url":"%s"%url_for('public.home',_external=True)},\

        {"type":"view","name":u"用户服务","sub_button":[
            {
                "type":"view",
                "name":u"个人中心",
                "url":'%s'%url_for('user.members',_external=True)
            },
            {
                "type":"view",
                "name":u"平台简介",
                "url":'%s'%url_for('public.home',_external=True)
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
    try:
        
        msg = request.wechat_msg
        reply=''

        if msg.type == 'text':

            # 匹配指令
            command_match = False
            user = User.query.filter_by(wechat_id=msg.source).first() 

            for key_word in commands:
                if re.match(key_word, msg.content):
                    re_str = msg.content.replace(commands[key_word][0],'').strip()
                    reply = commands[key_word][1](user,msg,re_str)
                    command_match = True
                    break

            if not command_match:
                reply=TextReply(content=u'您说什么我不懂耶。', message=msg)

    except Exception as e:
        return reply

    try:
        msg.event
    except Exception as e:
        return reply

    msg_str = '欢迎关注【安星物业服务管理平台】，如你非校内人员或非学生家长，\
        <a href="{0}">请点击这里注册填写您的信息</a>'.format(url_for('user.register_set_role',_external=True))

    #关注事件  扫描二维码
    if msg.event == 'subscribe':

        user = autoregister(msg.source)
        createmenu()
        
        reply = TextReply(content=msg_str, message=msg)
    

    #扫描带参数二维码关注事件
    if msg.event == 'subscribe_scan':
        createmenu()
        user = autoregister(msg.source)

        if not msg.scene_id:
            reply = TextReply(content=msg_str, message=msg)

        #注册学生  家长   教师   门卫  
        if msg.scene_id =='register_student':
            msg_str = '欢迎关注【安星物业服务管理平台】，\
                <a href="{0}">请点击这里验证学生信息</a>'.format(url_for('user.register_set_student',_external=True))
            
        if msg.scene_id =='register_parent':
            msg_str = '欢迎关注【安星物业服务管理平台】，\
                <a href="{0}">请点击这里验证家长信息</a>'.format(url_for('user.register_set_parent',_external=True))

        if msg.scene_id =='register_teacher':
            msg_str = '欢迎关注【安星物业服务管理平台】，\
                <a href="{0}">请点击这里验证教师身份信息</a>'.format(url_for('user.register_set_teacher',_external=True))

        if msg.scene_id =='register_dooereeper':
            msg_str = '欢迎关注【安星物业服务管理平台】，\
                <a href="{0}">请点击这里验证校警信息</a>'.format(url_for('user.register_set_dooereeper',_external=True))

        reply = TextReply(content=msg_str, message=msg)

    
    return reply
    





