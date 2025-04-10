from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager, bcrypt

# Função user_loader exigida pelo Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """Modelo de Usuário."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128)) # Não armazene a senha diretamente!
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    is_staff = db.Column(db.Boolean, default=False, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamento com LunchRegistration (um usuário tem muitos registros)
    lunch_registrations = db.relationship('LunchRegistration', backref='student', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.last_name or self.username # Fallback

    def __repr__(self):
        return f'<User {self.username}>'


class LunchRegistration(db.Model):
    """Modelo de Registro de Almoço."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # Chave estrangeira
    lunch_date = db.Column(db.Date, nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Garante unicidade de aluno por data
    __table_args__ = (db.UniqueConstraint('user_id', 'lunch_date', name='_user_lunch_date_uc'),)

    def __repr__(self):
        # Acessa o nome do aluno via backref 'student'
        student_name = self.student.username if self.student else 'Unknown'
        return f'<LunchRegistration {student_name} - {self.lunch_date.strftime("%Y-%m-%d")}>'