# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, url_for, current_app, redirect,request,flash, session
from flask_login import login_required,login_user,current_user
import time,random
from sqlalchemy import desc
from flask_wechatpy import oauth

import datetime as dt

from .models import User,Role,Permission
from ..public.models import *
from ..decorators import permission_required
from log import logger
from ..extensions import wechat
from .forms import SendLeaveForm
from school.utils import templated,flash_errors

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/')
@templated()
@login_required
def members():
    """List members."""
    return dict()

@blueprint.route('/set_roles')
@login_required
def set_roles():
	school = School.query.filter_by(active=True).order_by(desc('id')).all()
	return render_template('users/set_roles.html',school=school)


@blueprint.route('/set_roles',methods=["POST"])
@login_required
def set_roles_post():
	logger.info(u'doork0')
	school_id = request.form.get('school_id','0')
	role_id = request.form.get('role_id','0')
	number = request.form.get('number','0')
	verify = request.form.get('verify','0')
	phone = request.form.get('phone','0')
	name = request.form.get('name','')
	school = School.query.get_or_404(school_id)

	#教师
	if int(role_id) ==1:
		if verify != current_app.config['REGISTERVERIFY']:
			flash(u'校验码错误','danger')
			return redirect(url_for('public.home'))
		role = Role.query.filter_by(name='Teacher').first()
		current_user.update(phone=phone,roles=role,schools=school,first_name=name)
		ChargeTeacher.create(number=number,users=current_user)
		flash(u'您已设置角色为“教师”。','success')
	#学生
	if int(role_id)==0:
		role = Role.query.filter_by(name='Students').first()
		student = Student.query.filter_by(number=number).filter_by(name=name).first()
		if not student:
			flash(u'姓名与学号不符合，请重新输入','danger')
			return redirect(url_for('public.home'))
		student.update(users=current_user)
		current_user.update(phone=phone,roles=role,schools=school,first_name=name)
		flash(u'您已设置角色为“学生”。','success')
	#家长
	if int(role_id)==2:
		role = Role.query.filter_by(name='Patriarch').first()
		student = Student.query.filter_by(number=number).filter_by(name=name).first()
		if not student:
			flash(u'姓名与学号不符合，请重新输入','danger')
			return redirect(url_for('public.home'))
		sp = StudentParent.create(users=current_user)
		student.update(parents=sp)
		current_user.update(phone=phone,roles=role,schools=school,first_name=name+'的家长')
		flash(u'您已设置角色为“%s”的家长。'%name,'success')
	#门卫
	logger.info(u'doork1')
	if int(role_id)==3:
		logger.info(u'doork2')
		if verify != current_app.config['REGISTERVERIFY']:
			flash(u'校验码错误','danger')
			return redirect(url_for('public.home'))
		role = Role.query.filter_by(name='Doorkeeper').first()
		current_user.update(phone=phone,roles=role,schools=school,first_name=name)
		Doorkeeper.create(number=number,users=current_user)
		flash(u'您已设置角色为“门口保安”。','success')
	
	return redirect(url_for('public.home'))


#发起请假
@blueprint.route('/send_leave',methods=['GET'])
@templated()
@login_required
@permission_required(Permission.LEAVE)
def send_leave():
	form = SendLeaveForm()
	return dict(form=form)


