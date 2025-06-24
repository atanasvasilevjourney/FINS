from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime, date
from decimal import Decimal

from .database.connection import get_db
from .models.vendors import Vendor, VendorCreate, VendorUpdate
from .models.invoices import Invoice, InvoiceCreate, InvoiceUpdate, InvoiceLine
from .models.payments import Payment, PaymentCreate, PaymentUpdate
from .models.purchase_orders import PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate
from .services.ap_service import AccountsPayableService
from .services.invoice_service import InvoiceService
from .services.payment_service import PaymentService
from .services.vendor_service import VendorService
from .utils.validators import validate_invoice, validate_payment
from .utils.helpers import format_currency

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FINS ERP - Accounts Payable Service",
    description="Accounts Payable microservice for FINS ERP System",
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
ap_service = AccountsPayableService()
invoice_service = InvoiceService()
payment_service = PaymentService()
vendor_service = VendorService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Accounts Payable",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "service": "Accounts Payable",
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }

# Vendor Management endpoints
@app.post("/vendors", response_model=Vendor, status_code=status.HTTP_201_CREATED)
async def create_vendor(
    vendor: VendorCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new vendor"""
    try:
        return vendor_service.create_vendor(db, vendor)
    except Exception as e:
        logger.error(f"Error creating vendor: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vendors", response_model=List[Vendor])
async def get_vendors(
    skip: int = 0,
    limit: int = 100,
    active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get vendors with optional filtering"""
    try:
        return vendor_service.get_vendors(db, skip=skip, limit=limit, active=active, search=search)
    except Exception as e:
        logger.error(f"Error retrieving vendors: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/vendors/{vendor_id}", response_model=Vendor)
async def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific vendor by ID"""
    try:
        vendor = vendor_service.get_vendor(db, vendor_id)
        if not vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return vendor
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving vendor {vendor_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/vendors/{vendor_id}", response_model=Vendor)
async def update_vendor(
    vendor_id: int,
    vendor: VendorUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update an existing vendor"""
    try:
        updated_vendor = vendor_service.update_vendor(db, vendor_id, vendor)
        if not updated_vendor:
            raise HTTPException(status_code=404, detail="Vendor not found")
        return updated_vendor
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating vendor {vendor_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Purchase Order endpoints
@app.post("/purchase-orders", response_model=PurchaseOrder, status_code=status.HTTP_201_CREATED)
async def create_purchase_order(
    po: PurchaseOrderCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new purchase order"""
    try:
        return ap_service.create_purchase_order(db, po)
    except Exception as e:
        logger.error(f"Error creating purchase order: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/purchase-orders", response_model=List[PurchaseOrder])
async def get_purchase_orders(
    skip: int = 0,
    limit: int = 100,
    vendor_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get purchase orders with optional filtering"""
    try:
        return ap_service.get_purchase_orders(
            db, skip=skip, limit=limit, vendor_id=vendor_id,
            status=status, start_date=start_date, end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error retrieving purchase orders: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/purchase-orders/{po_id}", response_model=PurchaseOrder)
async def get_purchase_order(
    po_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific purchase order by ID"""
    try:
        po = ap_service.get_purchase_order(db, po_id)
        if not po:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return po
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving purchase order {po_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/purchase-orders/{po_id}", response_model=PurchaseOrder)
async def update_purchase_order(
    po_id: int,
    po: PurchaseOrderUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update an existing purchase order"""
    try:
        updated_po = ap_service.update_purchase_order(db, po_id, po)
        if not updated_po:
            raise HTTPException(status_code=404, detail="Purchase order not found")
        return updated_po
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating purchase order {po_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Invoice Management endpoints
@app.post("/invoices", response_model=Invoice, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new invoice"""
    try:
        # Validate invoice
        validation_result = validate_invoice(invoice)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"])
        
        return invoice_service.create_invoice(db, invoice)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating invoice: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/invoices/upload")
async def upload_invoice(
    file: UploadFile = File(...),
    vendor_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Upload and process invoice document (OCR)"""
    try:
        # This would integrate with OCR service for invoice processing
        result = invoice_service.process_invoice_upload(db, file, vendor_id)
        return {"message": "Invoice uploaded and processed", "invoice_id": result.id}
    except Exception as e:
        logger.error(f"Error uploading invoice: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/invoices", response_model=List[Invoice])
async def get_invoices(
    skip: int = 0,
    limit: int = 100,
    vendor_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get invoices with optional filtering"""
    try:
        return invoice_service.get_invoices(
            db, skip=skip, limit=limit, vendor_id=vendor_id,
            status=status, start_date=start_date, end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error retrieving invoices: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/invoices/{invoice_id}", response_model=Invoice)
async def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific invoice by ID"""
    try:
        invoice = invoice_service.get_invoice(db, invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return invoice
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving invoice {invoice_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/invoices/{invoice_id}", response_model=Invoice)
async def update_invoice(
    invoice_id: int,
    invoice: InvoiceUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update an existing invoice"""
    try:
        updated_invoice = invoice_service.update_invoice(db, invoice_id, invoice)
        if not updated_invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        return updated_invoice
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating invoice {invoice_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/invoices/{invoice_id}/approve")
async def approve_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Approve an invoice for payment"""
    try:
        result = invoice_service.approve_invoice(db, invoice_id)
        return {"message": "Invoice approved successfully", "invoice_id": invoice_id}
    except Exception as e:
        logger.error(f"Error approving invoice {invoice_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Payment Management endpoints
@app.post("/payments", response_model=Payment, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new payment"""
    try:
        # Validate payment
        validation_result = validate_payment(payment)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"])
        
        return payment_service.create_payment(db, payment)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/payments", response_model=List[Payment])
async def get_payments(
    skip: int = 0,
    limit: int = 100,
    vendor_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get payments with optional filtering"""
    try:
        return payment_service.get_payments(
            db, skip=skip, limit=limit, vendor_id=vendor_id,
            status=status, start_date=start_date, end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error retrieving payments: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/payments/{payment_id}", response_model=Payment)
async def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific payment by ID"""
    try:
        payment = payment_service.get_payment(db, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        return payment
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving payment {payment_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/payments/{payment_id}/process")
async def process_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Process a payment (execute bank transfer)"""
    try:
        result = payment_service.process_payment(db, payment_id)
        return {"message": "Payment processed successfully", "payment_id": payment_id}
    except Exception as e:
        logger.error(f"Error processing payment {payment_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Three-way matching
@app.post("/invoices/{invoice_id}/match")
async def three_way_match(
    invoice_id: int,
    po_id: Optional[int] = None,
    receipt_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Perform three-way matching (PO, Invoice, Receipt)"""
    try:
        result = ap_service.perform_three_way_match(db, invoice_id, po_id, receipt_id)
        return {"message": "Three-way matching completed", "match_result": result}
    except Exception as e:
        logger.error(f"Error performing three-way match: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Reporting endpoints
@app.get("/reports/aging")
async def get_aging_report(
    as_of_date: date,
    vendor_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get accounts payable aging report"""
    try:
        return ap_service.generate_aging_report(db, as_of_date, vendor_id)
    except Exception as e:
        logger.error(f"Error generating aging report: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reports/vendor-analysis")
async def get_vendor_analysis(
    start_date: date,
    end_date: date,
    vendor_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get vendor analysis report"""
    try:
        return ap_service.generate_vendor_analysis(db, start_date, end_date, vendor_id)
    except Exception as e:
        logger.error(f"Error generating vendor analysis: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 