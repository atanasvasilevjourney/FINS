from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime, date
from decimal import Decimal

from .database.connection import get_db
from .models.customers import Customer, CustomerCreate, CustomerUpdate
from .models.invoices import Invoice, InvoiceCreate, InvoiceUpdate, InvoiceLine
from .models.payments import Payment, PaymentCreate, PaymentUpdate
from .models.sales_orders import SalesOrder, SalesOrderCreate, SalesOrderUpdate
from .models.collections import Collection, CollectionCreate, CollectionUpdate
from .services.ar_service import AccountsReceivableService
from .services.invoice_service import InvoiceService
from .services.payment_service import PaymentService
from .services.customer_service import CustomerService
from .services.collection_service import CollectionService
from .utils.validators import validate_invoice, validate_payment
from .utils.helpers import format_currency

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FINS ERP - Accounts Receivable Service",
    description="Accounts Receivable microservice for FINS ERP System",
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
ar_service = AccountsReceivableService()
invoice_service = InvoiceService()
payment_service = PaymentService()
customer_service = CustomerService()
collection_service = CollectionService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Accounts Receivable",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "service": "Accounts Receivable",
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }

# Customer Management endpoints
@app.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new customer"""
    try:
        return customer_service.create_customer(db, customer)
    except Exception as e:
        logger.error(f"Error creating customer: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/customers", response_model=List[Customer])
async def get_customers(
    skip: int = 0,
    limit: int = 100,
    active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get customers with optional filtering"""
    try:
        return customer_service.get_customers(db, skip=skip, limit=limit, active=active, search=search)
    except Exception as e:
        logger.error(f"Error retrieving customers: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific customer by ID"""
    try:
        customer = customer_service.get_customer(db, customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving customer {customer_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update an existing customer"""
    try:
        updated_customer = customer_service.update_customer(db, customer_id, customer)
        if not updated_customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return updated_customer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating customer {customer_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/customers/{customer_id}/credit-check")
async def perform_credit_check(
    customer_id: int,
    amount: Decimal,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Perform credit check for a customer"""
    try:
        result = customer_service.perform_credit_check(db, customer_id, amount)
        return {"credit_approved": result["approved"], "credit_limit": result["limit"], "risk_score": result["risk_score"]}
    except Exception as e:
        logger.error(f"Error performing credit check: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Sales Order endpoints
@app.post("/sales-orders", response_model=SalesOrder, status_code=status.HTTP_201_CREATED)
async def create_sales_order(
    so: SalesOrderCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new sales order"""
    try:
        return ar_service.create_sales_order(db, so)
    except Exception as e:
        logger.error(f"Error creating sales order: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sales-orders", response_model=List[SalesOrder])
async def get_sales_orders(
    skip: int = 0,
    limit: int = 100,
    customer_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get sales orders with optional filtering"""
    try:
        return ar_service.get_sales_orders(
            db, skip=skip, limit=limit, customer_id=customer_id,
            status=status, start_date=start_date, end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error retrieving sales orders: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sales-orders/{so_id}", response_model=SalesOrder)
async def get_sales_order(
    so_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific sales order by ID"""
    try:
        so = ar_service.get_sales_order(db, so_id)
        if not so:
            raise HTTPException(status_code=404, detail="Sales order not found")
        return so
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving sales order {so_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/sales-orders/{so_id}", response_model=SalesOrder)
async def update_sales_order(
    so_id: int,
    so: SalesOrderUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update an existing sales order"""
    try:
        updated_so = ar_service.update_sales_order(db, so_id, so)
        if not updated_so:
            raise HTTPException(status_code=404, detail="Sales order not found")
        return updated_so
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating sales order {so_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Invoice Management endpoints
@app.post("/invoices", response_model=Invoice, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new customer invoice"""
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

@app.post("/invoices/generate-from-order/{so_id}")
async def generate_invoice_from_order(
    so_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate invoice from sales order"""
    try:
        invoice = ar_service.generate_invoice_from_order(db, so_id)
        return {"message": "Invoice generated successfully", "invoice_id": invoice.id}
    except Exception as e:
        logger.error(f"Error generating invoice from order: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/invoices", response_model=List[Invoice])
async def get_invoices(
    skip: int = 0,
    limit: int = 100,
    customer_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get invoices with optional filtering"""
    try:
        return invoice_service.get_invoices(
            db, skip=skip, limit=limit, customer_id=customer_id,
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

@app.post("/invoices/{invoice_id}/send")
async def send_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Send invoice to customer"""
    try:
        result = invoice_service.send_invoice(db, invoice_id)
        return {"message": "Invoice sent successfully", "invoice_id": invoice_id}
    except Exception as e:
        logger.error(f"Error sending invoice {invoice_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Payment Management endpoints
@app.post("/payments", response_model=Payment, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new payment receipt"""
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

@app.post("/payments/apply")
async def apply_payment(
    payment_id: int,
    invoice_ids: List[int],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Apply payment to specific invoices"""
    try:
        result = payment_service.apply_payment_to_invoices(db, payment_id, invoice_ids)
        return {"message": "Payment applied successfully", "payment_id": payment_id}
    except Exception as e:
        logger.error(f"Error applying payment: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/payments", response_model=List[Payment])
async def get_payments(
    skip: int = 0,
    limit: int = 100,
    customer_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get payments with optional filtering"""
    try:
        return payment_service.get_payments(
            db, skip=skip, limit=limit, customer_id=customer_id,
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

# Collections Management endpoints
@app.post("/collections", response_model=Collection, status_code=status.HTTP_201_CREATED)
async def create_collection(
    collection: CollectionCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new collection activity"""
    try:
        return collection_service.create_collection(db, collection)
    except Exception as e:
        logger.error(f"Error creating collection: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/collections", response_model=List[Collection])
async def get_collections(
    skip: int = 0,
    limit: int = 100,
    customer_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get collections with optional filtering"""
    try:
        return collection_service.get_collections(
            db, skip=skip, limit=limit, customer_id=customer_id,
            status=status, start_date=start_date, end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error retrieving collections: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/collections/automated-dunning")
async def run_automated_dunning(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Run automated dunning process"""
    try:
        result = collection_service.run_automated_dunning(db)
        return {"message": "Automated dunning completed", "processed": result["processed"]}
    except Exception as e:
        logger.error(f"Error running automated dunning: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Reporting endpoints
@app.get("/reports/aging")
async def get_aging_report(
    as_of_date: date,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get accounts receivable aging report"""
    try:
        return ar_service.generate_aging_report(db, as_of_date, customer_id)
    except Exception as e:
        logger.error(f"Error generating aging report: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reports/customer-analysis")
async def get_customer_analysis(
    start_date: date,
    end_date: date,
    customer_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get customer analysis report"""
    try:
        return ar_service.generate_customer_analysis(db, start_date, end_date, customer_id)
    except Exception as e:
        logger.error(f"Error generating customer analysis: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reports/collections-performance")
async def get_collections_performance(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get collections performance report"""
    try:
        return collection_service.generate_performance_report(db, start_date, end_date)
    except Exception as e:
        logger.error(f"Error generating collections performance report: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 