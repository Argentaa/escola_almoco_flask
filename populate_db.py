from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, LunchRegistration

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    for i in range(1, 11):
        username = f"aluno{i}"
        email = f"aluno{i}@exemplo.com"
        first_name = f"Aluno{i}"
        last_name = "Teste"

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=False
        )
        user.set_password("senha123")
        db.session.add(user)
        db.session.flush()  # Para obter user.id antes do commit

        for day_offset in range(7):
            lunch_date = (datetime.utcnow() + timedelta(days=day_offset)).date()
            lunch = LunchRegistration(
                user_id=user.id,
                lunch_date=lunch_date
            )
            db.session.add(lunch)

    db.session.commit()
    print("10 alunos criados com 7 registros de almoço cada.")
