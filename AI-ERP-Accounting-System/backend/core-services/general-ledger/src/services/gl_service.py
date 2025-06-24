from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
import logging

from ..models.chart_of_accounts import ChartOfAccounts, ChartOfAccountsCreate, ChartOfAccountsUpdate
from ..database.connection import get_db

logger = logging.getLogger(__name__)

class GeneralLedgerService:
    """Service class for General Ledger operations"""
    
    def create_account(self, db: Session, account: ChartOfAccountsCreate) -> ChartOfAccounts:
        """Create a new chart of accounts entry"""
        try:
            # Check if account code already exists
            existing_account = db.query(ChartOfAccounts).filter(
                ChartOfAccounts.account_code == account.account_code
            ).first()
            
            if existing_account:
                raise ValueError(f"Account code {account.account_code} already exists")
            
            # Validate parent account if provided
            if account.parent_account_id:
                parent_account = db.query(ChartOfAccounts).filter(
                    ChartOfAccounts.id == account.parent_account_id
                ).first()
                if not parent_account:
                    raise ValueError(f"Parent account {account.parent_account_id} not found")
            
            # Create new account
            db_account = ChartOfAccounts(
                account_code=account.account_code,
                account_name=account.account_name,
                account_type=account.account_type,
                account_category=account.account_category,
                parent_account_id=account.parent_account_id,
                description=account.description,
                is_active=account.is_active,
                is_system_account=account.is_system_account,
                normal_balance=account.normal_balance
            )
            
            db.add(db_account)
            db.commit()
            db.refresh(db_account)
            
            logger.info(f"Created account: {account.account_code} - {account.account_name}")
            return db_account
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating account: {str(e)}")
            raise
    
    def get_accounts(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        account_type: Optional[str] = None,
        active: Optional[bool] = None
    ) -> List[ChartOfAccounts]:
        """Get chart of accounts with optional filtering"""
        try:
            query = db.query(ChartOfAccounts)
            
            # Apply filters
            if account_type:
                query = query.filter(ChartOfAccounts.account_type == account_type)
            
            if active is not None:
                query = query.filter(ChartOfAccounts.is_active == active)
            
            # Order by account code
            query = query.order_by(ChartOfAccounts.account_code)
            
            # Apply pagination
            accounts = query.offset(skip).limit(limit).all()
            
            return accounts
            
        except Exception as e:
            logger.error(f"Error retrieving accounts: {str(e)}")
            raise
    
    def get_account(self, db: Session, account_id: int) -> Optional[ChartOfAccounts]:
        """Get a specific account by ID"""
        try:
            account = db.query(ChartOfAccounts).filter(
                ChartOfAccounts.id == account_id
            ).first()
            
            return account
            
        except Exception as e:
            logger.error(f"Error retrieving account {account_id}: {str(e)}")
            raise
    
    def update_account(
        self, 
        db: Session, 
        account_id: int, 
        account_update: ChartOfAccountsUpdate
    ) -> Optional[ChartOfAccounts]:
        """Update an existing account"""
        try:
            # Get existing account
            db_account = db.query(ChartOfAccounts).filter(
                ChartOfAccounts.id == account_id
            ).first()
            
            if not db_account:
                return None
            
            # Update fields if provided
            update_data = account_update.dict(exclude_unset=True)
            
            for field, value in update_data.items():
                setattr(db_account, field, value)
            
            # Update timestamp
            db_account.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(db_account)
            
            logger.info(f"Updated account: {db_account.account_code}")
            return db_account
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating account {account_id}: {str(e)}")
            raise
    
    def delete_account(self, db: Session, account_id: int) -> bool:
        """Delete an account (soft delete by setting is_active to False)"""
        try:
            db_account = db.query(ChartOfAccounts).filter(
                ChartOfAccounts.id == account_id
            ).first()
            
            if not db_account:
                return False
            
            # Check if account has child accounts
            child_accounts = db.query(ChartOfAccounts).filter(
                ChartOfAccounts.parent_account_id == account_id,
                ChartOfAccounts.is_active == True
            ).count()
            
            if child_accounts > 0:
                raise ValueError(f"Cannot delete account with {child_accounts} active child accounts")
            
            # Soft delete
            db_account.is_active = False
            db_account.updated_at = datetime.utcnow()
            
            db.commit()
            
            logger.info(f"Deleted account: {db_account.account_code}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting account {account_id}: {str(e)}")
            raise
    
    def get_account_hierarchy(self, db: Session, account_id: Optional[int] = None) -> List[dict]:
        """Get account hierarchy (parent-child relationships)"""
        try:
            if account_id:
                # Get specific account and its children
                accounts = db.query(ChartOfAccounts).filter(
                    or_(
                        ChartOfAccounts.id == account_id,
                        ChartOfAccounts.parent_account_id == account_id
                    ),
                    ChartOfAccounts.is_active == True
                ).order_by(ChartOfAccounts.account_code).all()
            else:
                # Get all root accounts and their children
                accounts = db.query(ChartOfAccounts).filter(
                    ChartOfAccounts.parent_account_id.is_(None),
                    ChartOfAccounts.is_active == True
                ).order_by(ChartOfAccounts.account_code).all()
            
            def build_hierarchy(account_list, parent_id=None):
                hierarchy = []
                for account in account_list:
                    if account.parent_account_id == parent_id:
                        account_dict = {
                            "id": account.id,
                            "account_code": account.account_code,
                            "account_name": account.account_name,
                            "account_type": account.account_type,
                            "account_category": account.account_category,
                            "normal_balance": account.normal_balance,
                            "children": build_hierarchy(account_list, account.id)
                        }
                        hierarchy.append(account_dict)
                return hierarchy
            
            return build_hierarchy(accounts)
            
        except Exception as e:
            logger.error(f"Error retrieving account hierarchy: {str(e)}")
            raise
    
    def get_account_balance(
        self, 
        db: Session, 
        account_id: int, 
        as_of_date: Optional[datetime] = None
    ) -> dict:
        """Get account balance as of a specific date"""
        try:
            # This would integrate with journal entries to calculate balance
            # For now, return placeholder data
            account = self.get_account(db, account_id)
            if not account:
                raise ValueError(f"Account {account_id} not found")
            
            # TODO: Implement actual balance calculation from journal entries
            return {
                "account_id": account_id,
                "account_code": account.account_code,
                "account_name": account.account_name,
                "as_of_date": as_of_date or datetime.utcnow(),
                "debit_balance": Decimal("0.00"),
                "credit_balance": Decimal("0.00"),
                "net_balance": Decimal("0.00")
            }
            
        except Exception as e:
            logger.error(f"Error calculating account balance: {str(e)}")
            raise
    
    def validate_account_structure(self, db: Session) -> dict:
        """Validate chart of accounts structure"""
        try:
            # Check for duplicate account codes
            duplicate_codes = db.query(ChartOfAccounts.account_code).group_by(
                ChartOfAccounts.account_code
            ).having(
                db.func.count(ChartOfAccounts.id) > 1
            ).all()
            
            # Check for orphaned accounts (parent doesn't exist)
            orphaned_accounts = db.query(ChartOfAccounts).filter(
                and_(
                    ChartOfAccounts.parent_account_id.isnot(None),
                    ~db.query(ChartOfAccounts.id).filter(
                        ChartOfAccounts.id == ChartOfAccounts.parent_account_id
                    ).exists()
                )
            ).all()
            
            # Check for circular references
            # TODO: Implement circular reference detection
            
            return {
                "valid": len(duplicate_codes) == 0 and len(orphaned_accounts) == 0,
                "duplicate_codes": [code[0] for code in duplicate_codes],
                "orphaned_accounts": [acc.account_code for acc in orphaned_accounts],
                "total_accounts": db.query(ChartOfAccounts).count(),
                "active_accounts": db.query(ChartOfAccounts).filter(
                    ChartOfAccounts.is_active == True
                ).count()
            }
            
        except Exception as e:
            logger.error(f"Error validating account structure: {str(e)}")
            raise 