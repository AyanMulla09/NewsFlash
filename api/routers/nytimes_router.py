from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from models.nytimes_model import NYTimesDB
from schemas.nytimes_schema import NYTimesSchema
from db.db import get_postgres_db

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)-8s | ""%(module)s:%(funcName)s:%(lineno)d - %(message)s")
logger = logging.getLogger('app')

router = APIRouter(prefix="/nytimes", tags=["NYTimes"])

# Get all NYTimes articles
@router.get("/", response_model=List[NYTimesSchema])
def get_articles(db: Session = Depends(get_postgres_db)):
    try:
        articles = db.query(NYTimesDB).all()
        return articles
    except Exception as e:
        logger.error(f"Error fetching articles: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles")

# Get distinct categories of NYTimes articles
@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_postgres_db)):
    try:
        categories = db.query(NYTimesDB.category).distinct().all()
        return [cat[0] for cat in categories]
    except Exception as e:
        logger.error(f"Error fetching categories: {e}")
        raise HTTPException(status_code=500, detail="Error fetching categories")

# Get articles for a specific date
@router.get("/date", response_model=List[NYTimesSchema])
def fetch_articles_date(date_param: str, db: Session = Depends(get_postgres_db)):
    try:
        date_param = datetime.strptime(date_param, "%Y-%m-%d").date()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Date format")
    
    try:
        articles = db.query(NYTimesDB).filter(NYTimesDB.date == date_param).all()
        return articles
    except Exception as e:
        logger.error(f"Error fetching articles by date: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles by date")

# Get articles by category
@router.get("/{category}", response_model=List[NYTimesSchema])
def get_articles_category(category: str, db: Session = Depends(get_postgres_db)):
    try:
        articles_category = db.query(NYTimesDB).filter(NYTimesDB.category == category).all()
        return articles_category
    except Exception as e:
        logger.error(f"Error fetching articles by category: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles by category")

# Get articles by both category and date
@router.get("/{date_param}/{category}", response_model=List[NYTimesSchema])
def get_articles_category_date(category: str, date_param: str, db: Session = Depends(get_postgres_db)):
    try:
        date_param = datetime.strptime(date_param, "%Y-%m-%d").date()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid Date format")
    
    try:
        articles_category_date = db.query(NYTimesDB).filter(NYTimesDB.category == category).filter(NYTimesDB.date == date_param).all()
        return articles_category_date
    except Exception as e:
        logger.error(f"Error fetching articles by category and date: {e}")
        raise HTTPException(status_code=500, detail="Error fetching articles by category and date")
