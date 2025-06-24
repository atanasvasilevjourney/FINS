from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime, date
from decimal import Decimal

from .database.connection import get_db
from .models.suppliers import Supplier, SupplierCreate, SupplierUpdate
from .models.purchase_requisitions import PurchaseRequisition, PurchaseRequisitionCreate, PurchaseRequisitionUpdate
from .models.rfqs import RFQ, RFQCreate, RFQUpdate
from .models.purchase_orders import PurchaseOrder, PurchaseOrderCreate, PurchaseOrderUpdate
from .models.contracts import Contract, ContractCreate, ContractUpdate
from .services.procurement_service import ProcurementService
from .services.supplier_service import SupplierService
from .services.rfq_service import RFQService
from .utils.validators import validate_purchase_requisition
from .utils.helpers import format_currency

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FINS ERP - Procurement Service",
    description="Procurement microservice for FINS ERP System",
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
procurement_service = ProcurementService()
supplier_service = SupplierService()
rfq_service = RFQService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Procurement",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "service": "Procurement",
        "status": "healthy",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }

# Supplier Management endpoints
@app.post("/suppliers", response_model=Supplier, status_code=status.HTTP_201_CREATED)
async def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new supplier"""
    try:
        return supplier_service.create_supplier(db, supplier)
    except Exception as e:
        logger.error(f"Error creating supplier: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/suppliers", response_model=List[Supplier])
async def get_suppliers(
    skip: int = 0,
    limit: int = 100,
    active: Optional[bool] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get suppliers with optional filtering"""
    try:
        return supplier_service.get_suppliers(
            db, skip=skip, limit=limit, active=active, 
            category=category, search=search
        )
    except Exception as e:
        logger.error(f"Error retrieving suppliers: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/suppliers/{supplier_id}", response_model=Supplier)
