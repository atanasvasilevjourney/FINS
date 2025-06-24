from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal
import logging
import uuid

from ..models.journal_entries import JournalEntry, JournalEntryCreate, JournalEntryUpdate, JournalLine, JournalLineCreate
from ..models.chart_of_accounts import ChartOfAccounts
from ..database.connection import get_db

logger = logging.getLogger(__name__)

class JournalService:
    """Service class for Journal Entry operations"""
    
    def create_journal_entry(self, db: Session, entry: JournalEntryCreate) -> JournalEntry:
        """Create a new journal entry"""
        try:
            # Generate unique entry number
            entry_number = self._generate_entry_number(db)
            
            # Calculate totals
            total_debits = sum(line.debit_amount for line in entry.journal_lines)
            total_credits = sum(line.credit_amount for line in entry.journal_lines)
            is_balanced = total_debits == total_credits
            
            if not is_balanced:
                raise ValueError(f"Journal entry is not balanced. Debits: {total_debits}, Credits: {total_credits}")
            
            # Create journal entry
            db_entry = JournalEntry(
                entry_number=entry_number,
                entry_date=entry.entry_date,
                reference=entry.reference,
                description=entry.description,
                entry_type=entry.entry_type,
                total_debits=total_debits,
                total_credits=total_credits,
                is_balanced=is_balanced,
                status="Draft"
            )
            
            db.add(db_entry)
            db.flush()  # Get the ID without committing
            
            # Create journal lines
            for line_data in entry.journal_lines:
                # Validate account exists and is active
                account = db.query(ChartOfAccounts).filter(
                    and_(
                        ChartOfAccounts.id == line_data.account_id,
                        ChartOfAccounts.is_active == True
                    )
                ).first()
                
                if not account:
                    raise ValueError(f"Account {line_data.account_id} not found or inactive")
                
                db_line = JournalLine(
                    journal_entry_id=db_entry.id,
                    account_id=line_data.account_id,
                    line_number=line_data.line_number,
                    description=line_data.description,
                    debit_amount=line_data.debit_amount,
                    credit_amount=line_data.credit_amount
                )
                
                db.add(db_line)
            
            db.commit()
            db.refresh(db_entry)
            
            logger.info(f"Created journal entry: {entry_number}")
            return db_entry
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating journal entry: {str(e)}")
            raise
    
    def get_journal_entries(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        account_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[JournalEntry]:
        """Get journal entries with optional filtering"""
        try:
            query = db.query(JournalEntry)
            
            # Apply filters
            if start_date:
                query = query.filter(JournalEntry.entry_date >= start_date)
            
            if end_date:
                query = query.filter(JournalEntry.entry_date <= end_date)
            
            if status:
                query = query.filter(JournalEntry.status == status)
            
            if account_id:
                # Filter by account in journal lines
                query = query.join(JournalLine).filter(JournalLine.account_id == account_id)
            
            # Order by entry date (newest first)
            query = query.order_by(JournalEntry.entry_date.desc(), JournalEntry.id.desc())
            
            # Apply pagination
            entries = query.offset(skip).limit(limit).all()
            
            return entries
            
        except Exception as e:
            logger.error(f"Error retrieving journal entries: {str(e)}")
            raise
    
    def get_journal_entry(self, db: Session, entry_id: int) -> Optional[JournalEntry]:
        """Get a specific journal entry by ID"""
        try:
            entry = db.query(JournalEntry).filter(
                JournalEntry.id == entry_id
            ).first()
            
            return entry
            
        except Exception as e:
            logger.error(f"Error retrieving journal entry {entry_id}: {str(e)}")
            raise
    
    def update_journal_entry(
        self, 
        db: Session, 
        entry_id: int, 
        entry_update: JournalEntryUpdate
    ) -> Optional[JournalEntry]:
        """Update an existing journal entry"""
        try:
            # Get existing entry
            db_entry = db.query(JournalEntry).filter(
                JournalEntry.id == entry_id
            ).first()
            
            if not db_entry:
                return None
            
            # Check if entry is posted
            if db_entry.status == "Posted":
                raise ValueError("Cannot update posted journal entry")
            
            # Update basic fields
            update_data = entry_update.dict(exclude_unset=True)
            
            for field, value in update_data.items():
                if field != "journal_lines":
                    setattr(db_entry, field, value)
            
            # Update journal lines if provided
            if entry_update.journal_lines is not None:
                # Delete existing lines
                db.query(JournalLine).filter(
                    JournalLine.journal_entry_id == entry_id
                ).delete()
                
                # Add new lines
                total_debits = Decimal("0")
                total_credits = Decimal("0")
                
                for line_data in entry_update.journal_lines:
                    # Validate account exists and is active
                    account = db.query(ChartOfAccounts).filter(
                        and_(
                            ChartOfAccounts.id == line_data.account_id,
                            ChartOfAccounts.is_active == True
                        )
                    ).first()
                    
                    if not account:
                        raise ValueError(f"Account {line_data.account_id} not found or inactive")
                    
                    db_line = JournalLine(
                        journal_entry_id=entry_id,
                        account_id=line_data.account_id,
                        line_number=line_data.line_number,
                        description=line_data.description,
                        debit_amount=line_data.debit_amount,
                        credit_amount=line_data.credit_amount
                    )
                    
                    db.add(db_line)
                    total_debits += line_data.debit_amount
                    total_credits += line_data.credit_amount
                
                # Update totals
                db_entry.total_debits = total_debits
                db_entry.total_credits = total_credits
                db_entry.is_balanced = total_debits == total_credits
                
                if not db_entry.is_balanced:
                    raise ValueError(f"Journal entry is not balanced. Debits: {total_debits}, Credits: {total_credits}")
            
            # Update timestamp
            db_entry.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(db_entry)
            
            logger.info(f"Updated journal entry: {db_entry.entry_number}")
            return db_entry
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating journal entry {entry_id}: {str(e)}")
            raise
    
    def post_journal_entry(self, db: Session, entry_id: int) -> bool:
        """Post a journal entry to the general ledger"""
        try:
            # Get journal entry
            db_entry = db.query(JournalEntry).filter(
                JournalEntry.id == entry_id
            ).first()
            
            if not db_entry:
                raise ValueError(f"Journal entry {entry_id} not found")
            
            if db_entry.status == "Posted":
                raise ValueError(f"Journal entry {entry_id} is already posted")
            
            if db_entry.status == "Void":
                raise ValueError(f"Cannot post voided journal entry {entry_id}")
            
            if not db_entry.is_balanced:
                raise ValueError(f"Cannot post unbalanced journal entry {entry_id}")
            
            # Update status to Posted
            db_entry.status = "Posted"
            db_entry.posted_at = datetime.utcnow()
            db_entry.updated_at = datetime.utcnow()
            
            # TODO: Create general ledger entries
            # This would typically create entries in a separate GL table
            # or update account balances
            
            db.commit()
            
            logger.info(f"Posted journal entry: {db_entry.entry_number}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error posting journal entry {entry_id}: {str(e)}")
            raise
    
    def void_journal_entry(self, db: Session, entry_id: int, reason: str) -> bool:
        """Void a journal entry"""
        try:
            # Get journal entry
            db_entry = db.query(JournalEntry).filter(
                JournalEntry.id == entry_id
            ).first()
            
            if not db_entry:
                raise ValueError(f"Journal entry {entry_id} not found")
            
            if db_entry.status == "Posted":
                raise ValueError(f"Cannot void posted journal entry {entry_id}. Create reversing entry instead.")
            
            if db_entry.status == "Void":
                raise ValueError(f"Journal entry {entry_id} is already voided")
            
            # Update status to Void
            db_entry.status = "Void"
            db_entry.updated_at = datetime.utcnow()
            # TODO: Add void reason field
            
            db.commit()
            
            logger.info(f"Voided journal entry: {db_entry.entry_number}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error voiding journal entry {entry_id}: {str(e)}")
            raise
    
    def create_reversing_entry(self, db: Session, entry_id: int, reverse_date: date) -> JournalEntry:
        """Create a reversing entry for a posted journal entry"""
        try:
            # Get original entry
            original_entry = db.query(JournalEntry).filter(
                JournalEntry.id == entry_id
            ).first()
            
            if not original_entry:
                raise ValueError(f"Journal entry {entry_id} not found")
            
            if original_entry.status != "Posted":
                raise ValueError(f"Cannot reverse non-posted journal entry {entry_id}")
            
            # Create reversing lines
            reversing_lines = []
            for line in original_entry.journal_lines:
                reversing_line = JournalLineCreate(
                    account_id=line.account_id,
                    line_number=line.line_number,
                    description=f"Reversal of {original_entry.entry_number}",
                    debit_amount=line.credit_amount,  # Reverse the amounts
                    credit_amount=line.debit_amount
                )
                reversing_lines.append(reversing_line)
            
            # Create reversing entry
            reversing_entry = JournalEntryCreate(
                entry_date=reverse_date,
                reference=f"REV-{original_entry.entry_number}",
                description=f"Reversing entry for {original_entry.entry_number}",
                entry_type="System",
                journal_lines=reversing_lines
            )
            
            return self.create_journal_entry(db, reversing_entry)
            
        except Exception as e:
            logger.error(f"Error creating reversing entry: {str(e)}")
            raise
    
    def _generate_entry_number(self, db: Session) -> str:
        """Generate unique journal entry number"""
        try:
            # Get current year
            current_year = datetime.utcnow().year
            
            # Get count of entries for current year
            count = db.query(JournalEntry).filter(
                func.extract('year', JournalEntry.created_at) == current_year
            ).count()
            
            # Format: JE-YYYY-XXXXX (e.g., JE-2024-00001)
            entry_number = f"JE-{current_year}-{count + 1:05d}"
            
            return entry_number
            
        except Exception as e:
            logger.error(f"Error generating entry number: {str(e)}")
            raise 