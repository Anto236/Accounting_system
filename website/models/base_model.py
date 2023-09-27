from website import db
import uuid  # Import the uuid library
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    """The BaseModel class from which future classes will be derived"""
    __abstract__ = True
    id = Column(String(36), primary_key=True, default=str(uuid.uuid4()))  # Use UUID for id
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
