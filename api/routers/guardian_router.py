from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import datetime, date
from fastapi import Query
import logging

from models.guardian_model import GuardianDB
from schemas.guardian_schema import GuardianSchema
from db.db import get_postgres_db

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)-8s | ""%(module)s:%(funcName)s:%(lineno)d - %(message)s")
logger = logging.getLogger('app')

router = APIRouter(prefix="/guardian", tags=["Guardian"])

@router.get("/", response_model=List[GuardianSchema])
def get_articles(db: Session = Depends(get_postgres_db)):
    articles = db.query(GuardianDB).all()
    return articles


@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_postgres_db)):
    categories = db.query(GuardianDB.category).distinct().all()

    return [cat[0] for cat in categories]

@router.get("/date", response_model=List[GuardianSchema])
def fetch_articles_date(date_param: str, db: Session = Depends(get_postgres_db)):
    try:
        date_param = datetime.strptime(date_param, "%Y-%m-%d").date()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Date format")
    
    articles = db.query(GuardianDB).filter(GuardianDB.date == date_param).all()
    return articles    

@router.get("/{category}", response_model=List[GuardianSchema])
def get_articles_category(category: str, db: Session = Depends(get_postgres_db)):
    articles_category = db.query(GuardianDB).filter(GuardianDB.category == category).all()

    return articles_category

@router.get("/{date_param}/{category}", response_model=List[GuardianSchema])
def get_articles_category_date(category: str, date_param: str, db: Session = Depends(get_postgres_db)):
    try:
        date_param = datetime.strptime(date_param, "%Y-%m-%d").date()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Date format")
    
    articles_category_date = db.query(GuardianDB).filter(GuardianDB.category == category).filter(GuardianDB.date == date_param).all()
    return articles_category_date
