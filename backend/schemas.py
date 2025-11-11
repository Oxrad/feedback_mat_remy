from pydantic import BaseModel
from typing import List
from datetime import date, datetime

class QuestionResponse(BaseModel):
    id: int
    title: str
    maximum_grade: int
    
    class Config:
        from_attributes = True

class GradeCreate(BaseModel):
    question_id: int
    grade: int

class FeedbackCreate(BaseModel):
    grades: List[GradeCreate]

class OrderResponse(BaseModel):
    id: int
    tracking_number: str
    shipping_date: date
    estimated_delivery_date: date
    order_status_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AverageGradeResponse(BaseModel):
    question_id: int
    title: str
    average_grade: float
    maximum_grade: int

class DashboardStatsResponse(BaseModel):
    total_feedbacks: int
    total_orders: int
    average_grades: List[AverageGradeResponse]