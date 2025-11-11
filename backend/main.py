from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import date, timedelta
import random

from database import get_db, engine
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FeelBack API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API FeelBack",
        "version": "2.0.0 (avec PostgreSQL)",
        "endpoints": {
            "questions": "/api/questions",
            "create_order": "/api/orders/create",
            "submit_feedback": "/api/orders/{order_id}/feedback",
            "stats": "/api/dashboard-stats"
        }
    }

@app.get("/api/questions", response_model=List[schemas.QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(models.Question).all()
    return questions

@app.post("/api/orders/create", response_model=schemas.OrderResponse)
def create_order(db: Session = Depends(get_db)):
    tracking_number = f"TRK-{random.randint(100000, 999999)}"
    shipping_date = date.today()
    estimated_delivery_date = shipping_date + timedelta(days=random.randint(3, 7))
    
    new_order = models.Order(
        tracking_number=tracking_number,
        shipping_date=shipping_date,
        estimated_delivery_date=estimated_delivery_date,
        order_status_id=4
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return new_order

@app.post("/api/orders/{order_id}/feedback")
def submit_feedback(
    order_id: int,
    feedback_data: schemas.FeedbackCreate,
    db: Session = Depends(get_db)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    existing_feedback = db.query(models.Feedback).filter(
        models.Feedback.order_id == order_id
    ).first()
    if existing_feedback:
        raise HTTPException(status_code=400, detail="Un feedback existe déjà pour cette commande")
    
    new_feedback = models.Feedback(order_id=order_id)
    db.add(new_feedback)
    db.flush()
    
    for grade_data in feedback_data.grades:
        grade = models.Grade(
            question_id=grade_data.question_id,
            feedback_id=new_feedback.id,
            grade=grade_data.grade
        )
        db.add(grade)
    
    db.commit()
    db.refresh(new_feedback)
    
    return {
        "message": "Feedback enregistré avec succès",
        "feedback_id": new_feedback.id
    }

@app.get("/api/dashboard-stats", response_model=schemas.DashboardStatsResponse)
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_feedbacks = db.query(models.Feedback).count()
    total_orders = db.query(models.Order).count()
    
    average_grades = []
    questions = db.query(models.Question).all()
    
    for question in questions:
        avg_result = db.query(
            func.avg(models.Grade.grade)
        ).filter(
            models.Grade.question_id == question.id
        ).scalar()
        
        average_grade = round(float(avg_result), 1) if avg_result else 0.0
        
        average_grades.append({
            "question_id": question.id,
            "title": question.title.split("le ")[-1].capitalize() if "le " in question.title else question.title,
            "average_grade": average_grade,
            "maximum_grade": question.maximum_grade
        })
    
    return {
        "total_feedbacks": total_feedbacks,
        "total_orders": total_orders,
        "average_grades": average_grades
    }

@app.delete("/api/reset")
def reset_database(db: Session = Depends(get_db)):
    try:
        db.query(models.Grade).delete()
        db.query(models.Feedback).delete()
        db.query(models.Order).delete()
        db.commit()
        return {"message": "Données réinitialisées avec succès"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))