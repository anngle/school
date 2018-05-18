# -*- coding: utf-8 -*-
"""Superadmin views."""
from flask import Blueprint, render_template,request,flash,redirect,url_for,current_app, Response,jsonify, abort
from .models import SystemVersion
from flask_login import current_user,login_required
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from werkzeug.datastructures import Headers
import xlrd, sys, datetime, os, xlsxwriter,mimetypes

from ..public.models import School,Grade,Classes,Student,StudentParent,AskLeave
from ..user.models import User,Role
from school.utils import create_file_name,allowed_file,templated,gen_rnd_filename,allowed_img_lambda
from school.database import db
from school.decorators import admin_required,permission_required
from school.extensions import csrf_protect
from school.user.models  import Permission
from log import logger

from io import StringIO,BytesIO

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


blueprint = Blueprint('superadmin', __name__, url_prefix='/superadmin')



@blueprint.route('/')
@templated()
def home():
	if not current_user.is_authenticated:
		return redirect(url_for('user.user_login',next=request.endpoint))
	
	if not current_user.can(Permission.ADMINISTER):
		abort(401)

	return  dict()


@blueprint.route('/add_school')
@templated()
@login_required
@admin_required
def add_school():
    return dict()


@blueprint.route('/add_school',methods=['POST'])
@templated()
@login_required
@admin_required
def add_school_post():
	name = request.form.get('name','')
	if name:
		School.create(name=name)
	flash(u'添加成功。','success')

	return redirect(url_for('.home'))


@blueprint.route('/add_grade/<int:id>')
@templated()
@login_required
@admin_required
def add_grade(id=0):
	return dict(school_id=id)


@blueprint.route('/add_grade',methods=['POST'])
@login_required
@admin_required
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
@login_required
@admin_required
def add_classes(id=0):
	return dict(grade_id=id)


@blueprint.route('/add_classes',methods=['POST'])
@login_required
@admin_required
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
@login_required
@admin_required
def all_school():
	return dict(school=School.query.order_by(desc('id')).all())


@blueprint.route('/all_version')
@templated()
@login_required
@admin_required
def all_version():
	return dict(version=SystemVersion.query.order_by(desc('id')).all())


@blueprint.route('/all_users')
@templated()
@login_required
@admin_required
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
		.order_by(desc(User.id))\
		.all()
	return dict(users=users)


@blueprint.route('/all_students')
@templated()
@login_required
@admin_required
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
	
	return dict(students=students)


#所有老师
@blueprint.route('/all_teacher')
@templated()
@login_required
@admin_required
def all_teacher():
	return dict()



@blueprint.route('/add_version',methods=['GET'])
@login_required
@admin_required
def add_version():
	version = SystemVersion.query.order_by(desc('id')).first()
	return render_template('superadmin/add_version.html',version=version)


@blueprint.route('/add_version',methods=['POST'])
@login_required
@admin_required
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
@templated()
@login_required
@admin_required
def show_classes(id=0):
	classes = Classes.query.get_or_404(id)
	return dict(classes=classes)

@blueprint.route('/set_teachers',methods=['POST'])
@login_required
@admin_required
def set_teachers():
	classes_id = request.form.get('classes_id','0')

	phone = request.form.get('phone','')
	user = User.query.filter_by(phone=phone).first()
	if not user:
		flash(u'设置班主任失败，手机号码不正确.','danger')
		return redirect(url_for('.show_classes',id=classes_id))
	
	classes = Classes.query.get_or_404(classes_id)
	classes.update(teacher=user.teacher)
	flash(u'设置班主任成功.','success')
	return redirect(url_for('.show_classes',id=classes_id))


@blueprint.route('/add_student',methods=['POST'])
@login_required
@admin_required
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
		

		filedata = xlrd.open_workbook(current_app.config['UPLOADED_PATH'] +file_dir+filename)
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
		except Exception as e:
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
	except Exception as e:
		flash(u'excel文件读取错误：%s'%str(e))
		return redirect(url_for('.show_classes',id=classes_id))
	

@blueprint.route('/delete_users/<int:id>')
@login_required
@admin_required
def delete_users(id=0):
	users = User.query.get_or_404(id)
	users.delete()
	flash(u'删除成功。')
	return redirect(url_for('.all_users'))


@blueprint.route('/all_parent')
@templated()
@login_required
@admin_required
def all_parent():
	return dict(parent=StudentParent.query.order_by(desc('id')).all())


