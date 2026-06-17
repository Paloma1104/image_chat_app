from sqlalchemy import Column, ForeignKey, Float
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

class Detection(Base):
    __tablename__ = "detections"
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"))
    label = Column(String)
    confidence = Column(Float)
    x1 = Column(Float)
    y1 = Column(Float)
    x2 = Column(Float)
    y2 = Column(Float)
