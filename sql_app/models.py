from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
import pytz

Base = declarative_base()
timezone_utc_7 = pytz.timezone('Asia/Bangkok')

def current_time_utc_7():
    return datetime.now(timezone_utc_7)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    shrimp_quantities = relationship("ShrimpQuantity", back_populates="owner")
    shrimp_pond = relationship("ShrimpPond", back_populates="owner_pond")

class ShrimpQuantity(Base):
    __tablename__ = "shrimp_quantities"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    # timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    timestamp = Column(DateTime, default=current_time_utc_7)
    
    owner = relationship("User", back_populates="shrimp_quantities")
    
class ShrimpPond(Base):
    __tablename__ = "shrimp_pond"
    
    id = Column(Integer, primary_key=True, index=True)
    pond_name = Column(String, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    pond_quantity = Column(Integer, index=True)
    shrimp_sold = Column(Integer, default=None)
    date = Column(DateTime, default=current_time_utc_7)

    owner_pond = relationship("User", back_populates="shrimp_pond")
