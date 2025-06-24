from fastapi import FastAPI, HTTPException, Depends, status, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime, date
import json
import httpx
import asyncio

from .database.connection import get_db
from .models.integrations import Integration, IntegrationCreate, IntegrationUpdate
from .models.entities import Entity, EntityCreate, EntityUpdate
from .models.api_keys import APIKey, APIKeyCreate, APIKeyUpdate
from .services.gateway_service import GatewayService
from .services.integration_service import IntegrationService
from .services.entity_service import EntityService
from .services.rate_limiting_service import RateLimitingService
from .utils.validators import validate_api_request
from .utils.helpers import format_response
from .middleware.auth_middleware import AuthMiddleware
from .middleware.rate_limit_middleware import RateLimitMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FINS ERP - API Gateway",
    description="API Gateway microservice for FINS ERP System",
    version="2.0.0"
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(AuthMiddleware)
app.add_middleware(RateLimitMiddleware)

# Security
security = HTTPBearer()

# Service instances
gateway_service = GatewayService()
integration_service = IntegrationService()
entity_service = EntityService()
rate_limiting_service = RateLimitingService()

# Service registry for routing
SERVICE_REGISTRY = {
    "general-ledger": "http://general-ledger:8000",
    "accounts-payable": "http://accounts-payable:8000",
    "accounts-receivable": "http://accounts-receivable:8000",
    "procurement": "http://procurement:8000",
    "inventory": "http://inventory:8000",
    "ai-ml-engine": "http://ai-ml-engine:8000",
    "workflow": "http://workflow:8000",
    "reporting": "http://reporting:8000"
}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "API Gateway",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": list(SERVICE_REGISTRY.keys())
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    # Check all service health
    service_health = {}
    async with httpx.AsyncClient() as client:
        for service_name, service_url in SERVICE_REGISTRY.items():
            try:
                response = await client.get(f"{service_url}/health", timeout=5.0)
                service_health[service_name] = "healthy" if response.status_code == 200 else "unhealthy"
            except Exception as e:
                service_health[service_name] = "unreachable"
                logger.error(f"Service {service_name} health check failed: {str(e)}")
    
    return {
        "service": "API Gateway",
        "status": "healthy",
        "database": "connected",
        "services": service_health,
        "timestamp": datetime.utcnow().isoformat()
    }

