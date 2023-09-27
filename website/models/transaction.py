from website import db
from .base_model import BaseModel
from sqlalchemy import Column, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4

class Transaction(BaseModel, db.Model):
    __tablename__ = 'transactions'

    amount = Column(Float, nullable=False)
    transaction_type = Column(String(50), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)  # Default to the current timestamp

    # Define the relationship to the Account model
    account_id = Column(String(36), ForeignKey('accounts.id'), nullable=False)
    account = relationship("Account", back_populates="transactions")

    def __init__(self, amount, transaction_type, account_id):
        self.amount = amount
        self.transaction_type = transaction_type
        self.account_id = account_id
