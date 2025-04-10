from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from .forms import LoginForm, RegistrationForm
from .models import User
from . import db, bcrypt

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index')) # Redireciona se já logado
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            is_staff=False # Novos usuários são sempre alunos
        )
        db.session.add(user)
        db.session.commit()
        flash('Sua conta foi criada com sucesso! Você já pode fazer login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Cadastro', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index')) # Redireciona se já logado
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login realizado com sucesso!', 'success')
            # Redireciona para a página que o usuário tentava acessar ou para a index
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login falhou. Verifique usuário e senha.', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@bp.route('/logout')
@login_required # Só pode deslogar quem está logado
def logout():
    logout_user()
    flash('Você saiu da sua conta.', 'info')
    return redirect(url_for('auth.login'))