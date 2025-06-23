import pandas as pd
from typing import Dict, List, Optional

class AccountingEngine:
    def __init__(self):
        self.transactions = []
        self.accounts = {}
        self.ledger = pd.DataFrame()
        
    def add_transaction(self, date: str, description: str, amount: float, 
                       account: str, transaction_type: str = "expense"):
        """Add a new transaction to the accounting system"""
        transaction = {
            'date': date,
            'description': description,
            'amount': amount,
            'account': account,
            'type': transaction_type
        }
        self.transactions.append(transaction)
        return True
        
    def get_balance_sheet(self) -> pd.DataFrame:
        """Generate a basic balance sheet"""
        if not self.transactions:
            return pd.DataFrame()
            
        df = pd.DataFrame(self.transactions)
        balance_sheet = df.groupby('account')['amount'].sum().reset_index()
        return balance_sheet
        
    def get_income_statement(self) -> pd.DataFrame:
        """Generate a basic income statement"""
        if not self.transactions:
            return pd.DataFrame()
            
        df = pd.DataFrame(self.transactions)
        income_stmt = df.groupby('type')['amount'].sum().reset_index()
        return income_stmt
        
    def export_to_csv(self, filename: str) -> bool:
        """Export transactions to CSV"""
        try:
            df = pd.DataFrame(self.transactions)
            df.to_csv(filename, index=False)
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False 