@blueprint.route('/send_leave',methods=['POST'])
@login_required
@permission_required(Permission.LEAVE)
def send_leave_post():

	logger.info(u'进来了0')

	form = SendLeaveForm()
	if not form.validate_on_submit():
		flash_errors(form)
		return redirect(url_for('.send_leave'))

	logger.info(u'进来了1')

	number = form.number.data
	ask_start_time = form.start_time.data
	ask_end_time = form.end_time.data
	why = form.why.data

	if not number:
		try:
			number = current_user.student.number
		except Exception, e:
			flash(u'请输入学号')
			return redirect(url_for('.send_leave'))
		
	student = Student.query\
		.join(Classes,Classes.id==Student.classesd) \
		.join(Grade,Grade.id==Classes.grades) \
		.join(School,School.id==Grade.school) \
		.filter(School.id==current_user.school)\
		.filter(Student.number==number)\
		.first()
	if not student:
		flash(u'没有该学生,请重新输入正确的学号。','danger')
		return redirect(url_for('.send_leave'))

	
	if AskLeave.query.filter_by(ask_student=student).filter(AskLeave.charge_state.in_([0,1])).first():
		flash(u'该请假人已经存在请假申请，不能再次发起申请。','danger')
		return redirect(url_for('.send_leave'))

	student_role = Role.query.filter_by(name='Students').first()
	if current_user.roles==student_role:
		if current_user !=student.users:
			flash(u'你也是学生不能帮其他同学请假的哟。','danger')
			return redirect(url_for('.send_leave'))

	if student_role!=current_user.roles:
		if  student.parents:
			patriarch_role = Role.query.filter_by(name='Patriarch').first()
			if student.parents.users != current_user:
				flash(u'您是家长只能给自己家的小孩请假哟。','danger')
				return redirect(url_for('.send_leave'))

	try:
		banzhuren = student.classes.teacher.users
	except Exception, e:
		flash(u'该班级未设置班主任。不能请假','danger')
		return redirect(url_for('.send_leave'))
	
	ask = AskLeave.create(
		send_ask_user=current_user,
		ask_student = student,
		charge_ask_user = banzhuren,
		ask_start_time = ask_start_time,
		ask_end_time = ask_end_time,
		why = why
	)
	
	#此处增加微信通知班主任和家长
	try:
		teacher_wechat = student.classes.teacher.users.wechat_id
		msg_title = u'您的学生：%s发起了请假'%student.name
		msg_description = u'请假时间：%s-%s <br/>请假原因：%s,<br/>如同意请回复"ag%s",拒绝请回复"re%s",'%(str(ask_start_time),str(ask_end_time),why,ask.id,ask.id)
		wechat.message.send_text_card(teacher_wechat,msg_title,msg_description)
	except Exception, e:
		logger.error(str(e))

	try:
		teacher_wechat = student.parents.users.wechat_id
		msg_title = u'您的小孩：%s发起了请假'%student.name
		msg_description = u'请假时间：%s-%s <br/>请假原因：%s'%(str(ask_start_time),str(ask_end_time),why)
		wechat.message.send_text_card(teacher_wechat,msg_title,msg_description)
	except Exception, e:
		logger.error(str(e))

	

	flash(u'请假申请提交成功，请等待班主任(%s)的审核。'%banzhuren.first_name,'success')
	return redirect(url_for('.my_leave'))


#我的请假
@blueprint.route('/my_leave')
@templated()
@login_required
def my_leave():
	if current_user.student:
		askleave = AskLeave.query \
			.join(Student,Student.id==AskLeave.ask_users) \
			.filter(Student.user==current_user.id) \
			.order_by('charge_state').all()
	else:
		askleave  = []
	return dict(askleave=askleave)


@blueprint.route('/charge_leave')
@login_required
@permission_required(Permission.ALLOW_LEAVE)
def charge_leave():
	askleave = AskLeave.query.filter_by(charge_ask_user=current_user).order_by('charge_state').all()
	return render_template('users/charge_leave.html',askleave=askleave)


#我的发起的请假
@blueprint.route('/my_senf_leave')
@login_required
def my_senf_leave():
	askleave = AskLeave.query.filter_by(send_ask_user=current_user).order_by('charge_state').all()
	return render_template('users/my_senf_leave.html',askleave=askleave)


@blueprint.route('/charge_ask_leave/<int:id>')
@login_required
@permission_required(Permission.ALLOW_LEAVE)
def charge_ask_leave(id=0):
	ask_leave = AskLeave.query.get_or_404(id)
	
	if current_user != ask_leave.charge_ask_user or ask_leave.charge_state!=0:
		flash(u'非法操作','danger')
		return redirect(url_for('public.home'))

	ask_leave.update(charge_state=1,charge_time=dt.datetime.now())
	flash(u'您已同意该请假申请','success')

	return redirect(url_for('user.charge_leave'))




#自动注册 
@blueprint.route('/autoregister')
@oauth(scope='snsapi_base')
def autoregister():

	wechat_id = session.get('wechat_user_id','')
	
	if wechat_id:
		user = User.query.filter_by(wechat_id=session.get('wechat_user_id')).first()
	else:
		user = []
	logger.info('autoregister:%s'%wechat_id)
	logger.info('autoregister:user%s'%user)
	if user:
		login_user(user,True)
		return redirect(request.args.get('next') or url_for('public.home'))

	logger.info(u'微信ID:%s,已经进入'%wechat_id)

	choice_str = 'ABCDEFGHJKLNMPQRSTUVWSXYZ'
	username_str = ''
	password_str = ''
	str_time =  time.time()
	username_str = 'AU'
	username_str += str(int(int(str_time)*1.301))
	for i in range(2):
		username_str += random.choice(choice_str)

	for i in range(6):
		password_str += random.choice(choice_str)

	username = username_str
	password = password_str

	user = User.query.filter_by(username=username).first()
	if user is None:
		user = User.create(
			username=username,
			password=password,
			wechat_id=wechat_id,
		)
		login_user(user,True)
		return redirect(request.args.get('next') or url_for('public.home'))
	else:
		return redirect(url_for('.autoregister'))


@blueprint.route('/autologin/<string:name>')
def autologin(name=''):
	login_user(User.query.filter_by(username=name).first())
	return redirect(url_for('public.home'))



