import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from app import app, db

def init_db():
    with app.app_context():
        db.create_all()  # Create database tables
        print("Database initialized.")

if __name__ == '__main__':
    init_db()
