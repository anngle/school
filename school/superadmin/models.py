#coding=utf-8
from school.database import Column, Model, SurrogatePK, db, reference_col, relationship

import datetime as dt

#系统更新版本号
class SystemVersion(SurrogatePK,Model):

	__tablename__ = 'system_versions'
	#版本号
	number = Column(db.String(20))
	#标题
	title = Column(db.String(100))
	#描述
	summary = Column(db.String(200))
	#内容
	context = Column(db.UnicodeText)

	created_at = Column(db.DateTime, nullable=False, default=dt.datetime.now)
