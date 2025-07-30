from app import app, db
from app.models import Operation

with app.app_context():
    db.create_all()
    print("✅ Base de dades creada amb èxit!")
