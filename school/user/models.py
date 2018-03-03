# -*- coding: utf-8 -*-
"""User models."""
import datetime as dt

from flask_login import UserMixin,AnonymousUserMixin

from school.database import Column, Model, SurrogatePK, db, reference_col, relationship
from school.extensions import bcrypt,login_manager

#权限常量
class Permission:
    LEAVE = 0x01   #请假
    ALLOW_LEAVE = 0x02 #批准请假

    ADMINISTER = 0x8000  #管理员权限

"""
#用户角色：

学生:发起请假 0x01
门卫:发起请假 0x01
家长:发起请假 0x01

教师:批准请假   0x02

"""

class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    name = Column(db.String(80), unique=True, nullable=False)
    permissions = db.Column(db.Integer)
    default = db.Column(db.Boolean, default=False, index=True)

    user = relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({name})>'.format(name=self.name)

    @staticmethod
    def insert_roles():
        roles = {
            'Students': (Permission.LEAVE,True), #学生
            'Doorkeeper': (Permission.LEAVE,False),#门卫
            'Patriarch': (Permission.LEAVE,False), #家长
            'Principal': (0xfff, False), #校长
            'ADMIN': (0xffff, False) #管理员
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    wechat_id = Column(db.String(80), nullable=True)

    role = reference_col('roles')

    #教师表 一对一
    charge_teacher = relationship('ChargeTeacher', backref='teacher',uselist=False)
    #学生表
    students = relationship('Student', backref='student',lazy='dynamic')

    

    def __init__(self, username, email=None, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

        if self.role is None:
            if self.username == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xffff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username!r})>'.format(username=self.username)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser



