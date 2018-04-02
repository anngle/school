# -*- coding: utf-8 -*-
"""Superadmin views."""
from flask import Blueprint, render_template,request,flash,redirect,url_for,current_app
from .models import SystemVersion
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import xlrd,sys,datetime,os

from ..public.models import School,Grade,Classes,Student,StudentParent
from ..user.models import User,Role
from school.utils import create_file_name,allowed_file,templated
from school.database import db

from log import logger

reload(sys)
sys.setdefaultencoding("utf-8")


blueprint = Blueprint('superadmin', __name__, url_prefix='/superadmin')



@blueprint.route('/')
@templated()
def home():
	return dict()


@blueprint.route('/add_school')
@templated()
def add_school():
    return dict()


@blueprint.route('/add_school',methods=['POST'])
@templated()
def add_school_post():
	name = request.form.get('name','')
	if name:
		School.create(name=name)
	flash(u'添加成功。','success')

	return redirect(url_for('.home'))


@blueprint.route('/add_grade/<int:id>')
@templated()
def add_grade(id=0):
	return dict(school_id=id)


@blueprint.route('/add_grade',methods=['POST'])
def add_grade_post():
	school_id = request.form.get('school_id','0')
	name = request.form.get('name','0')
	school =  School.query.get_or_404(school_id)
	if name:
		Grade.create(name=name,schools=school)
		flash(u'添加成功','success')

	return redirect(url_for('.home'))


@blueprint.route('/add_classes/<int:id>')
@templated()
def add_classes(id=0):
	return dict(grade_id=id)


@blueprint.route('/add_classes',methods=['POST'])
def add_classes_post():
	grade_id = request.form.get('grade_id','0')
	name = request.form.get('name','0')
	grade =  Grade.query.get_or_404(grade_id)
	
	if name:
		Classes.create(name=name,grade=grade)
		flash(u'添加成功','success')

	return redirect(url_for('.home'))


@blueprint.route('/all_school')
@templated()
def all_school():
	return dict(school=School.query.order_by(desc('id')).all())


@blueprint.route('/all_version')
@templated()
def all_version():
	return dict(version=SystemVersion.query.order_by(desc('id')).all())


@blueprint.route('/all_users')
@templated()
def all_users():
	users = User.query\
		.with_entities(\
			User.id,\
			User.username,\
			User.first_name,\
			User.phone,\
			User.wechat_id,\
			Role.name
			)\
		.join(Role,Role.id==User.role)\
		.order_by(desc('id'))\
		.all()
	# for i in users:
	# 	print i.wechat_id
	return dict(users=users)


@blueprint.route('/all_students')
@templated()
def all_students():
	students = Student.query\
		.with_entities(\
			Student.id,\
			Student.number,\
			Student.sex,\
			Student.user,\
			Student.parent,\
			Student.classesd,\
			)\
		.all()
	logger.info(u'所有学生')
	return dict(students=students)


#所有老师
@blueprint.route('/all_teacher')
@templated()
def all_teacher():
	return dict()



@blueprint.route('/add_version',methods=['GET'])
def add_version():
	version = SystemVersion.query.order_by(desc('id')).first()
	return render_template('superadmin/add_version.html',version=version)


@blueprint.route('/add_version',methods=['POST'])
def add_version_post():
	SystemVersion.create(
		number=request.form.get('number',' '),
		title=request.form.get('title',' '),
		summary=request.form.get('summary',' '),
		context=request.form.get('context',' '),	
	)
	flash(u'添加完成.','success')
	return redirect(url_for('.all_version'))


@blueprint.route('/show_classes/<int:id>',methods=['GET'])
def show_classes(id=0):
	classes = Classes.query.get_or_404(id)
	return render_template('superadmin/show_classes.html',classes=classes)

@blueprint.route('/set_teachers',methods=['POST'])
def set_teachers():
	classes_id = request.form.get('classes_id','0')

	phone = request.form.get('phone','')
	user = User.query.filter_by(phone=phone).first()
	if not user:
		flash(u'设置班主任失败，手机号码不正确.','danger')
		return redirect(url_for('.show_classes',id=classes_id))
	
	classes = Classes.query.get_or_404(classes_id)
	
	classes.update(teacher=user.charge_teacher)
	flash(u'设置班主任成功.','success')
	return redirect(url_for('.show_classes',id=classes_id))


@blueprint.route('/add_student',methods=['POST'])
def add_student():
	files = request.files['file']
	classes_id = request.form.get('classes_id','0')
	if not files:
		flash(u'请选择文件')
		return redirect(url_for('.show_classes',id=classes_id))
	classes = Classes.query.get_or_404(classes_id)

	try:
		filename = secure_filename(files.filename)
		filename = create_file_name(files)
		dataetime = datetime.datetime.today().strftime('%Y%m%d')
		file_dir = 'superadmin/excel/%s/'%dataetime
		if not os.path.isdir(current_app.config['UPLOADED_PATH']+file_dir):
			os.makedirs(current_app.config['UPLOADED_PATH']+file_dir)
		if  allowed_file(files.filename):
			files.save(current_app.config['UPLOADED_PATH'] +file_dir+filename)
				
		filedata = xlrd.open_workbook(current_app.config['UPLOADED_PATH'] +file_dir+filename,encoding_override='utf-8')
		table = filedata.sheets()[0]
		message =""
		try:
			if table.col(0)[0].value.strip() != u'学号':
				message = u"第一行名称必须叫‘学号’，请返回修改"
			if table.col(1)[0].value.strip() != u'姓名':
				message = u"第二行名称必须叫‘姓名’，请返回修改"
			if table.col(2)[0].value.strip() != u'性别':
				message = u"第三行名称必须叫‘性别’，请返回修改"

			if message !="":
				flash(message)
				return redirect(url_for('.show_classes',id=classes_id))
		except Exception, e:
			flash(u'excel文件操作错误：%s'%str(e))
			return redirect(url_for('.show_classes',id=classes_id))

		nrows = table.nrows #行数
		table_data_list =[]
		for rownum in range(1,nrows):
			if table.row_values(rownum):
				table_data_list.append(table.row_values(rownum))

		classes = Classes.query.get_or_404(classes_id)
		if table_data_list:
			for i in table_data_list:
				if i[2]==u'男':
					sex = True
				else:
					sex = False
				db.session.add(Student(number=i[0],name=i[1],sex=sex,classes=classes))
			db.session.commit()
		flash(u'添加完成')
		return redirect(url_for('.show_classes',id=classes_id))
	except Exception, e:
		flash(u'excel文件读取错误：%s'%str(e))
		return redirect(url_for('.show_classes',id=classes_id))
	



