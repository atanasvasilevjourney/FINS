from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

Base = declarative_base()

# SQLAlchemy Model
class ChartOfAccounts(Base):
    __tablename__ = "chart_of_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_code = Column(String(20), unique=True, index=True, nullable=False)
    account_name = Column(String(100), nullable=False)
    account_type = Column(String(50), nullable=False)  # Asset, Liability, Equity, Revenue, Expense
    account_category = Column(String(50), nullable=False)  # Current Assets, Fixed Assets, etc.
    parent_account_id = Column(Integer, ForeignKey("chart_of_accounts.id"), nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_system_account = Column(Boolean, default=False)
    normal_balance = Column(String(10), nullable=False)  # Debit or Credit
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    
    # Relationships
    parent_account = relationship("ChartOfAccounts", remote_side=[id], backref="child_accounts")
    journal_lines = relationship("JournalLine", back_populates="account")

# Pydantic Models
class ChartOfAccountsBase(BaseModel):
    account_code: str = Field(..., min_length=1, max_length=20)
    account_name: str = Field(..., min_length=1, max_length=100)
    account_type: str = Field(..., regex="^(Asset|Liability|Equity|Revenue|Expense)$")
    account_category: str = Field(..., min_length=1, max_length=50)
    parent_account_id: Optional[int] = None
    description: Optional[str] = None
    is_active: bool = True
    is_system_account: bool = False
    normal_balance: str = Field(..., regex="^(Debit|Credit)$")

class ChartOfAccountsCreate(ChartOfAccountsBase):
    pass

class ChartOfAccountsUpdate(BaseModel):
    account_name: Optional[str] = Field(None, min_length=1, max_length=100)
    account_type: Optional[str] = Field(None, regex="^(Asset|Liability|Equity|Revenue|Expense)$")
    account_category: Optional[str] = Field(None, min_length=1, max_length=50)
    parent_account_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    normal_balance: Optional[str] = Field(None, regex="^(Debit|Credit)$")

class ChartOfAccounts(ChartOfAccountsBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    
    class Config:
        from_attributes = True 