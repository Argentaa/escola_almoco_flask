import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from datetime import datetime
# Carrega variáveis de ambiente do arquivo .env na raiz do projeto
load_dotenv()

# Inicialização das extensões (sem app ainda)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

# Configuração do Flask-Login
login_manager.login_view = 'auth.login' # Rota para redirecionar se @login_required falhar
login_manager.login_message_category = 'info' # Categoria de mensagem flash
login_manager.login_message = 'Por favor, faça login para acessar esta página.'

def create_app():
    """Cria e configura a instância da aplicação Flask."""
    app = Flask(__name__, instance_relative_config=False) # instance_relative_config=False se não usar instance/config.py

    # Carrega configuração da classe Config (usa fallback para SQLite se DATABASE_URI não estiver definido)
    app.config.from_object('instance.config.Config')

    # Inicializa extensões com a app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app) # Proteção CSRF global

    # Importar modelos antes de criar tabelas ou blueprints
    from . import models

    # Registrar Blueprints (grupos de rotas)
    from .routes_auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from .routes_student import bp as student_bp
    app.register_blueprint(student_bp) # Sem prefixo, para rotas como /dashboard

    from .routes_admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.context_processor
    def inject_now():
        """Injeta a variável 'now' (com a data/hora atual) no contexto do template."""
        # Usamos datetime.now() para obter a hora local do servidor,
        # o que é geralmente aceitável para um ano de copyright.
        # Para lógica de negócio, datetime.utcnow() é frequentemente preferível.
        return {'now': datetime.now()}
    # <<< FIM DA ADIÇÃO >>>
    
    # Definir a rota raiz (página inicial)
    @app.route('/')
    def index():
        # Poderia renderizar uma página inicial estática
        # ou redirecionar baseado no login (similar ao home_view do Django)
        from flask_login import current_user
        from flask import redirect, url_for, render_template
        if current_user.is_authenticated:
             if current_user.is_staff:
                 return redirect(url_for('admin.dashboard'))
             else:
                 return redirect(url_for('student.dashboard'))
        # return render_template('home.html') # Se tiver uma página home
        return redirect(url_for('auth.login')) # Ou redireciona para login se não logado


    return app
