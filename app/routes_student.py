from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from datetime import date, timedelta, datetime
from .models import LunchRegistration
from . import db

bp = Blueprint('student', __name__)

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_staff:
        # Redireciona admin se tentar acessar painel de aluno
        return redirect(url_for('admin.dashboard'))

    weekday_map = {
        0: 'Segunda-feira',
        1: 'Terça-feira',
        2: 'Quarta-feira',
        3: 'Quinta-feira',
        4: 'Sexta-feira',
        5: 'Sábado',
        6: 'Domingo'
    }

    today = date.today()
    start_date = today
    end_date = today + timedelta(days=6)
    possible_dates = [start_date + timedelta(days=i) for i in range(7)]

    # Busca registros existentes do aluno logado neste período
    registrations_query = LunchRegistration.query.filter(
        LunchRegistration.student == current_user,
        LunchRegistration.lunch_date.between(start_date, end_date)
    ).all()
    registered_dates = {reg.lunch_date for reg in registrations_query} # Conjunto para busca rápida

    days_data = []
    for dt in possible_dates:
        if dt.weekday() in [5, 6]:
            continue  # pula sábado e domingo
        days_data.append({
            'date': dt,
            'is_registered': dt in registered_dates,
            'weekday_pt': weekday_map[dt.weekday()]
        })

    return render_template('student/dashboard.html', title='Meu Painel', days=days_data)


@bp.route('/mark_lunch/<string:lunch_date_str>', methods=['POST'])
@login_required
def mark_lunch(lunch_date_str):
    # Proteção CSRF é feita globalmente pelo Flask-WTF se o form incluir o token,
    # ou podemos adicionar CSRFProtect(bp) se necessário para POSTs sem form Flask-WTF
    if current_user.is_staff:
        flash("Administradores não podem marcar almoço.", 'warning')
        return redirect(url_for('admin.dashboard'))

    try:
        lunch_date_obj = date.fromisoformat(lunch_date_str)
    except ValueError:
        flash("Data inválida.", 'danger')
        return redirect(url_for('student.dashboard'))

    # Validação da Regra de 1 Semana
    today = date.today()
    max_date = today + timedelta(days=6)

    if not (today <= lunch_date_obj <= max_date):
        flash(f"Só é possível marcar almoço entre {today.strftime('%d/%m')} e {max_date.strftime('%d/%m')}.", 'warning')
        return redirect(url_for('student.dashboard'))

    # Verifica se já existe registro para essa data e aluno
    existing_registration = LunchRegistration.query.filter_by(
        student=current_user,
        lunch_date=lunch_date_obj
    ).first()

    if existing_registration:
        # Já existe, então remove (desmarca)
        db.session.delete(existing_registration)
        db.session.commit()
        flash(f"Marcação para {lunch_date_obj.strftime('%d/%m/%Y')} removida.", 'info')
    else:
        # Não existe, então cria (marca)
        new_registration = LunchRegistration(student=current_user, lunch_date=lunch_date_obj)
        db.session.add(new_registration)
        db.session.commit()
        flash(f"Almoço para {lunch_date_obj.strftime('%d/%m/%Y')} marcado!", 'success')

    return redirect(url_for('student.dashboard'))