#所有请假信息 toexcel
@blueprint.route('/all_ask_leave')
@blueprint.route('/all_ask_leave/<toexcel>')
@templated()
@login_required
@admin_required
def all_ask_leave(toexcel=''):
	leave = AskLeave.query\
		.with_entities(\
			AskLeave.ask_start_time,\
			AskLeave.ask_end_time,\
			AskLeave.back_leave_time,\
			AskLeave.charge_time,\
			AskLeave.charge_state,\
			AskLeave.why,\
			AskLeave.created_at,\
			Student.name,\
			Grade.name,\
			School.name,\
			Classes.name,\
			)\
		.join(Student,Student.id==AskLeave.ask_users)\
		.join(Classes,Classes.id==Student.classesd)\
		.join(Grade,Grade.id==Classes.grades)\
		.join(School,School.id==Grade.school)\
		.order_by(desc(AskLeave.id))\
		.limit(500)\
		.all()
	if not toexcel:
		return dict(leave=leave)
	else:
		try:			
			title_shipment = [u'学校',u'年级',u'班级',u'学生',u'请假时间',u'归来时间',u'批准时间',u'请假原因',u'状态',u'创建时间']
			shijian = datetime.datetime.now()

			response = Response()
			response.status_code = 200

			output = BytesIO()
			wb = xlsxwriter.Workbook(output, {'in_memory': True})
			ws = wb.add_worksheet(u'请假数据表')

			for i,x in enumerate(title_shipment):
				ws.write(0,i,x)

			for i,x in enumerate(leave):
				ws.write(i+1,0,x[9])
				ws.write(i+1,1,x[8])
				ws.write(i+1,2,x[10])
				ws.write(i+1,3,x[7])
				ws.write(i+1,4,str(x[0])+u"到"+str(x[1]))
				ws.write(i+1,5,x[2])
				ws.write(i+1,6,x[3])
				ws.write(i+1,7,x[5])
				if x[4] == 0:
					ws.write(i+1,8,'等待确认')
				if x[4] == 1:
					ws.write(i+1,8,'已批准')
				if x[4] == 2:
					ws.write(i+1,8,'已拒绝')
				if x[4] == 3:
					ws.write(i+1,8,'已完成')
				if x[4] == 4:
					ws.write(i+1,8,'已离校')

				ws.write(i+1,9,str(x[6]))

			wb.close()
			output.seek(0)
			response.data = output.read()

			file_name = u'all_ask_leave{}.xlsx'.format(datetime.datetime.now())
			mimetype_tuple = mimetypes.guess_type(file_name)

			response_headers = Headers({
				'Pragma': "public",  # required,
				'Expires': '0',
				'Charset': 'UTF-8',
				'Cache-Control': 'must-revalidate, post-check=0, pre-check=0',
				'Cache-Control': 'private',  # required for certain browsers,
				'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
				'Content-Disposition': 'attachment; filename=\"%s\";' % file_name,
				'Content-Transfer-Encoding': 'binary',
				'Content-Length': len(response.data)
			})

			if not mimetype_tuple[1] is None:
				response.update({
					'Content-Encoding': mimetype_tuple[1]
				})

			response.headers = response_headers
			# response.set_cookie('fileDownload', 'true', path='/')
			return response



		except Exception as e:
			return str(e)

		
#更新学校状态
@blueprint.route('/change_active/<int:id>')
@login_required
@admin_required
def change_active(id=0):
	school = School.query.get_or_404(id)
	if school.active:
		school.update(active=False)
	else:
		school.update(active=True)
	flash(u'状态更新成功。')
	return redirect(url_for('.all_school'))


#上传更新学生头像
@csrf_protect.exempt		
@blueprint.route('/submit_students_img',methods=['POST'])
@login_required
@admin_required
def submit_students_img():
    f = request.files.get('file')
    filename = allowed_img_lambda(f.filename)
    filename = gen_rnd_filename()+'.'+f.filename.rsplit('.', 1)[1]

    dataetime = datetime.datetime.today().strftime('%Y%m%d')
    file_dir = '%s/%s/'%('0',dataetime)
    
    if not os.path.isdir(current_app.config['STUDENTS_IMG']+file_dir):
        os.makedirs(current_app.config['STUDENTS_IMG']+file_dir)
    
    f.save(current_app.config['STUDENTS_IMG'] +file_dir+filename)
    filename = file_dir+filename

    student = Student.query.get(request.form.get('id'))
    if  student:
    	student.update(img=filename)
    return jsonify({'success':[filename,request.form.get('id')]})
		


