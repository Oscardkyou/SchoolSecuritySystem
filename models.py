from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True)
    unique_id = Column(String, unique=True, nullable=False)
    parent_name = Column(String, nullable=False)
    parent_surname = Column(String, nullable=False)
    child_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    photos = relationship("Photo", back_populates="parent")

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    parent = relationship("Parent", back_populates="photos")
