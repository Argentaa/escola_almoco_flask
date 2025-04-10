from app import create_app, db # Importa a factory e o db
from app.models import User, LunchRegistration # Importa modelos para o contexto do shell

app = create_app()

# Adiciona contexto ao comando 'flask shell' para facilitar o debug
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'LunchRegistration': LunchRegistration}

if __name__ == '__main__':
    # Roda usando o servidor de desenvolvimento do Flask
    # Para produção, use Gunicorn: gunicorn --bind 0.0.0.0:5000 "run:create_app()"
    app.run(debug=app.config.get('DEBUG', True))