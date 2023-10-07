from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_name.db'  # Set your database URI
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # username = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(256), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # "username": self.username,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    
