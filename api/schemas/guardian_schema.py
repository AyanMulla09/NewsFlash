from pydantic import BaseModel
from datetime import datetime, date

class GuardianSchema(BaseModel):
    title: str
    category: str
    image: str
    link: str
    date: date

    class config:
        orm_mode = True