# Entity Management endpoints
@app.post("/entities", response_model=Entity, status_code=status.HTTP_201_CREATED)
async def create_entity(
    entity: EntityCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new entity (company, subsidiary, etc.)"""
    try:
        return entity_service.create_entity(db, entity)
    except Exception as e:
        logger.error(f"Error creating entity: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/entities", response_model=List[Entity])
async def get_entities(
    skip: int = 0,
    limit: int = 100,
    entity_type: Optional[str] = None,
    active: Optional[bool] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get entities with optional filtering"""
    try:
        return entity_service.get_entities(db, skip=skip, limit=limit, entity_type=entity_type, active=active)
    except Exception as e:
        logger.error(f"Error retrieving entities: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/entities/{entity_id}", response_model=Entity)
async def get_entity(
    entity_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific entity by ID"""
    try:
        entity = entity_service.get_entity(db, entity_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")
        return entity
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving entity {entity_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/entities/{entity_id}", response_model=Entity)
async def update_entity(
    entity_id: int,
    entity: EntityUpdate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Update an existing entity"""
    try:
        updated_entity = entity_service.update_entity(db, entity_id, entity)
        if not updated_entity:
            raise HTTPException(status_code=404, detail="Entity not found")
        return updated_entity
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating entity {entity_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Integration Management endpoints
@app.post("/integrations", response_model=Integration, status_code=status.HTTP_201_CREATED)
async def create_integration(
    integration: IntegrationCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new external integration"""
    try:
        return integration_service.create_integration(db, integration)
    except Exception as e:
        logger.error(f"Error creating integration: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/integrations", response_model=List[Integration])
async def get_integrations(
    skip: int = 0,
    limit: int = 100,
    integration_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get integrations with optional filtering"""
    try:
        return integration_service.get_integrations(db, skip=skip, limit=limit, integration_type=integration_type, status=status)
    except Exception as e:
        logger.error(f"Error retrieving integrations: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/integrations/{integration_id}", response_model=Integration)
async def get_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific integration by ID"""
    try:
        integration = integration_service.get_integration(db, integration_id)
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        return integration
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving integration {integration_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/integrations/{integration_id}/test")
async def test_integration(
    integration_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Test an external integration"""
    try:
        result = integration_service.test_integration(db, integration_id)
        return {"message": "Integration test completed", "status": result["status"], "details": result["details"]}
    except Exception as e:
        logger.error(f"Error testing integration {integration_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/integrations/{integration_id}/sync")
async def sync_integration(
    integration_id: int,
    sync_config: Dict[str, Any],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Sync data with external integration"""
    try:
        result = integration_service.sync_integration(db, integration_id, sync_config)
        return {"message": "Integration sync completed", "records_synced": result["records_synced"]}
    except Exception as e:
        logger.error(f"Error syncing integration {integration_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# API Key Management endpoints
@app.post("/api-keys", response_model=APIKey, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    api_key: APIKeyCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new API key"""
    try:
        return gateway_service.create_api_key(db, api_key)
    except Exception as e:
        logger.error(f"Error creating API key: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api-keys", response_model=List[APIKey])
async def get_api_keys(
    skip: int = 0,
    limit: int = 100,
    entity_id: Optional[int] = None,
    active: Optional[bool] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get API keys with optional filtering"""
    try:
        return gateway_service.get_api_keys(db, skip=skip, limit=limit, entity_id=entity_id, active=active)
    except Exception as e:
        logger.error(f"Error retrieving API keys: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api-keys/{key_id}")
async def revoke_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Revoke an API key"""
    try:
        result = gateway_service.revoke_api_key(db, key_id)
        return {"message": "API key revoked successfully", "key_id": key_id}
    except Exception as e:
        logger.error(f"Error revoking API key {key_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Multi-Entity Consolidation endpoints
@app.post("/consolidation/run")
async def run_consolidation(
    consolidation_config: Dict[str, Any],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Run multi-entity consolidation"""
    try:
        result = gateway_service.run_consolidation(db, consolidation_config)
        return {
            "message": "Consolidation completed",
            "entities_processed": result["entities_processed"],
            "consolidation_date": result["consolidation_date"],
            "status": result["status"]
        }
    except Exception as e:
        logger.error(f"Error running consolidation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/consolidation/reports")
async def get_consolidation_reports(
    start_date: date,
    end_date: date,
    entity_ids: Optional[List[int]] = None,
    report_type: str = "financial",
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get consolidated reports"""
    try:
        result = gateway_service.get_consolidation_reports(db, start_date, end_date, entity_ids, report_type)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "report_type": report_type,
            "consolidated_data": result["consolidated_data"],
            "eliminations": result["eliminations"]
        }
    except Exception as e:
        logger.error(f"Error getting consolidation reports: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Global Deployment endpoints
@app.post("/deployment/configure")
async def configure_global_deployment(
    deployment_config: Dict[str, Any],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Configure global deployment settings"""
    try:
        result = gateway_service.configure_global_deployment(db, deployment_config)
        return {"message": "Global deployment configured", "config_id": result["config_id"]}
    except Exception as e:
        logger.error(f"Error configuring global deployment: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/deployment/sync")
async def sync_global_deployment(
    sync_config: Dict[str, Any],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Sync data across global deployments"""
    try:
        result = gateway_service.sync_global_deployment(db, sync_config)
        return {
            "message": "Global deployment sync completed",
            "regions_synced": result["regions_synced"],
            "data_synced": result["data_synced"]
        }
    except Exception as e:
        logger.error(f"Error syncing global deployment: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Dynamic Routing
@app.api_route("/{service}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def route_request(
    service: str,
    path: str,
    request: Request,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Route requests to appropriate microservices"""
    try:
        # Validate service exists
        if service not in SERVICE_REGISTRY:
            raise HTTPException(status_code=404, detail=f"Service '{service}' not found")
        
        # Get request data
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.json()
            except:
                body = await request.body()
        
        # Get query parameters
        query_params = dict(request.query_params)
        
        # Get headers
        headers = dict(request.headers)
        # Remove host header to avoid conflicts
        headers.pop("host", None)
        
        # Build target URL
        target_url = f"{SERVICE_REGISTRY[service]}/{path}"
        
        # Validate API request
        validation_result = validate_api_request(service, path, request.method, body)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"])
        
        # Forward request to target service
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=target_url,
                params=query_params,
                json=body if isinstance(body, dict) else None,
                content=body if not isinstance(body, dict) else None,
                headers=headers,
                timeout=30.0
            )
        
        # Return response
        return JSONResponse(
            content=response.json() if response.headers.get("content-type") == "application/json" else response.text,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error routing request to {service}/{path}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "timestamp": datetime.utcnow().isoformat()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "timestamp": datetime.utcnow().isoformat()}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 