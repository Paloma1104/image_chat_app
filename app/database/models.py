from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from datetime import datetime

from app.database.database import Base

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    filename = Column(String, index=True)
    title = Column(String)
    notes = Column(String)
    uploaded_at = Column(DateTime, default=datetime.now)
