from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from decimal import Decimal
import logging

from ..models.vendors import Vendor, VendorCreate, VendorUpdate
from ..models.invoices import Invoice, InvoiceCreate, InvoiceUpdate
from ..models.purchase_orders import PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate
from ..database.connection import get_db

logger = logging.getLogger(__name__)

class AccountsPayableService:
    """Service class for Accounts Payable operations"""
    
    def create_purchase_order(self, db: Session, po: PurchaseOrderCreate) -> PurchaseOrder:
        """Create a new purchase order"""
        try:
            # Generate PO number
            po_number = self._generate_po_number(db)
            
            # Calculate totals
            total_amount = sum(line.quantity * line.unit_price for line in po.po_lines)
            
            # Create purchase order
            db_po = PurchaseOrder(
                po_number=po_number,
                vendor_id=po.vendor_id,
                order_date=po.order_date,
                expected_delivery_date=po.expected_delivery_date,
                status="Draft",
                total_amount=total_amount,
                currency=po.currency,
                notes=po.notes
            )
            
            db.add(db_po)
            db.flush()  # Get the ID without committing
            
            # Create PO lines
            for line_data in po.po_lines:
                db_line = PurchaseOrderLine(
                    purchase_order_id=db_po.id,
                    item_code=line_data.item_code,
                    description=line_data.description,
                    quantity=line_data.quantity,
                    unit_price=line_data.unit_price,
                    line_total=line_data.quantity * line_data.unit_price
                )
                db.add(db_line)
            
            db.commit()
            db.refresh(db_po)
            
            logger.info(f"Created purchase order: {po_number}")
            return db_po
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating purchase order: {str(e)}")
            raise
    
    def get_purchase_orders(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        vendor_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[PurchaseOrder]:
        """Get purchase orders with optional filtering"""
        try:
            query = db.query(PurchaseOrder)
            
            # Apply filters
            if vendor_id:
                query = query.filter(PurchaseOrder.vendor_id == vendor_id)
            
            if status:
                query = query.filter(PurchaseOrder.status == status)
            
            if start_date:
                query = query.filter(PurchaseOrder.order_date >= start_date)
            
            if end_date:
                query = query.filter(PurchaseOrder.order_date <= end_date)
            
            # Order by order date (newest first)
            query = query.order_by(PurchaseOrder.order_date.desc(), PurchaseOrder.id.desc())
            
            # Apply pagination
            pos = query.offset(skip).limit(limit).all()
            
            return pos
            
        except Exception as e:
            logger.error(f"Error retrieving purchase orders: {str(e)}")
            raise
    
    def get_purchase_order(self, db: Session, po_id: int) -> Optional[PurchaseOrder]:
        """Get a specific purchase order by ID"""
        try:
            po = db.query(PurchaseOrder).filter(
                PurchaseOrder.id == po_id
            ).first()
            
            return po
            
        except Exception as e:
            logger.error(f"Error retrieving purchase order {po_id}: {str(e)}")
            raise
    
    def update_purchase_order(
        self, 
        db: Session, 
        po_id: int, 
        po_update: PurchaseOrderUpdate
    ) -> Optional[PurchaseOrder]:
        """Update an existing purchase order"""
        try:
            # Get existing PO
            db_po = db.query(PurchaseOrder).filter(
                PurchaseOrder.id == po_id
            ).first()
            
            if not db_po:
                return None
            
            # Check if PO can be updated
            if db_po.status in ["Closed", "Cancelled"]:
                raise ValueError(f"Cannot update purchase order in {db_po.status} status")
            
            # Update fields
            update_data = po_update.dict(exclude_unset=True)
            
            for field, value in update_data.items():
                if field != "po_lines":
                    setattr(db_po, field, value)
            
            # Update PO lines if provided
            if po_update.po_lines is not None:
                # Delete existing lines
                db.query(PurchaseOrderLine).filter(
                    PurchaseOrderLine.purchase_order_id == po_id
                ).delete()
                
                # Add new lines
                total_amount = Decimal("0")
                for line_data in po_update.po_lines:
                    db_line = PurchaseOrderLine(
                        purchase_order_id=po_id,
                        item_code=line_data.item_code,
                        description=line_data.description,
                        quantity=line_data.quantity,
                        unit_price=line_data.unit_price,
                        line_total=line_data.quantity * line_data.unit_price
                    )
                    db.add(db_line)
                    total_amount += line_data.quantity * line_data.unit_price
                
                db_po.total_amount = total_amount
            
            # Update timestamp
            db_po.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(db_po)
            
            logger.info(f"Updated purchase order: {db_po.po_number}")
            return db_po
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating purchase order {po_id}: {str(e)}")
            raise
    
    def approve_purchase_order(self, db: Session, po_id: int) -> bool:
        """Approve a purchase order"""
        try:
            db_po = db.query(PurchaseOrder).filter(
                PurchaseOrder.id == po_id
            ).first()
            
            if not db_po:
                raise ValueError(f"Purchase order {po_id} not found")
            
            if db_po.status != "Draft":
                raise ValueError(f"Purchase order {po_id} is not in Draft status")
            
            # Update status
            db_po.status = "Approved"
            db_po.approved_at = datetime.utcnow()
            db_po.updated_at = datetime.utcnow()
            
            db.commit()
            
            logger.info(f"Approved purchase order: {db_po.po_number}")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error approving purchase order {po_id}: {str(e)}")
            raise
    
    def perform_three_way_match(
        self, 
        db: Session, 
        invoice_id: int, 
        po_id: Optional[int] = None, 
        receipt_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Perform three-way matching (PO, Invoice, Receipt)"""
        try:
            # Get invoice
            invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
            if not invoice:
                raise ValueError(f"Invoice {invoice_id} not found")
            
            match_result = {
                "invoice_id": invoice_id,
                "po_id": po_id,
                "receipt_id": receipt_id,
                "matched": False,
                "discrepancies": [],
                "match_score": 0.0
            }
            
            # Two-way match (Invoice vs PO)
            if po_id:
                po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
                if po:
                    po_match = self._match_invoice_to_po(invoice, po)
                    match_result["po_match"] = po_match
                    match_result["match_score"] += po_match["score"] * 0.5
            
            # Two-way match (Invoice vs Receipt)
            if receipt_id:
                receipt = db.query(Receipt).filter(Receipt.id == receipt_id).first()
                if receipt:
                    receipt_match = self._match_invoice_to_receipt(invoice, receipt)
                    match_result["receipt_match"] = receipt_match
                    match_result["match_score"] += receipt_match["score"] * 0.5
            
            # Three-way match
            if po_id and receipt_id:
                three_way_match = self._perform_three_way_match_logic(invoice, po, receipt)
                match_result["three_way_match"] = three_way_match
                match_result["matched"] = three_way_match["matched"]
            else:
                # Two-way match only
                match_result["matched"] = match_result["match_score"] >= 0.8
            
            return match_result
            
        except Exception as e:
            logger.error(f"Error performing three-way match: {str(e)}")
            raise
    
    def generate_aging_report(
        self, 
        db: Session, 
        as_of_date: date, 
        vendor_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate accounts payable aging report"""
        try:
            # Get unpaid invoices
            query = db.query(Invoice).filter(
                and_(
                    Invoice.status == "Approved",
                    Invoice.due_date <= as_of_date,
                    Invoice.paid_amount < Invoice.total_amount
                )
            )
            
            if vendor_id:
                query = query.filter(Invoice.vendor_id == vendor_id)
            
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
                "vendor_id": vendor_id,
                "aging_buckets": aging_buckets,
                "total_outstanding": total_outstanding,
                "total_invoices": len(invoices)
            }
            
        except Exception as e:
            logger.error(f"Error generating aging report: {str(e)}")
            raise
    
    def generate_vendor_analysis(
        self, 
        db: Session, 
        start_date: date, 
        end_date: date, 
        vendor_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate vendor analysis report"""
        try:
            # Get invoices for the period
            query = db.query(Invoice).filter(
                and_(
                    Invoice.invoice_date >= start_date,
                    Invoice.invoice_date <= end_date
                )
            )
            
            if vendor_id:
                query = query.filter(Invoice.vendor_id == vendor_id)
            
            invoices = query.all()
            
            # Calculate metrics
            total_invoiced = sum(inv.total_amount for inv in invoices)
            total_paid = sum(inv.paid_amount for inv in invoices)
            total_outstanding = total_invoiced - total_paid
            
            # Calculate average payment time
            paid_invoices = [inv for inv in invoices if inv.paid_amount > 0]
            avg_payment_days = 0
            if paid_invoices:
                total_days = sum(
                    (inv.payment_date - inv.invoice_date).days 
                    for inv in paid_invoices 
                    if inv.payment_date
                )
                avg_payment_days = total_days / len(paid_invoices)
            
            # Vendor breakdown
            vendor_breakdown = {}
            for invoice in invoices:
                vendor_name = invoice.vendor.name if invoice.vendor else "Unknown"
                if vendor_name not in vendor_breakdown:
                    vendor_breakdown[vendor_name] = {
                        "total_invoiced": Decimal("0"),
                        "total_paid": Decimal("0"),
                        "invoice_count": 0
                    }
                
                vendor_breakdown[vendor_name]["total_invoiced"] += invoice.total_amount
                vendor_breakdown[vendor_name]["total_paid"] += invoice.paid_amount
                vendor_breakdown[vendor_name]["invoice_count"] += 1
            
            return {
                "start_date": start_date,
                "end_date": end_date,
                "vendor_id": vendor_id,
                "total_invoiced": total_invoiced,
                "total_paid": total_paid,
                "total_outstanding": total_outstanding,
                "avg_payment_days": avg_payment_days,
                "vendor_breakdown": vendor_breakdown,
                "invoice_count": len(invoices)
            }
            
        except Exception as e:
            logger.error(f"Error generating vendor analysis: {str(e)}")
            raise
    
    def _generate_po_number(self, db: Session) -> str:
        """Generate unique purchase order number"""
        try:
            current_year = datetime.utcnow().year
            count = db.query(PurchaseOrder).filter(
                func.extract('year', PurchaseOrder.created_at) == current_year
            ).count()
            
            po_number = f"PO-{current_year}-{count + 1:05d}"
            return po_number
            
        except Exception as e:
            logger.error(f"Error generating PO number: {str(e)}")
            raise
    
    def _match_invoice_to_po(self, invoice: Invoice, po: PurchaseOrder) -> Dict[str, Any]:
        """Match invoice to purchase order"""
        # TODO: Implement detailed matching logic
        return {
            "matched": True,
            "score": 0.9,
            "discrepancies": []
        }
    
    def _match_invoice_to_receipt(self, invoice: Invoice, receipt: Any) -> Dict[str, Any]:
        """Match invoice to receipt"""
        # TODO: Implement detailed matching logic
        return {
            "matched": True,
            "score": 0.8,
            "discrepancies": []
        }
    
    def _perform_three_way_match_logic(self, invoice: Invoice, po: PurchaseOrder, receipt: Any) -> Dict[str, Any]:
        """Perform three-way matching logic"""
        # TODO: Implement detailed three-way matching logic
        return {
            "matched": True,
            "score": 0.95,
            "discrepancies": []
        } 