from sqlalchemy import Column, Integer, String
from app.db.session import Base

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, index=True)
    user_id = Column(Integer, index=True)