from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Interaction(Base):
    __tablename__ = 'interactions'

    id = Column(Integer, primary_key=True, index=True)
    user_text = Column(String, nullable=False)
    predicted_emotion = Column(String)
    predicted_topic = Column(String)
    final_recommendation = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())