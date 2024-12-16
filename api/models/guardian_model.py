from db.db import Base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, date

class GuardianDB(Base):
    __tablename__ = "guardian"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=True)
    image = Column(String, nullable=True)
    link = Column(String, nullable=True)
    date = Column(Date, nullable=False)


