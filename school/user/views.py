# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, url_for, current_app, redirect,request,flash
from flask_login import login_required,login_user,current_user
import time,random
from sqlalchemy import desc

from .models import User,Role,Permission
from ..public.models import School,ChargeTeacher
from ..decorators import permission_required


blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html')

@blueprint.route('/set_roles')
@login_required
def set_roles():
	school = School.query.filter_by(active=True).order_by(desc('id')).all()
	return render_template('users/set_roles.html',school=school)


@blueprint.route('/set_roles',methods=["POST"])
@login_required
def set_roles_post():
	school_id = request.form.get('school_id','0')
	role_id = request.form.get('school_id','0')
	number = request.form.get('number','0')
	verify = request.form.get('verify','0')
	phone = request.form.get('phone','0')
	school = School.query.get_or_404(school_id)
	#教师
	if int(role_id) ==1:
		if verify != current_app.config['REGISTERVERIFY']:
			flash(u'校验码错误','danger')
			return redirect(url_for('public.home'))
		role = Role.query.filter_by(name='Teacher').first()
		current_user.update(phone=phone,roles=role)
		ChargeTeacher.create(number=number,teacher=current_user)
		flash(u'您已设置角色为“教师”。','success')
	
	return redirect(url_for('public.home'))


@blueprint.route('/send_leave')
@login_required
@permission_required(Permission.LEAVE)
def send_leave():
	return render_template('users/send_leave.html')



#自动注册 
@blueprint.route('/autoregister')
# @oauth(scope='snsapi_userinfo')
def autoregister():
	try:
		wechat_id = session.get('wechat_user_id','')
	except Exception, e:
		wechat_id = ''
	if wechat_id:
		user = User.query.filter_by(wechat_id=session.get('wechat_user_id')).first()
	else:
		user = []
	if user:
		login_user(user,True)
		return redirect(request.args.get('next') or url_for('public.home'))

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
		# return 'ok'
	else:
		return redirect(url_for('.autoregister'))


@blueprint.route('/autologin/<string:name>')
def autologin(name=''):
	login_user(User.query.filter_by(username=name).first())
	return redirect(url_for('public.home'))



