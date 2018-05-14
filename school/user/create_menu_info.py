from flask import url_for
from school.extensions import wechat


#注册门卫 家长
def create_patriarch_doorkeeper__menu():
    wechat.menu.create({"button":[
        {"type":"view","name":"请假系统","sub_button":[
            {
                "type":"view",
                "name":"发起请假",
                "url":"%s"%url_for('user.send_leave',_external=True)
            },
            {
                "type":"view",
                "name":"我的发起",
                "url":'%s'%url_for('user.my_senf_leave',_external=True)
            },
        ]},\

        {"type":"view","name":"用户服务","sub_button":[
            {
                "type":"view",
                "name":"平台简介",
                "url":'%s'%url_for('public.introduction',_external=True)
            },
            {
                "type":"view",
                "name":"个人信息",
                "url":'%s'%url_for('public.user_info',_external=True)
            },
        ]},\
        
    ]})


#注册学生
def create_student_menu():
    wechat.menu.create({"button":[
        {"type":"view","name":"请假系统","sub_button":[
            {
                "type":"view",
                "name":"发起请假",
                "url":"%s"%url_for('user.send_leave',_external=True)
            },
            {
                "type":"view",
                "name":"我的请假",
                "url":'%s'%url_for('user.my_leave',_external=True)
            },
        ]},\

        {"type":"view","name":"用户服务","sub_button":[
            {
                "type":"view",
                "name":"平台简介",
                "url":'%s'%url_for('public.introduction',_external=True)
            },
            {
                "type":"view",
                "name":"个人信息",
                "url":'%s'%url_for('public.user_info',_external=True)
            },
        ]},\
        
    ]})


def create_teacher_menu():
    wechat.menu.create({"button":[
        {"type":"view","name":"请假系统","sub_button":[
            {
                "type":"view",
                "name":"发起请假",
                "url":"%s"%url_for('user.send_leave',_external=True)
            },
            {
                "type":"view",
                "name":"我的发起",
                "url":'%s'%url_for('user.my_senf_leave',_external=True)
            },
            {
                "type":"view",
                "name":"我的批准",
                "url":'%s'%url_for('user.charge_leave',_external=True)
            },
        ]},\

        {"type":"view","name":"用户服务","sub_button":[
            {
                "type":"view",
                "name":"平台简介",
                "url":'%s'%url_for('public.introduction',_external=True)
            },
            {
                "type":"view",
                "name":"个人信息",
                "url":'%s'%url_for('public.user_info',_external=True)
            },
        ]},\
        
    ]})




