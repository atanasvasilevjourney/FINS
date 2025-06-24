from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime, date
from decimal import Decimal
import json

from .database.connection import get_db
from .models.ml_models import MLModel, MLModelCreate, MLModelUpdate
from .models.predictions import Prediction, PredictionCreate, PredictionUpdate
from .models.training_jobs import TrainingJob, TrainingJobCreate, TrainingJobUpdate
from .services.ai_service import AIService
from .services.ml_service import MLService
from .services.prediction_service import PredictionService
from .services.forecasting_service import ForecastingService
from .utils.validators import validate_prediction_request
from .utils.helpers import format_prediction_result

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FINS ERP - AI/ML Engine",
    description="AI/ML Engine microservice for FINS ERP System",
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
ai_service = AIService()
ml_service = MLService()
prediction_service = PredictionService()
forecasting_service = ForecastingService()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "AI/ML Engine",
        "version": "2.0.0",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "service": "AI/ML Engine",
        "status": "healthy",
        "database": "connected",
        "ml_models": "available",
        "timestamp": datetime.utcnow().isoformat()
    }

# ML Model Management endpoints
@app.post("/models", response_model=MLModel, status_code=status.HTTP_201_CREATED)
async def create_ml_model(
    model: MLModelCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Create a new ML model"""
    try:
        return ml_service.create_model(db, model)
    except Exception as e:
        logger.error(f"Error creating ML model: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/models", response_model=List[MLModel])
async def get_ml_models(
    skip: int = 0,
    limit: int = 100,
    model_type: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get ML models with optional filtering"""
    try:
        return ml_service.get_models(db, skip=skip, limit=limit, model_type=model_type, status=status)
    except Exception as e:
        logger.error(f"Error retrieving ML models: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/models/{model_id}", response_model=MLModel)
async def get_ml_model(
    model_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific ML model by ID"""
    try:
        model = ml_service.get_model(db, model_id)
        if not model:
            raise HTTPException(status_code=404, detail="ML model not found")
        return model
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving ML model {model_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/models/{model_id}/train")
async def train_model(
    model_id: int,
    training_config: Dict[str, Any],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Train an ML model"""
    try:
        result = ml_service.train_model(db, model_id, training_config)
        return {"message": "Model training started", "job_id": result["job_id"]}
    except Exception as e:
        logger.error(f"Error training model {model_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/models/{model_id}/deploy")
async def deploy_model(
    model_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Deploy an ML model"""
    try:
        result = ml_service.deploy_model(db, model_id)
        return {"message": "Model deployed successfully", "model_id": model_id}
    except Exception as e:
        logger.error(f"Error deploying model {model_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Prediction endpoints
@app.post("/predict", response_model=Prediction)
async def make_prediction(
    prediction_request: PredictionCreate,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Make a prediction using deployed models"""
    try:
        # Validate prediction request
        validation_result = validate_prediction_request(prediction_request)
        if not validation_result["valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"])
        
        return prediction_service.make_prediction(db, prediction_request)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/predictions", response_model=List[Prediction])
async def get_predictions(
    skip: int = 0,
    limit: int = 100,
    model_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get predictions with optional filtering"""
    try:
        return prediction_service.get_predictions(
            db, skip=skip, limit=limit, model_id=model_id,
            start_date=start_date, end_date=end_date
        )
    except Exception as e:
        logger.error(f"Error retrieving predictions: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/predictions/{prediction_id}", response_model=Prediction)
async def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific prediction by ID"""
    try:
        prediction = prediction_service.get_prediction(db, prediction_id)
        if not prediction:
            raise HTTPException(status_code=404, detail="Prediction not found")
        return prediction
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving prediction {prediction_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Financial Forecasting endpoints
@app.post("/forecast/cash-flow")
async def forecast_cash_flow(
    forecast_periods: int,
    start_date: date,
    confidence_level: float = 0.95,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate cash flow forecast"""
    try:
        result = forecasting_service.forecast_cash_flow(db, forecast_periods, start_date, confidence_level)
        return {
            "forecast_type": "cash_flow",
            "periods": forecast_periods,
            "start_date": start_date,
            "confidence_level": confidence_level,
            "forecast_data": result["forecast_data"],
            "accuracy_metrics": result["accuracy_metrics"]
        }
    except Exception as e:
        logger.error(f"Error forecasting cash flow: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/forecast/revenue")
async def forecast_revenue(
    forecast_periods: int,
    start_date: date,
    product_category: Optional[str] = None,
    confidence_level: float = 0.95,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate revenue forecast"""
    try:
        result = forecasting_service.forecast_revenue(db, forecast_periods, start_date, product_category, confidence_level)
        return {
            "forecast_type": "revenue",
            "periods": forecast_periods,
            "start_date": start_date,
            "product_category": product_category,
            "confidence_level": confidence_level,
            "forecast_data": result["forecast_data"],
            "accuracy_metrics": result["accuracy_metrics"]
        }
    except Exception as e:
        logger.error(f"Error forecasting revenue: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/forecast/expenses")
async def forecast_expenses(
    forecast_periods: int,
    start_date: date,
    expense_category: Optional[str] = None,
    confidence_level: float = 0.95,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate expense forecast"""
    try:
        result = forecasting_service.forecast_expenses(db, forecast_periods, start_date, expense_category, confidence_level)
        return {
            "forecast_type": "expenses",
            "periods": forecast_periods,
            "start_date": start_date,
            "expense_category": expense_category,
            "confidence_level": confidence_level,
            "forecast_data": result["forecast_data"],
            "accuracy_metrics": result["accuracy_metrics"]
        }
    except Exception as e:
        logger.error(f"Error forecasting expenses: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Anomaly Detection endpoints
@app.post("/anomaly/detect")
async def detect_anomalies(
    data_source: str,
    start_date: date,
    end_date: date,
    threshold: float = 0.05,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Detect anomalies in financial data"""
    try:
        result = ai_service.detect_anomalies(db, data_source, start_date, end_date, threshold)
        return {
            "data_source": data_source,
            "start_date": start_date,
            "end_date": end_date,
            "threshold": threshold,
            "anomalies_detected": len(result["anomalies"]),
            "anomalies": result["anomalies"],
            "confidence_scores": result["confidence_scores"]
        }
    except Exception as e:
        logger.error(f"Error detecting anomalies: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Risk Assessment endpoints
@app.post("/risk/assess")
async def assess_risk(
    risk_type: str,
    parameters: Dict[str, Any],
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Assess financial risk"""
    try:
        result = ai_service.assess_risk(db, risk_type, parameters)
        return {
            "risk_type": risk_type,
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "risk_factors": result["risk_factors"],
            "recommendations": result["recommendations"]
        }
    except Exception as e:
        logger.error(f"Error assessing risk: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Natural Language Processing endpoints
@app.post("/nlp/analyze")
async def analyze_text(
    text: str,
    analysis_type: str,  # sentiment, entities, key_phrases, etc.
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Analyze text using NLP"""
    try:
        result = ai_service.analyze_text(text, analysis_type)
        return {
            "text": text,
            "analysis_type": analysis_type,
            "results": result
        }
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/nlp/extract-financial-data")
async def extract_financial_data(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Extract financial data from documents using NLP"""
    try:
        result = ai_service.extract_financial_data(file)
        return {
            "filename": file.filename,
            "extracted_data": result["extracted_data"],
            "confidence": result["confidence"],
            "entities": result["entities"]
        }
    except Exception as e:
        logger.error(f"Error extracting financial data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Model Performance endpoints
@app.get("/models/{model_id}/performance")
async def get_model_performance(
    model_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get model performance metrics"""
    try:
        result = ml_service.get_model_performance(db, model_id, start_date, end_date)
        return {
            "model_id": model_id,
            "accuracy": result["accuracy"],
            "precision": result["precision"],
            "recall": result["recall"],
            "f1_score": result["f1_score"],
            "confusion_matrix": result["confusion_matrix"],
            "performance_trend": result["performance_trend"]
        }
    except Exception as e:
        logger.error(f"Error getting model performance: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Training Job Management endpoints
@app.get("/training-jobs", response_model=List[TrainingJob])
async def get_training_jobs(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    model_id: Optional[int] = None,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get training jobs with optional filtering"""
    try:
        return ml_service.get_training_jobs(db, skip=skip, limit=limit, status=status, model_id=model_id)
    except Exception as e:
        logger.error(f"Error retrieving training jobs: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/training-jobs/{job_id}", response_model=TrainingJob)
async def get_training_job(
    job_id: int,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get a specific training job by ID"""
    try:
        job = ml_service.get_training_job(db, job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Training job not found")
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving training job {job_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 