from typing import List, Dict
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
    try:
        articles = articles = db.query(GuardianDB).all()
        return articles
    except Exception as e:
        logger.error(f"Error fetching articles: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles")        


@router.get("/categories", response_model=Dict[str, List[str]])
def get_categories(db: Session = Depends(get_postgres_db)):
    try:
        categories = categories = db.query(GuardianDB.category).distinct().all()
        return {"categories": [cat[0] for cat in categories]}
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail="Error fetching categories")        
    

@router.get("/date", response_model=List[GuardianSchema])
def fetch_articles_date(date_param: str, db: Session = Depends(get_postgres_db)):
    try:
        date_param = datetime.strptime(date_param, "%Y-%m-%d").date()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Date format")
    
    articles = db.query(GuardianDB).filter(GuardianDB.date == date_param).all()
    return articles    

@router.get("/today", response_model=List[GuardianSchema])
def fetch_articles_date(db: Session = Depends(get_postgres_db)):
    try:
        date_param = datetime.today().date().strftime("%Y-%m-%d")
        articles = db.query(GuardianDB).filter(GuardianDB.date == date_param).all()
        return articles   
    except Exception as e:
        logger.error(f"Error fetching articles by date: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles by date")         

@router.get("/{category}", response_model=List[GuardianSchema])
def get_articles_category(category: str, db: Session = Depends(get_postgres_db)):
    try:
        category = re.sub(r'[^A-Za-z]', "", category).lower()
        articles_category = db.query(GuardianDB).filter(GuardianDB.category == category).all()
        return articles_category
    except Exception as e:
        logger.error(f"Error fetching articles by category: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles by category")       


@router.get("/today/{category}", response_model=List[GuardianSchema])
def get_articles_category_date(category: str, db: Session = Depends(get_postgres_db)):    
    try :
        date_param = datetime.today().date().strftime("%Y-%m-%d")        
        articles_category_date = db.query(GuardianDB).filter(GuardianDB.category == category).filter(GuardianDB.date == date_param).all()
        return articles_category_date
    except Exception as e:
        logger.error(f"Error fetching articles by category and date: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles by category and date")    


