from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class OrderStatus(Base):
    __tablename__ = "order_status"
    
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100), nullable=False)
    orders = relationship("Order", back_populates="order_status")

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String(50), unique=True, nullable=False)
    shipping_date = Column(Date, nullable=False)
    estimated_delivery_date = Column(Date, nullable=False)
    order_status_id = Column(Integer, ForeignKey("order_status.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    order_status = relationship("OrderStatus", back_populates="orders")
    feedback = relationship("Feedback", back_populates="order", uselist=False)

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    maximum_grade = Column(Integer, default=5, nullable=False)
    grades = relationship("Grade", back_populates="question")

class Feedback(Base):
    __tablename__ = "feedbacks"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    order = relationship("Order", back_populates="feedback")
    grades = relationship("Grade", back_populates="feedback", cascade="all, delete-orphan")

class Grade(Base):
    __tablename__ = "grades"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    feedback_id = Column(Integer, ForeignKey("feedbacks.id"), nullable=False)
    grade = Column(Integer, nullable=False)
    
    question = relationship("Question", back_populates="grades")
    feedback = relationship("Feedback", back_populates="grades")