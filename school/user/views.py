# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, url_for
from flask_login import login_required,login_user
import time,random
blueprint = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """List members."""
    return render_template('users/members.html')




#108.333286,22.841502
#自动注册 微信登录
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
		user = User(username=username,password=password,wechat_id=wechat_id)
		db.session.add(user)
		db.session.commit()
		login_user(user,True)
		return redirect(request.args.get('next') or url_for('public.home'))
	else:
		return redirect(url_for('.autoregister'))


@blueprint.route('/autologin/<string:name>')
def autologin(name=''):
	login_user(User.query.filter_by(username=name).first())
	return redirect(url_for('public.home'))



