from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from datetime import date, datetime
from .models import LunchRegistration, User
from .forms import AdminDateSelectionForm
from .utils import admin_required # Importa o decorador
from . import db

bp = Blueprint('admin', __name__)

@bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required # Garante que só admin acesse
def dashboard():
    form = AdminDateSelectionForm(request.args) # Preenche com dados da query string GET
    selected_date_obj = date.today() # Data padrão é hoje

    try:
        if form.validate(): # Valida se a data veio no formato correto via GET
            selected_date_obj = form.selected_date.data
        elif 'selected_date' in request.args: # Se veio mas falhou na validação do form
            # Tenta converter a data manualmente
            try:
                date_str = request.args.get('selected_date')
                # Tenta diferentes formatos comuns
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
                    try:
                        selected_date_obj = datetime.strptime(date_str, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    # Se nenhum formato funcionar
                    flash('Formato de data inválido. Usando data de hoje.', 'warning')
            except Exception:
                flash('Formato de data inválido. Usando data de hoje.', 'warning')
    except Exception as e:
        flash(f'Erro ao processar a data: {str(e)}. Usando data de hoje.', 'warning')

    # Busca registros para a data (inclui dados do aluno via join implícito do backref)
    registrations = LunchRegistration.query.filter_by(
        lunch_date=selected_date_obj
    ).join(User).order_by(User.first_name, User.last_name).all()

    student_count = len(registrations)

    # Preenche o formulário com a data usada para exibição no template
    form.selected_date.data = selected_date_obj

    return render_template('admin/dashboard.html',
                           title='Painel Admin',
                           form=form, # Passa o formulário para o template
                           selected_date=selected_date_obj,
                           registrations=registrations,
                           student_count=student_count)
