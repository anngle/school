# -*- coding: utf-8 -*-
"""Public models."""
import datetime as dt

from school.user.models import User

from school.database import Column, Model, SurrogatePK, db, reference_col, relationship



class School(SurrogatePK, Model):
	"""学校列表
	表名称：schools
	parameters参数:
	name:学校名称
	active:是否激活 指是否可以添加下级操作
	state:是否可使用，暂定，无作用
	created_at:创建时间

	grades:外键年级表
	user:外键用户表,,这里设置校管员
	student_parents外键家长表
	doorkeepers这里外键到门卫表,用于判断门卫归属那个学校
	"""
	__tablename__ = 'schools'
	name = Column(db.String(80), nullable=False)
	active = Column(db.Boolean(), default=False)
	state = Column(db.Boolean(), default=True)
	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)
	# phone = Column(db.String(80), nullable=False)

	grades = relationship('Grade', backref='schools',lazy='joined')
	student_parents = relationship('StudentParent', backref='schools')
	doorkeepers = relationship('Doorkeeper', backref='schools')

	user = reference_col('users')
    



class Grade(SurrogatePK, Model):
	"""年级表
	表名称：grades
	parameters参数:
	name：年级名称
	created_at:创建时间

	classes_id外键

	school外键学校表
	"""
	__tablename__ = 'grades'
	name = Column(db.String(80), nullable=False)
	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)

	classes_id = relationship('Classes', backref='grade')

	school = reference_col('schools')
    


class Classes(SurrogatePK, Model):
	"""班级表
	表名称：classesd
	parameters参数:
	name班级名称

	student学生表

	charge_teachers班主任表
	grades年级表
	"""
	__tablename__ = 'classesd'
	name = Column(db.String(80), nullable=False)

	student = relationship('Student', backref='classes')
    
	charge_teachers = reference_col('charge_teacher')
	grades = reference_col('grades')



class Student(SurrogatePK, Model):
	"""学生表
	表名称：students
	parameters参数:
	number学号
	sex性别#男女 默认男
	name姓名
	img照片
	patriarch_name家长姓名
	id_number身份证号
	address住址
	phone联系电话

	user外键用户  默认空
	parent外键家长表  默认空
	classesd外键班级

	ask_student外键请假表	
	entry_exit 外键学生出入表

	"""
	__tablename__ = 'students'
	number = Column(db.String(80),nullable=False)
	sex = Column(db.Boolean(), default=True) #男女
	name = Column(db.String(80))
	img = Column(db.String(100))
	patriarch_name = Column(db.String(80))
	patriarch_phone = Column(db.String(50))
	id_number = Column(db.String(80))
	address = Column(db.String(200))
	phone = Column(db.String(50))

	user = reference_col('users')
	parent = reference_col('student_parents')
	classesd = reference_col('classesd')

	ask_student = relationship('AskLeave', backref='ask_student',primaryjoin="Student.id == AskLeave.ask_users")
	entry_exit = relationship('StudentEntryExit', backref='student')
  
    

class StudentParent(SurrogatePK, Model):
	"""学生家长表
	表名称：student_parents
	parameters参数:
	phone手机号
	name姓名
	id_number身份证号
	address住址
	child_name子女姓名
	child_number子女学号

	student外键学生表
	user外键用户表
	school_id外键学校表

	"""
	__tablename__ = 'student_parents'

	student = relationship('Student', backref='parents')
	

	phone = Column(db.String(80))
	name = Column(db.String(80))
	id_number = Column(db.String(80))
	address = Column(db.String(200))
	child_name = Column(db.String(80))
	child_number = Column(db.String(80))

	user = reference_col('users')
	school_id = reference_col('schools')

	

class ChargeTeacher(SurrogatePK, Model):
	"""教师表
	表名：charge_teacher
	parameters参数:
	number编码
	name姓名
	phone手机号
	id_number身份证号
	address住址
	tmp_classes_id 临时存储 classes_id班级字段  发送 微信通知到校管员 同意后变更为classes_id

	classes_id外键班级表，只要对应班级表后即可查询 所属学校、所属年级
	user外键用户表
	"""
	__tablename__ = 'charge_teacher'

	number = Column(db.String(80), nullable=False)
	phone = Column(db.String(80))
	name = Column(db.String(80))
	id_number = Column(db.String(80))
	address = Column(db.String(200))
	tmp_classes_id = Column(db.String(80))

	user = reference_col('users')

	student_entry_exit_id = relationship('Classes', backref='teacher',lazy='dynamic')
  

class Doorkeeper(SurrogatePK, Model):
	"""门卫表
	表名：doorkeepers
	parameters参数:
	number编号
	user外键用户表
	school_id这里外键到学校表  方式变更 原代码门卫发起请假代码需要更改

	"""
	__tablename__ = 'doorkeepers'

	number = Column(db.String(80), nullable=False)

	user = reference_col('users')

	school_id = reference_col('schools')


class AskLeave(SurrogatePK, Model):
	"""请假表
	表名：ask_leave
	parameters参数:
	send_users发起人 外键用户表
	ask_users请假人 外键学生表
	charge_users批准人 外键用户表
	ask_start_time请假开始事假
	ask_end_time请假结束时间
	leave_time离校事假
	back_leave_time回来时间
	charge_time批准时间
	charge_state是否批准 0发起  1批准  2拒绝 3完成 4已离校
	why请假原因
	created_at创建时间
	"""
	__tablename__ = 'ask_leave'
	send_users = reference_col('users')
	ask_users = reference_col('students')
	charge_users = reference_col('users')

	ask_start_time = Column(db.DateTime)
	ask_end_time = Column(db.DateTime)
	leave_time = Column(db.DateTime)
	back_leave_time = Column(db.DateTime,default=None)
	charge_time = Column(db.DateTime)
	charge_state = Column(db.Integer,default=0)
	why = Column(db.UnicodeText)
	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)



class StudentEntryExit(SurrogatePK,Model):
	"""
	学生出入表
	表名：student_entry_exits
	student_id 学生id 
	state 状态 0出 1入
	created_at 创建时间
	"""

	__tablename__ = 'student_entry_exits'

	student_id = reference_col('students')

	state = Column(db.Integer,default=0)
	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)






























