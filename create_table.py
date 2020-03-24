from manager import app
from Meeting import db

with app.app_context():
    db.create_all()
