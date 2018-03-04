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

	grades = relationship('Grade', backref='school',lazy='dynamic')
    
    
#年级
class Grade(SurrogatePK, Model):
	__tablename__ = 'grades'
	name = Column(db.String(80), nullable=False)
	#创建时间
	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)

	classes_id = relationship('Classes', backref='grade',lazy='dynamic')

	schools = reference_col('schools')
    

#班级
class Classes(SurrogatePK, Model):
	__tablename__ = 'classesd'
	name = Column(db.String(80), nullable=False)
	#学生
	students = reference_col('students')
	#班主任
	charge_teachers = reference_col('charge_teacher')
	#年级
	grades = reference_col('grades')


#学生
class Student(SurrogatePK, Model):
	__tablename__ = 'students'
	number = Column(db.String(80), nullable=False)
	sex = Column(db.Boolean(), default=True) #男女

	users = reference_col('users')

	classes_id = relationship('Classes', backref='student',lazy='dynamic')
    

#教师
class ChargeTeacher(SurrogatePK, Model):
	__tablename__ = 'charge_teacher'

	number = Column(db.String(80), nullable=False)

	users = reference_col('users')

	classes_id = relationship('Classes', backref='teacher',lazy='dynamic')
  

#门卫
class Doorkeeper(SurrogatePK, Model):
	__tablename__ = 'doorkeepers'

	number = Column(db.String(80), nullable=False)

	users = reference_col('users')








