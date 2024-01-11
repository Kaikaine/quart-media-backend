from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    bio = Column(String(200))
    profile_image = Column(String(20), nullable=False, default='default.jpg')
    posts = relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')  
    comments = relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')  
    date_created = Column(DateTime, nullable=False, default=datetime.utcnow)