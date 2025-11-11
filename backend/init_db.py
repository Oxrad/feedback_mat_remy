# -*- coding: utf-8 -*-
import os
os.environ['PGCLIENTENCODING'] = 'UTF8'

from database import engine, SessionLocal, Base
from models import OrderStatus, Question

def init_database():
    print("Creation des tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables creees avec succes !")
    
    db = SessionLocal()
    
    try:
        existing_statuses = db.query(OrderStatus).count()
        existing_questions = db.query(Question).count()
        
        if existing_statuses == 0:
            print("Insertion des statuts de commande...")
            statuses = [
                OrderStatus(id=1, description="En preparation"),
                OrderStatus(id=2, description="Expediee"),
                OrderStatus(id=3, description="En cours de livraison"),
                OrderStatus(id=4, description="Livree"),
                OrderStatus(id=5, description="Retournee")
            ]
            db.add_all(statuses)
            db.commit()
            print("Statuts de commande inseres !")
        
        if existing_questions == 0:
            print("Insertion des questions...")
            questions = [
                Question(id=1, title="Evaluer de 1 a 5 le respect du delai de livraison", maximum_grade=5),
                Question(id=2, title="Evaluer de 1 a 5 l etat de votre colis a sa reception", maximum_grade=5),
                Question(id=3, title="Evaluer de 1 a 5 le comportement du livreur", maximum_grade=5)
            ]
            db.add_all(questions)
            db.commit()
            print("Questions inserees !")
        
        print("\nBase de donnees initialisee avec succes !")
        
    except Exception as e:
        print(f"Erreur lors de l initialisation : {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()