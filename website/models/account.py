from website import db
from .base_model import BaseModel
from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from uuid import uuid4

class Account(BaseModel, db.Model):
    __tablename__ = 'accounts'

    name = Column(String(100), nullable=False)
    balance = Column(Float, nullable=False, default=0.0)

    # Add relationships to users and transactions
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="accounts")
    transactions = relationship("Transaction", back_populates="account")

    def __init__(self, name, user_id, balance=0.0):
        self.name = name
        self.user_id = user_id
        self.balance = balance
