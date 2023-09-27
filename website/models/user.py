from website import db
from .base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(UserMixin, BaseModel, db.Model):
    __tablename__ = 'users'

    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)

    # Add a relationship to accounts
    accounts = relationship("Account", back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
