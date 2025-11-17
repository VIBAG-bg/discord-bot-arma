from sqlalchemy import Boolean, Column, Integer, BigInteger, String
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    discord_id = Column(BigInteger, unique=True, index=True, nullable=False)

    # Новые поля
    username = Column(String(100), nullable=True)       # Discord username (login / handle)
    display_name = Column(String(100), nullable=True)   # Nick on server

    steam_id = Column(String(32), nullable=True)
    language = Column(String(5), nullable=True)
    status = Column(String(20), nullable=False, server_default="active")
    is_admin = Column(Boolean, nullable=False, server_default="false")

