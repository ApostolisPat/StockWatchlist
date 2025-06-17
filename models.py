from sqlalchemy import Column, Integer, String, DateTime, func
from .database import Base

#Database data model for user
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True, nullable=False) 
    email = Column(String, index=True, unique=True, nullable=False) 
    password = Column(String, nullable=False) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())