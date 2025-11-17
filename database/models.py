from sqlalchemy import Column, Integer, BigInteger, String
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    discord_id = Column(BigInteger, unique=True, nullable=False)
    steam_id = Column(String, nullable=True)
    language = Column(String, default="en")
    status = Column(String, default="new")
