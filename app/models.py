from sqlalchemy import Column, Integer, String, JSON, Table, UniqueConstraint, MetaData
from app.database import Base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, Text
from pydantic import BaseModel, EmailStr
from datetime import datetime
import pytz


class Token(BaseModel):
    access_token: str

class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    
    class Config:
        from_attributes = True  # Renamed to 'from_attributes' in newer Pydantic versions

class User(Base):
    __tablename__ = "users_user"

    id = Column(Integer, primary_key=True, index=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    is_superuser = Column(Boolean, default=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime(timezone=True), server_default=func.now())
    email = Column(String, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    is_verified = Column(Boolean, default=False)
    role = Column(String, nullable=True)
    created_by_id = Column(BigInteger, nullable=True)


class SendEmailData(BaseModel):
    sender_email: EmailStr
    receiver_email: EmailStr
    sender_password: str
    body: str
    subject: str

    class Config:
        from_attributes = True
        

class ServerMetadata(Base):
    __tablename__ = "server_metadata"

    id = Column(Integer, primary_key=True, index=True)
    server_name = Column(String, nullable=False)
    server_data = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint('server_name', name='unique_server_name'),
    )
    

class ServerMetadataLogs(Base):
    __tablename__ = "server_metadata_logs"

    id = Column(Integer, primary_key=True, index=True)
    server_logs = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())