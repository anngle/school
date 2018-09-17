#coding=utf-8
from school.database import Column, Model, SurrogatePK, db, reference_col, relationship

import datetime as dt


class SystemVersion(SurrogatePK,Model):
	"""系统更新版本号列表 暂定不用了  
	表名：system_versions
	parameters参数:
	number版本号
	title标题
	summary描述
	context内容
	created_at创建时间
	"""
	__tablename__ = 'system_versions'
	number = Column(db.String(20))
	title = Column(db.String(100))
	summary = Column(db.String(200))
	context = Column(db.UnicodeText)
	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)
