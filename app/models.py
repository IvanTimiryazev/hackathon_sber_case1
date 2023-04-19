from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from typing import List


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200))
    name = db.Column(db.String(100), nullable=True)
    surname = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    city = db.Column(db.String(200))
    tlg_link = db.Column(db.String(100))
    resume = db.Column(db.String(100), nullable=True)
    rate = db.Column(db.Float, nullable=True)
    hard_rate = db.Column(db.Float, nullable=True)
    soft_rate = db.Column(db.Float, nullable=True)
    employee = db.Column(db.Boolean, nullable=False, default=False)
    stack_id = db.Column(db.Integer, db.ForeignKey('stack.id'), nullable=True)
    stack = db.relationship('Stack')

    def __repr__(self):
        return f'<{self.email}-{self.name}>'

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_token(self, expire_time: int = 168) -> str:
        expire_delta = timedelta(hours=expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email: str, password: str) -> 'Users':
        user = cls.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            return user

    @staticmethod
    def get_users(stack_id: int) -> List['Users']:
        users = Users.query.filter_by(stack_id=stack_id)
        return users


class Stack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(200), nullable=False)
