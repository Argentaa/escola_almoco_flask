from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(func):
    """Decorador para rotas que exigem privilégios de administrador."""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_staff:
            # Retorna 403 Forbidden se não for admin
            abort(403)
        return func(*args, **kwargs)
    return decorated_view