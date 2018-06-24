# -*- coding: utf-8 -*-
"""Public models."""
import datetime as dt

from school.database import Column, Model, SurrogatePK, db, reference_col, relationship

from school.user.models import User

#学校列表
class School(SurrogatePK, Model):

	__tablename__ = 'schools'
	name = Column(db.String(80), nullable=False)
	#是否活动 指是否可以添加用户
	active = Column(db.Boolean(), default=False)
	#是否可使用
	state = Column(db.Boolean(), default=True)
	#创建时间
	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)

	grades = relationship('Grade', backref='schools',lazy='joined')

	user = relationship('User', backref='schools')

    
    
#年级
class Grade(SurrogatePK, Model):
	__tablename__ = 'grades'
	name = Column(db.String(80), nullable=False)
	#创建时间
	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)

	classes_id = relationship('Classes', backref='grade')

	school = reference_col('schools')
    

#班级
class Classes(SurrogatePK, Model):
	__tablename__ = 'classesd'
	name = Column(db.String(80), nullable=False)

	student = relationship('Student', backref='classes')
    
	#班主任
	charge_teachers = reference_col('charge_teacher')
	#年级
	grades = reference_col('grades')


#学生
class Student(SurrogatePK, Model):
	__tablename__ = 'students'
	number = Column(db.String(80),nullable=False)
	sex = Column(db.Boolean(), default=True) #男女
	name = Column(db.String(80))
	img = Column(db.String(80))

	user = reference_col('users')
	#家长
	parent = reference_col('student_parents')
	#班级
	classesd = reference_col('classesd')

	#请假人
	ask_student = relationship('AskLeave', backref='ask_student',primaryjoin="Student.id == AskLeave.ask_users")
    

#学生家长表
class StudentParent(SurrogatePK, Model):
	__tablename__ = 'student_parents'

	student = relationship('Student', backref='parents')

	phone = Column(db.String(80))
	name = Column(db.String(80))

	user = reference_col('users')
	

#教师
class ChargeTeacher(SurrogatePK, Model):
	__tablename__ = 'charge_teacher'

	number = Column(db.String(80), nullable=False)

	phone = Column(db.String(80))
	name = Column(db.String(80))

	user = reference_col('users')

	classes_id = relationship('Classes', backref='teacher',lazy='dynamic')
  

#门卫
class Doorkeeper(SurrogatePK, Model):
	__tablename__ = 'doorkeepers'

	number = Column(db.String(80), nullable=False)

	user = reference_col('users')


#请假列表
class AskLeave(SurrogatePK, Model):
	__tablename__ = 'ask_leave'
	#发起人
	send_users = reference_col('users')
	#请假人
	ask_users = reference_col('students')
	#批准人
	charge_users = reference_col('users')
	#请假开始事假
	ask_start_time = Column(db.DateTime)
	#请假结束时间
	ask_end_time = Column(db.DateTime)
	#离校事假
	leave_time = Column(db.DateTime)
	#回来时间`
	back_leave_time = Column(db.DateTime,default=None)
	#批准时间`
	charge_time = Column(db.DateTime)
	#是否批准 0发起  1批准  2拒绝 3完成 4已离校
	charge_state = Column(db.Integer,default=0)
	#请假原因
	why = Column(db.UnicodeText)
	#创建时间
	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)






