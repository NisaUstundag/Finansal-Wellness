from pydantic import BaseModel
from datetime import datetime

# Temel etkileşim bilgilerini içeren ana şema
class InteractionBase(BaseModel):
    user_text: str
    predicted_emotion: str | None = None
    predicted_topic: str | None = None
    final_recommendation: str | None = None

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True