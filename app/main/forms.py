# -*- coding: utf-8 -*-
"""
@Time    : 2018/2/6 10:51
@Author  : zhaoguoqing600689
@File    : forms.py
@Software: PyCharm
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from flask_ckeditor.fields import CKEditorField
from ..models import Role, User


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('介绍')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('电子邮件', validators=[
        DataRequired(),
        Length(1, 64),
        Email(),
    ])
    username = StringField('用户姓名', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
               0,
               'Username must have only letters, numbers, dot or underscores',
               )])
    confirmed = BooleanField('是否确认')
    role = SelectField('用户角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = StringField('位置', validators=[Length(0, 64)])
    about_me = TextAreaField('介绍')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经注册.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被占用.')


class PostForm(FlaskForm):
    # body = PageDownField("MarkDown", validators=[DataRequired()])
    body = CKEditorField("MarkDown", validators=[DataRequired()])
    submit = SubmitField('提交')


class CommentForm(FlaskForm):
    body = PageDownField('评论', validators=[DataRequired()])
    submit = SubmitField('提交')
