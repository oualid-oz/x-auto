from sqlalchemy import Column, Integer, String, DateTime
from app.db.session import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    
