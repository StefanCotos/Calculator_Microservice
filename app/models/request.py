from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.session import Base


class RequestRecord(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    expression = Column(String, nullable=False)
    result = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
