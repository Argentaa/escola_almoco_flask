# instance/config.py
import os
from dotenv import load_dotenv

# Carrega variáveis do .env na pasta raiz do projeto
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'app.db') # Fallback para SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Adicione outras configurações aqui