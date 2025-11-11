# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Forcer l'encodage UTF-8
os.environ['PGCLIENTENCODING'] = 'UTF8'
os.environ['LANG'] = 'en_US.UTF-8'

# URL simple sans paramÃ¨tres dans l'URL
DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost/feelback_db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "client_encoding": "utf8"
    },
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()