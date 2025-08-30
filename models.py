from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import date

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # new column for role
    created_at = db.Column(db.Date, default=date.today)

    transactions = db.relationship('Transaction', backref='user', lazy=True)
    goals = db.relationship('Goal', uselist=False, backref='user', lazy=True)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False, default='expense')  # 'income' or 'expense'
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False, default='Other')
    note = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date, nullable=False, default=date.today)

class Goal(db.Model):
    __tablename__ = 'goals'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    monthly_savings_target = db.Column(db.Float, nullable=False, default=0.0)