async def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific supplier by ID"""
    try:
        supplier = supplier_service.get_supplier(db, supplier_id)
        if not supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return supplier
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving supplier {supplier_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/suppliers/{supplier_id}", response_model=Supplier)
async def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update an existing supplier"""
    try:
        updated_supplier = supplier_service.update_supplier(db, supplier_id, supplier)
        if not updated_supplier:
            raise HTTPException(status_code=404, detail="Supplier not found")
        return updated_supplier
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating supplier {supplier_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/suppliers/{supplier_id}/evaluate")
async def evaluate_supplier(
    supplier_id: int,
    evaluation_data: dict,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Evaluate supplier performance"""
    try:
        result = supplier_service.evaluate_supplier(db, supplier_id, evaluation_data)
        return {"message": "Supplier evaluation completed", "score": result["score"]}
    except Exception as e:
        logger.error(f"Error evaluating supplier {supplier_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Purchase Requisition endpoints
@app.post("/purchase-requisitions", response_model=PurchaseRequisition, status_code=status.HTTP_201_CREATED)
async def create_purchase_requisition(
    pr: PurchaseRequisitionCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new purchase requisition"""
    try:
        # Validate purchase requisition
        validation_result = validate_purchase_requisition(pr)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"])
        
        return procurement_service.create_purchase_requisition(db, pr)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating purchase requisition: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/purchase-requisitions", response_model=List[PurchaseRequisition])
async def get_purchase_requisitions(
    skip: int = 0,
    limit: int = 100,
    requester_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get purchase requisitions with optional filtering"""
    try:
        return procurement_service.get_purchase_requisitions(
            db, skip=skip, limit=limit, requester_id=requester_id,
            status=status, start_date=start_date, end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error retrieving purchase requisitions: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/purchase-requisitions/{pr_id}", response_model=PurchaseRequisition)
async def get_purchase_requisition(
    pr_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific purchase requisition by ID"""
    try:
        pr = procurement_service.get_purchase_requisition(db, pr_id)
        if not pr:
            raise HTTPException(status_code=404, detail="Purchase requisition not found")
        return pr
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving purchase requisition {pr_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/purchase-requisitions/{pr_id}/approve")
async def approve_purchase_requisition(
    pr_id: int,
    approver_id: int,
    comments: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Approve a purchase requisition"""
    try:
        result = procurement_service.approve_purchase_requisition(db, pr_id, approver_id, comments)
        return {"message": "Purchase requisition approved", "pr_id": pr_id}
    except Exception as e:
        logger.error(f"Error approving purchase requisition {pr_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/purchase-requisitions/{pr_id}/reject")
async def reject_purchase_requisition(
    pr_id: int,
    rejector_id: int,
    reason: str,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Reject a purchase requisition"""
    try:
        result = procurement_service.reject_purchase_requisition(db, pr_id, rejector_id, reason)
        return {"message": "Purchase requisition rejected", "pr_id": pr_id}
    except Exception as e:
        logger.error(f"Error rejecting purchase requisition {pr_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# RFQ (Request for Quotation) endpoints
@app.post("/rfqs", response_model=RFQ, status_code=status.HTTP_201_CREATED)
async def create_rfq(
    rfq: RFQCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new RFQ"""
    try:
        return rfq_service.create_rfq(db, rfq)
    except Exception as e:
        logger.error(f"Error creating RFQ: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/rfqs", response_model=List[RFQ])
async def get_rfqs(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get RFQs with optional filtering"""
    try:
        return rfq_service.get_rfqs(
            db, skip=skip, limit=limit, status=status,
            start_date=start_date, end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error retrieving RFQs: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/rfqs/{rfq_id}", response_model=RFQ)
async def get_rfq(
    rfq_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific RFQ by ID"""
    try:
        rfq = rfq_service.get_rfq(db, rfq_id)
        if not rfq:
            raise HTTPException(status_code=404, detail="RFQ not found")
        return rfq
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving RFQ {rfq_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rfqs/{rfq_id}/send")
async def send_rfq(
    rfq_id: int,
    supplier_ids: List[int],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Send RFQ to suppliers"""
    try:
        result = rfq_service.send_rfq_to_suppliers(db, rfq_id, supplier_ids)
        return {"message": "RFQ sent to suppliers", "rfq_id": rfq_id, "suppliers_count": len(supplier_ids)}
    except Exception as e:
        logger.error(f"Error sending RFQ {rfq_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/rfqs/{rfq_id}/close")
async def close_rfq(
    rfq_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Close an RFQ and evaluate responses"""
    try:
        result = rfq_service.close_rfq(db, rfq_id)
        return {"message": "RFQ closed and responses evaluated", "rfq_id": rfq_id}
    except Exception as e:
        logger.error(f"Error closing RFQ {rfq_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Contract Management endpoints
@app.post("/contracts", response_model=Contract, status_code=status.HTTP_201_CREATED)
async def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new contract"""
    try:
        return procurement_service.create_contract(db, contract)
    except Exception as e:
        logger.error(f"Error creating contract: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/contracts", response_model=List[Contract])
async def get_contracts(
    skip: int = 0,
    limit: int = 100,
    supplier_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get contracts with optional filtering"""
    try:
        return procurement_service.get_contracts(
            db, skip=skip, limit=limit, supplier_id=supplier_id,
            status=status, start_date=start_date, end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error retrieving contracts: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/contracts/{contract_id}", response_model=Contract)
async def get_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific contract by ID"""
    try:
        contract = procurement_service.get_contract(db, contract_id)
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        return contract
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving contract {contract_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Reporting endpoints
@app.get("/reports/supplier-performance")
async def get_supplier_performance_report(
    start_date: date,
    end_date: date,
    supplier_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get supplier performance report"""
    try:
        return procurement_service.generate_supplier_performance_report(db, start_date, end_date, supplier_id)
    except Exception as e:
        logger.error(f"Error generating supplier performance report: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reports/procurement-analytics")
async def get_procurement_analytics(
    start_date: date,
    end_date: date,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get procurement analytics report"""
    try:
        return procurement_service.generate_procurement_analytics(db, start_date, end_date, category)
    except Exception as e:
        logger.error(f"Error generating procurement analytics: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/reports/contract-compliance")
async def get_contract_compliance_report(
    as_of_date: date,
    supplier_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get contract compliance report"""
    try:
        return procurement_service.generate_contract_compliance_report(db, as_of_date, supplier_id)
    except Exception as e:
        logger.error(f"Error generating contract compliance report: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 