from typing import List, Dict
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from datetime import datetime, date
from fastapi import Query
import re
import logging

from models.asianews_model import AsiaNewsDB
from schemas.asianews_schema import AsiaNewsSchema
from db.db import get_postgres_db

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)-8s | ""%(module)s:%(funcName)s:%(lineno)d - %(message)s")
logger = logging.getLogger('app')

router = APIRouter(prefix="/asianews", tags=["AsiaNews"])

@router.get("/", response_model=List[AsiaNewsSchema])
def get_articles(db: Session = Depends(get_postgres_db)):
    try:
        articles = articles = db.query(AsiaNewsDB).all()
        return articles
    except Exception as e:
        logger.error(f"Error fetching articles: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles")        


@router.get("/categories", response_model=Dict[str, List[str]])
def get_categories(db: Session = Depends(get_postgres_db)):
    try:
        categories = db.query(AsiaNewsDB.category).distinct().all()
        return {"categories": [cat[0] for cat in categories]}
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail="Error fetching categories")    

@router.get("/date", response_model=List[AsiaNewsSchema])
def fetch_articles_date(date_param: str, db: Session = Depends(get_postgres_db)):
    try:
        date_param = datetime.strptime(date_param, "%Y-%m-%d").date()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Date format")
    
    articles = db.query(AsiaNewsDB).filter(AsiaNewsDB.date == date_param).all()
    return articles    

@router.get("/today", response_model=List[AsiaNewsSchema])
def fetch_articles_date(db: Session = Depends(get_postgres_db)):
    try:
        date_param = datetime.today().date().strftime("%Y-%m-%d")
        articles = db.query(AsiaNewsDB).filter(AsiaNewsDB.date == date_param).all()
        return articles   
    except Exception as e:
        logger.error(f"Error fetching articles by date: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles by date")    

@router.get("/{category}", response_model=List[AsiaNewsSchema])
def get_articles_category(category: str, db: Session = Depends(get_postgres_db)):
    try:
        category = re.sub(r'[^A-Za-z]', "", category).lower()
        articles_category = db.query(AsiaNewsDB).filter(AsiaNewsDB.category == category).all()
        return articles_category
    except Exception as e:
        logger.error(f"Error fetching articles by category: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles by category")    

@router.get("/today/{category}", response_model=List[AsiaNewsSchema])
def get_articles_category_date(category: str, db: Session = Depends(get_postgres_db)):    
    try :
        date_param = datetime.today().date().strftime("%Y-%m-%d")        
        articles_category_date = db.query(AsiaNewsDB).filter(AsiaNewsDB.category == category).filter(AsiaNewsDB.date == date_param).all()
        return articles_category_date
    except Exception as e:
        logger.error(f"Error fetching articles by category and date: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles by category and date")    

