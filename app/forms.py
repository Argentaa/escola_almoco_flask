from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired(), Length(min=4, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Sobrenome', validators=[DataRequired(), Length(max=100)])
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmar Senha', validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais.')])
    submit = SubmitField('Cadastrar')

    # Validadores customizados para verificar se username/email já existem
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Este nome de usuário já está em uso. Escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está em uso. Escolha outro.')

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember = BooleanField('Lembrar-me') # Para cookie persistente do Flask-Login
    submit = SubmitField('Login')

class AdminDateSelectionForm(FlaskForm):
    selected_date = DateField('Selecionar Data', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Ver Registros')
    
    def __init__(self, *args, **kwargs):
        super(AdminDateSelectionForm, self).__init__(*args, **kwargs)
        # Adiciona um atributo HTML type="date" para garantir formato correto
        self.selected_date.render_kw = {"type": "date"}
