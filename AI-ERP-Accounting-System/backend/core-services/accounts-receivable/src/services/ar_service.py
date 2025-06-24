from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from decimal import Decimal
import logging

from ..models.customers import Customer, CustomerCreate, CustomerUpdate
from ..models.invoices import Invoice, InvoiceCreate, InvoiceUpdate
from ..models.sales_orders import SalesOrder, SalesOrderCreate, SalesOrderUpdate
from ..models.collections import Collection, CollectionCreate, CollectionUpdate
from ..database.connection import get_db

logger = logging.getLogger(__name__)

class AccountsReceivableService:
    """Service class for Accounts Receivable operations"""
    
    def create_sales_order(self, db: Session, so: SalesOrderCreate) -> SalesOrder:
        """Create a new sales order"""
        try:
            # Generate SO number
            so_number = self._generate_so_number(db)
            
            # Calculate totals
            total_amount = sum(line.quantity * line.unit_price for line in so.so_lines)
            
            # Create sales order
            db_so = SalesOrder(
                so_number=so_number,
                customer_id=so.customer_id,
                order_date=so.order_date,
                expected_delivery_date=so.expected_delivery_date,
                status="Draft",
                total_amount=total_amount,
                currency=so.currency,
                notes=so.notes
            )
            
            db.add(db_so)
            db.flush()  # Get the ID without committing
            
            # Create SO lines
            for line_data in so.so_lines:
                db_line = SalesOrderLine(
                    sales_order_id=db_so.id,
                    item_code=line_data.item_code,
                    description=line_data.description,
                    quantity=line_data.quantity,
                    unit_price=line_data.unit_price,
                    line_total=line_data.quantity * line_data.unit_price
                )
                db.add(db_line)
            
            db.commit()
            db.refresh(db_so)
            
            logger.info(f"Created sales order: {so_number}")
            return db_so
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating sales order: {str(e)}")
            raise
    
    def get_sales_orders(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        customer_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[SalesOrder]:
        """Get sales orders with optional filtering"""
        try:
            query = db.query(SalesOrder)
            
            # Apply filters
            if customer_id:
                query = query.filter(SalesOrder.customer_id == customer_id)
            
            if status:
                query = query.filter(SalesOrder.status == status)
            
            if start_date:
                query = query.filter(SalesOrder.order_date >= start_date)
            
            if end_date:
                query = query.filter(SalesOrder.order_date <= end_date)
            
            # Order by order date (newest first)
            query = query.order_by(SalesOrder.order_date.desc(), SalesOrder.id.desc())
            
            # Apply pagination
            sos = query.offset(skip).limit(limit).all()
            
            return sos
            
        except Exception as e:
            logger.error(f"Error retrieving sales orders: {str(e)}")
            raise
    
    def get_sales_order(self, db: Session, so_id: int) -> Optional[SalesOrder]:
        """Get a specific sales order by ID"""
        try:
            so = db.query(SalesOrder).filter(
                SalesOrder.id == so_id
            ).first()
            
            return so
            
        except Exception as e:
            logger.error(f"Error retrieving sales order {so_id}: {str(e)}")
            raise
    
    def update_sales_order(
        self, 
        db: Session, 
        so_id: int, 
        so_update: SalesOrderUpdate
    ) -> Optional[SalesOrder]:
        """Update an existing sales order"""
        try:
            # Get existing SO
            db_so = db.query(SalesOrder).filter(
                SalesOrder.id == so_id
            ).first()
            
            if not db_so:
                return None
            
            # Check if SO can be updated
            if db_so.status in ["Shipped", "Delivered", "Cancelled"]:
                raise ValueError(f"Cannot update sales order in {db_so.status} status")
            
            # Update fields
            update_data = so_update.dict(exclude_unset=True)
            
            for field, value in update_data.items():
                if field != "so_lines":
                    setattr(db_so, field, value)
            
            # Update SO lines if provided
            if so_update.so_lines is not None:
                # Delete existing lines
                db.query(SalesOrderLine).filter(
                    SalesOrderLine.sales_order_id == so_id
                ).delete()
                
                # Add new lines
                total_amount = Decimal("0")
                for line_data in so_update.so_lines:
                    db_line = SalesOrderLine(
                        sales_order_id=so_id,
                        item_code=line_data.item_code,
                        description=line_data.description,
                        quantity=line_data.quantity,
                        unit_price=line_data.unit_price,
                        line_total=line_data.quantity * line_data.unit_price
                    )
                    db.add(db_line)
                    total_amount += line_data.quantity * line_data.unit_price
                
                db_so.total_amount = total_amount
            
            # Update timestamp
            db_so.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(db_so)
            
            logger.info(f"Updated sales order: {db_so.so_number}")
            return db_so
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating sales order {so_id}: {str(e)}")
            raise
    
    def generate_invoice_from_order(self, db: Session, so_id: int) -> Invoice:
        """Generate invoice from sales order"""
        try:
            # Get sales order
            so = db.query(SalesOrder).filter(
                SalesOrder.id == so_id
            ).first()
            
            if not so:
                raise ValueError(f"Sales order {so_id} not found")
            
            if so.status not in ["Approved", "Shipped"]:
                raise ValueError(f"Cannot generate invoice from sales order in {so.status} status")
            
            # Check if invoice already exists
            existing_invoice = db.query(Invoice).filter(
                Invoice.sales_order_id == so_id
            ).first()
            
            if existing_invoice:
                raise ValueError(f"Invoice already exists for sales order {so_id}")
            
            # Generate invoice number
            invoice_number = self._generate_invoice_number(db)
            
            # Calculate due date (30 days from invoice date)
            invoice_date = date.today()
            due_date = invoice_date + timedelta(days=30)
            
            # Create invoice
            invoice = Invoice(
                invoice_number=invoice_number,
                customer_id=so.customer_id,
                sales_order_id=so_id,
                invoice_date=invoice_date,
                due_date=due_date,
                status="Draft",
                total_amount=so.total_amount,
                currency=so.currency,
                notes=f"Invoice generated from sales order {so.so_number}"
            )
            
            db.add(invoice)
            db.flush()
            
            # Create invoice lines from SO lines
            for so_line in so.so_lines:
                invoice_line = InvoiceLine(
                    invoice_id=invoice.id,
                    item_code=so_line.item_code,
                    description=so_line.description,
                    quantity=so_line.quantity,
                    unit_price=so_line.unit_price,
                    line_total=so_line.line_total
                )
                db.add(invoice_line)
            
            db.commit()
            db.refresh(invoice)
            
            logger.info(f"Generated invoice {invoice_number} from sales order {so.so_number}")
            return invoice
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error generating invoice from order: {str(e)}")
            raise
    
    def generate_aging_report(
        self, 
        db: Session, 
        as_of_date: date, 
        customer_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate accounts receivable aging report"""
        try:
            # Get unpaid invoices
            query = db.query(Invoice).filter(
                and_(
                    Invoice.status == "Sent",
                    Invoice.due_date <= as_of_date,
                    Invoice.paid_amount < Invoice.total_amount
                )
            )
            
            if customer_id:
                query = query.filter(Invoice.customer_id == customer_id)
            
            invoices = query.all()
            
            # Calculate aging buckets
            aging_buckets = {
                "current": {"amount": Decimal("0"), "count": 0},
                "1_30_days": {"amount": Decimal("0"), "count": 0},
                "31_60_days": {"amount": Decimal("0"), "count": 0},
                "61_90_days": {"amount": Decimal("0"), "count": 0},
                "over_90_days": {"amount": Decimal("0"), "count": 0}
            }
            
            total_outstanding = Decimal("0")
            
            for invoice in invoices:
                outstanding_amount = invoice.total_amount - invoice.paid_amount
                days_overdue = (as_of_date - invoice.due_date).days
                
                if days_overdue <= 0:
                    bucket = "current"
                elif days_overdue <= 30:
                    bucket = "1_30_days"
                elif days_overdue <= 60:
                    bucket = "31_60_days"
                elif days_overdue <= 90:
                    bucket = "61_90_days"
                else:
                    bucket = "over_90_days"
                
                aging_buckets[bucket]["amount"] += outstanding_amount
                aging_buckets[bucket]["count"] += 1
                total_outstanding += outstanding_amount
            
            return {
                "as_of_date": as_of_date,
                "customer_id": customer_id,
                "aging_buckets": aging_buckets,
                "total_outstanding": total_outstanding,
                "total_invoices": len(invoices)
            }
            
        except Exception as e:
            logger.error(f"Error generating aging report: {str(e)}")
            raise
    
    def generate_customer_analysis(
        self, 
        db: Session, 
        start_date: date, 
        end_date: date, 
        customer_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate customer analysis report"""
        try:
            # Get invoices for the period
            query = db.query(Invoice).filter(
                and_(
                    Invoice.invoice_date >= start_date,
                    Invoice.invoice_date <= end_date
                )
            )
            
            if customer_id:
                query = query.filter(Invoice.customer_id == customer_id)
            
            invoices = query.all()
            
            # Calculate metrics
            total_invoiced = sum(inv.total_amount for inv in invoices)
            total_paid = sum(inv.paid_amount for inv in invoices)
            total_outstanding = total_invoiced - total_paid
            
            # Calculate average collection time
            paid_invoices = [inv for inv in invoices if inv.paid_amount > 0]
            avg_collection_days = 0
            if paid_invoices:
                total_days = sum(
                    (inv.payment_date - inv.invoice_date).days 
                    for inv in paid_invoices 
                    if inv.payment_date
                )
                avg_collection_days = total_days / len(paid_invoices)
            
            # Customer breakdown
            customer_breakdown = {}
            for invoice in invoices:
                customer_name = invoice.customer.name if invoice.customer else "Unknown"
                if customer_name not in customer_breakdown:
                    customer_breakdown[customer_name] = {
                        "total_invoiced": Decimal("0"),
                        "total_paid": Decimal("0"),
                        "invoice_count": 0
                    }
                
                customer_breakdown[customer_name]["total_invoiced"] += invoice.total_amount
                customer_breakdown[customer_name]["total_paid"] += invoice.paid_amount
                customer_breakdown[customer_name]["invoice_count"] += 1
            
            return {
                "start_date": start_date,
                "end_date": end_date,
                "customer_id": customer_id,
                "total_invoiced": total_invoiced,
                "total_paid": total_paid,
                "total_outstanding": total_outstanding,
                "avg_collection_days": avg_collection_days,
                "customer_breakdown": customer_breakdown,
                "invoice_count": len(invoices)
            }
            
        except Exception as e:
            logger.error(f"Error generating customer analysis: {str(e)}")
            raise
    
    def _generate_so_number(self, db: Session) -> str:
        """Generate unique sales order number"""
        try:
            current_year = datetime.utcnow().year
            count = db.query(SalesOrder).filter(
                func.extract('year', SalesOrder.created_at) == current_year
            ).count()
            
            so_number = f"SO-{current_year}-{count + 1:05d}"
            return so_number
            
        except Exception as e:
            logger.error(f"Error generating SO number: {str(e)}")
            raise
    
    def _generate_invoice_number(self, db: Session) -> str:
        """Generate unique invoice number"""
        try:
            current_year = datetime.utcnow().year
            count = db.query(Invoice).filter(
                func.extract('year', Invoice.created_at) == current_year
            ).count()
            
            invoice_number = f"INV-{current_year}-{count + 1:05d}"
            return invoice_number
            
        except Exception as e:
            logger.error(f"Error generating invoice number: {str(e)}")
            raise 