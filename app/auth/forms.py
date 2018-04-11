# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/7 13:20
@Author  : zhaoguoqing600689
@File    : forms.py
@Software: PyCharm
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(),
                                                   Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                          0,
                                                          '用户名只能包含字母/数字/./下划线',
                                                          )])
    password = PasswordField('密码', validators=[
        DataRequired(),
        EqualTo('password2', message='两次密码必须一致!'),
    ])

    password2 = PasswordField('确认密码', validators=[
        DataRequired(),
    ])

    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被注册')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('确认新密码',
                              validators=[DataRequired()])
    submit = SubmitField('更新密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重置密码')


class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('重置密码')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮件地址', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('邮箱地址更新')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')
