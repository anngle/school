#coding=utf-8

from ..public.models import AskLeave,ChargeTeacher,Classes,Grade,School
from wechatpy.replies import TextReply
from school.extensions import db,wechat
import datetime as dt

#同意请假
def allow_ask_leave(user,msg,data=''):
    ask_leave = AskLeave.query.get(data)

    if not ask_leave:
        return TextReply(content=u'输入请假编号不正确。', message=msg)
    
    if user != ask_leave.charge_ask_user or ask_leave.charge_state!=0:
        return TextReply(content=u'操作不正确', message=msg)
    
    ask_leave.update(charge_state=1,charge_time=dt.datetime.now())
    return TextReply(content='您已同意该请假申请。',message=msg)


#拒绝请假
def reject_allow_ask_leave(user,msg,data=''):
    ask_leave = AskLeave.query.get(data)

    if not ask_leave:
        return TextReply(content=u'输入请假编号有误，请重新输入。', message=msg)

    if user != ask_leave.charge_ask_user or ask_leave.charge_state!=0:
        return TextReply(content=u'操作不正确', message=msg)

    #2拒绝
    ask_leave.update(charge_state=2,charge_time=dt.datetime.now())
    return TextReply(content=u'您已拒绝该请假申请。', message=msg)


#修改用户名
def change_username(user,msg,data=''):
    if len(data)<6 or len(data)>15:
        return TextReply(content='用户名长度不正确', message=msg)

    user.update(username=data)
    return TextReply(content='用户名已修改。', message=msg)


def change_password(user,msg,data=''):
    if len(data)<6 or len(data)>15:
        return TextReply(content='密码长度不正确', message=msg)

    user.set_password(password=data)
    db.session.add(user)
    db.session.commit()
    return TextReply(content=u'密码已修改。', message=msg)


#同意教师的设置申请
def allow_reg_teacher(user,msg,data=''):
    teacher = ChargeTeacher.query.get(int(data))
    if not teacher or not teacher.tmp_classes_id:
        return TextReply(content='输入编号不正确，请重新输入', message=msg)

    classes = Classes.query\
        .with_entities(Classes.id,School.id)\
        .join(Grade,Grade.id==Classes.grades) \
        .join(School,School.id==Grade.school) \
        .filter(Classes.id==teacher.tmp_classes_id)\
        .first()
    school = School.query.filter_by(users=user).first() 

    if not school:
        return TextReply(content='输入错误。', message=msg)
    if classes[1] != school.id:
        return TextReply(content='输入编号不正确，请重新输入', message=msg)

    update_classes = Classes.query.get(int(teacher.tmp_classes_id))

    update_classes.update(teacher=teacher)
    teacher.update(tmp_classes_id='')

    try:
        wechat.message.send_text(teacher.users.wechat_id,'您申请的信息已被确认')
    except Exception as e:
        pass

    return TextReply(content='您已同意该申请信息', message=msg)







