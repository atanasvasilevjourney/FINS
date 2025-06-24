from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field
from decimal import Decimal

Base = declarative_base()

# SQLAlchemy Models
class JournalEntry(Base):
    __tablename__ = "journal_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    entry_number = Column(String(20), unique=True, index=True, nullable=False)
    entry_date = Column(Date, nullable=False)
    reference = Column(String(100), nullable=True)
    description = Column(Text, nullable=False)
    status = Column(String(20), default="Draft")  # Draft, Posted, Void
    entry_type = Column(String(50), nullable=False)  # Manual, System, Recurring
    total_debits = Column(Numeric(15, 2), default=0)
    total_credits = Column(Numeric(15, 2), default=0)
    is_balanced = Column(Boolean, default=False)
    posted_at = Column(DateTime, nullable=True)
    posted_by = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
    # Relationships
    journal_lines = relationship("JournalLine", back_populates="journal_entry", cascade="all, delete-orphan")

class JournalLine(Base):
    __tablename__ = "journal_lines"
    
    id = Column(Integer, primary_key=True, index=True)
    journal_entry_id = Column(Integer, ForeignKey("journal_entries.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("chart_of_accounts.id"), nullable=False)
    line_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    debit_amount = Column(Numeric(15, 2), default=0)
    credit_amount = Column(Numeric(15, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    journal_entry = relationship("JournalEntry", back_populates="journal_lines")
    account = relationship("ChartOfAccounts", back_populates="journal_lines")

# Pydantic Models
class JournalLineBase(BaseModel):
    account_id: int
    line_number: int
    description: Optional[str] = None
    debit_amount: Decimal = Field(default=0, ge=0)
    credit_amount: Decimal = Field(default=0, ge=0)

class JournalLineCreate(JournalLineBase):
    pass

class JournalLineUpdate(BaseModel):
    account_id: Optional[int] = None
    line_number: Optional[int] = None
    description: Optional[str] = None
    debit_amount: Optional[Decimal] = Field(None, ge=0)
    credit_amount: Optional[Decimal] = Field(None, ge=0)

class JournalLine(JournalLineBase):
    id: int
    journal_entry_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class JournalEntryBase(BaseModel):
    entry_date: date
    reference: Optional[str] = Field(None, max_length=100)
    description: str
    entry_type: str = Field(..., regex="^(Manual|System|Recurring)$")
    journal_lines: List[JournalLineCreate]

class JournalEntryCreate(JournalEntryBase):
    pass

class JournalEntryUpdate(BaseModel):
    entry_date: Optional[date] = None
    reference: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    entry_type: Optional[str] = Field(None, regex="^(Manual|System|Recurring)$")
    journal_lines: Optional[List[JournalLineCreate]] = None

class JournalEntry(JournalEntryBase):
    id: int
    entry_number: str
    status: str
    total_debits: Decimal
    total_credits: Decimal
    is_balanced: bool
    posted_at: Optional[datetime] = None
    posted_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    journal_lines: List[JournalLine]
    
    class Config:
        from_attributes = True 