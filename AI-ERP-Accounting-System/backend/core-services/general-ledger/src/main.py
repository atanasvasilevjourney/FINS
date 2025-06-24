from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime, date
from decimal import Decimal

from .database.connection import get_db
from .models.chart_of_accounts import ChartOfAccounts, ChartOfAccountsCreate, ChartOfAccountsUpdate
from .models.journal_entries import JournalEntry, JournalEntryCreate, JournalEntryUpdate, JournalLine
from .models.financial_statements import FinancialStatement, BalanceSheet, IncomeStatement
from .services.gl_service import GeneralLedgerService
from .services.journal_service import JournalService
from .services.reporting_service import ReportingService
from .utils.validators import validate_journal_entry
from .utils.helpers import format_currency

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FINS ERP - General Ledger Service",
    description="General Ledger microservice for FINS ERP System",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Service instances
gl_service = GeneralLedgerService()
journal_service = JournalService()
reporting_service = ReportingService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "General Ledger",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "service": "General Ledger",
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }

# Chart of Accounts endpoints
@app.post("/accounts", response_model=ChartOfAccounts, status_code=status.HTTP_201_CREATED)
async def create_account(
    account: ChartOfAccountsCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new chart of accounts entry"""
    try:
        return gl_service.create_account(db, account)
    except Exception as e:
        logger.error(f"Error creating account: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/accounts", response_model=List[ChartOfAccounts])
async def get_accounts(
    skip: int = 0,
    limit: int = 100,
    account_type: Optional[str] = None,
    active: Optional[bool] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get chart of accounts with optional filtering"""
    try:
        return gl_service.get_accounts(db, skip=skip, limit=limit, account_type=account_type, active=active)
    except Exception as e:
        logger.error(f"Error retrieving accounts: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/accounts/{account_id}", response_model=ChartOfAccounts)
async def get_account(
    account_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific account by ID"""
    try:
        account = gl_service.get_account(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving account {account_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/accounts/{account_id}", response_model=ChartOfAccounts)
async def update_account(
    account_id: int,
    account: ChartOfAccountsUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update an existing account"""
    try:
        updated_account = gl_service.update_account(db, account_id, account)
        if not updated_account:
            raise HTTPException(status_code=404, detail="Account not found")
        return updated_account
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating account {account_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Journal Entries endpoints
@app.post("/journal-entries", response_model=JournalEntry, status_code=status.HTTP_201_CREATED)
async def create_journal_entry(
    entry: JournalEntryCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new journal entry"""
    try:
        # Validate journal entry
        validation_result = validate_journal_entry(entry)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"])
        
        return journal_service.create_journal_entry(db, entry)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating journal entry: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/journal-entries", response_model=List[JournalEntry])
async def get_journal_entries(
    skip: int = 0,
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    account_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get journal entries with optional filtering"""
    try:
        return journal_service.get_journal_entries(
            db, skip=skip, limit=limit, 
            start_date=start_date, end_date=end_date,
            account_id=account_id, status=status
        )
    except Exception as e:
        logger.error(f"Error retrieving journal entries: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/journal-entries/{entry_id}", response_model=JournalEntry)
async def get_journal_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific journal entry by ID"""
    try:
        entry = journal_service.get_journal_entry(db, entry_id)
        if not entry:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        return entry
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving journal entry {entry_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/journal-entries/{entry_id}", response_model=JournalEntry)
async def update_journal_entry(
    entry_id: int,
    entry: JournalEntryUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update an existing journal entry"""
    try:
        updated_entry = journal_service.update_journal_entry(db, entry_id, entry)
        if not updated_entry:
            raise HTTPException(status_code=404, detail="Journal entry not found")
        return updated_entry
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating journal entry {entry_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/journal-entries/{entry_id}/post")
async def post_journal_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Post a journal entry to the general ledger"""
    try:
        result = journal_service.post_journal_entry(db, entry_id)
        return {"message": "Journal entry posted successfully", "entry_id": entry_id}
    except Exception as e:
        logger.error(f"Error posting journal entry {entry_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Financial Reporting endpoints
@app.get("/reports/balance-sheet", response_model=BalanceSheet)
async def get_balance_sheet(
    as_of_date: date,
    entity_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate balance sheet as of a specific date"""
    try:
        return reporting_service.generate_balance_sheet(db, as_of_date, entity_id)
    except Exception as e:
        logger.error(f"Error generating balance sheet: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reports/income-statement", response_model=IncomeStatement)
async def get_income_statement(
    start_date: date,
    end_date: date,
    entity_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate income statement for a date range"""
    try:
        return reporting_service.generate_income_statement(db, start_date, end_date, entity_id)
    except Exception as e:
        logger.error(f"Error generating income statement: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reports/trial-balance")
async def get_trial_balance(
    as_of_date: date,
    entity_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate trial balance as of a specific date"""
    try:
        return reporting_service.generate_trial_balance(db, as_of_date, entity_id)
    except Exception as e:
        logger.error(f"Error generating trial balance: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reports/account-activity/{account_id}")
async def get_account_activity(
    account_id: int,
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get account activity for a specific account and date range"""
    try:
        return reporting_service.get_account_activity(db, account_id, start_date, end_date)
    except Exception as e:
        logger.error(f"Error retrieving account activity: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 