from sqlalchemy import Column, Integer, String
from app.database import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(length=160), nullable=False)
    counter = Column(Integer, default=0, nullable=False)
