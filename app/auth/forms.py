from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginFrom(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(), Length(1,64)])
    password = PasswordField("密码", validators=[DataRequired()])
    remember_me = BooleanField("保持登录")
    submit = SubmitField("登录")


class RegistrationFrom(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1,64),
                                              Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                     '用户名必须由字母，数字，点或'
                                                     '下划线组成')])
    password = PasswordField('密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须匹配')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_username(self, filed):
        if User.query.filter_by(username=filed.data).first():
            raise ValidationError('用户名已存在')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('password2', message='密码必须匹配.')])
    password2 = PasswordField("确认新密码", validators=[DataRequired()])
    submit = SubmitField("更新密码")


class PasswordResetRequestForm(FlaskForm):
    username = StringField("用户名", validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField("重置密码")


class PasswordResetForm(FlaskForm):
    password = PasswordField("新密码", validators=[
        DataRequired(), EqualTo('password2', message="密码必须匹配")])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('重置密码')


