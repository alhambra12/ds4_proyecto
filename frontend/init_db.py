from app import create_app
from database import db, User

app = create_app([]) 

with app.app_context():
    db.create_all()
    
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin123') 
        db.session.add(admin)
        db.session.commit()
        print("Usuario admin creado")
    
    print("Base de datos inicializada")