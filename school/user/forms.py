# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField,SelectField,SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from .models import User
from ..public.models import School


class RegisterForm(FlaskForm):
    """Register form."""

    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email',
                        validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Verify password',
                            [DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('Username already registered')
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Email already registered')
            return False
        return True


class SendLeaveForm(FlaskForm):
    number = StringField(u'请假人学号',validators=[DataRequired(), Length(min=1, max=25)])
    start_time = StringField(u'请假开始时间',validators=[DataRequired(), Length(min=3, max=25)])
    end_time = StringField(u'请假结束时间',validators=[DataRequired(), Length(min=3, max=25)])
    why = StringField(u'请假事由',validators=[DataRequired(), Length(min=1, max=25)])


class RegisterRoleForm(FlaskForm):
    """
    其他用户注册填写的信息  信息保存在users表

    """

    name = StringField('真实姓名',validators=[DataRequired(), Length(min=2, max=10,message='姓名长度不正确')])
    phone = StringField('手机号码',validators=[DataRequired(),Length(min=11, max=11,message='手机号码格式不正确')])
    id_number = StringField('身份证号',validators=[DataRequired(), Length(min=15, max=18,message='请输入有效的身份证号')])
    address = StringField('家庭住址',validators=[Length(min=0, max=200,message='请输入有效的居住地址')])
    car_number = StringField('车牌号码',validators=[Length(min=0, max=50,message='请输入有效的车牌号')])
    submit = SubmitField('提交信息',render_kw={'class':'btn btn-primary btn-lg btn-block'})
    
    def __init__(self, *args, **kwargs):

        super(RegisterRoleForm, self).__init__(*args, **kwargs)
        

class RegisterStudentForm(FlaskForm):
    school_id = SelectField(u'学校名称',choices=[(-1,u'请选择学校')],coerce=int)

    name = StringField('真实姓名',validators=[DataRequired(), Length(min=2, max=10)])
    id_car = StringField('学号',validators=[DataRequired(), Length(min=2, max=20)])
    id_number = StringField('身份证号',validators=[DataRequired(), Length(min=15, max=18)])
    address = StringField('家庭住址')
    phone = StringField('手机号(可空)',validators=[Length(min=11, max=11)])
    parent_name = StringField('家长姓名',validators=[DataRequired(),Length(min=2, max=10)])
    parent_phone = StringField('家长联系电话',validators=[DataRequired(),Length(min=11, max=11)])
    submit = SubmitField('提交',render_kw={'class':'btn btn-primary btn-lg btn-block'})

    def __init__(self, *args, **kwargs):

        super(RegisterStudentForm, self).__init__(*args, **kwargs)
        self.school_id.choices = self.school_id.choices+[(obj.id, obj.name) for obj in School.query.order_by('id').all()]
    


class RegisterRoleTracherForm(FlaskForm):

    name = StringField('真实姓名',validators=[DataRequired(), Length(min=2, max=10)])
    id_car = StringField('教师编号',validators=[DataRequired(), Length(min=2, max=20)])
    id_number = StringField('身份证号',validators=[DataRequired(), Length(min=15, max=18)])
    address = StringField('家庭住址')
    phone = StringField('手机号码',validators=[Length(min=11, max=11)])
    submit = SubmitField('提交',render_kw={'class':'btn btn-primary btn-lg btn-block'})
    
    
    def __init__(self, *args, **kwargs):

        super(RegisterRoleTracherForm, self).__init__(*args, **kwargs)
        


class RegisterRoleParentForm(FlaskForm):

    name = StringField('真实姓名',validators=[DataRequired(), Length(min=2, max=10,message='输入不正确')])
    id_number = StringField('身份证号',validators=[DataRequired(), Length(min=15, max=18,message='输入不正确')])
    address = StringField('家庭住址')
    phone = StringField('手机号码',validators=[Length(min=11, max=11,message='输入不正确')])
    child_name = StringField('子女姓名',validators=[DataRequired(), Length(min=2, max=10,message='输入不正确')])

    school_id = SelectField(u'所在学校',choices=[(-1,u'请选择学校')],coerce=int,validators=[DataRequired(message='请选择学校')])

    child_number = StringField('子女学号',validators=[DataRequired(), Length(min=2, max=20,message='输入不正确')])

    submit = SubmitField('提交',render_kw={'class':'btn btn-primary btn-lg btn-block'})
    
    def __init__(self, *args, **kwargs):

        super(RegisterRoleParentForm, self).__init__(*args, **kwargs)
        self.school_id.choices = self.school_id.choices+[(obj.id, obj.name) for obj in School.query.order_by('id').all()]
    






