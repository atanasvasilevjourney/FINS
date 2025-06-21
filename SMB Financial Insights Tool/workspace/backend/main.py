import os
import json
import pandas as pd
import duckdb
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import plotly.express as px
import plotly.graph_objects as go
import openai
from dotenv import load_dotenv
from pathlib import Path
import logging
import stripe

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Set Stripe API key
if STRIPE_API_KEY:
    stripe.api_key = STRIPE_API_KEY

# Create data directory if it doesn't exist
data_dir = Path("./data")
data_dir.mkdir(exist_ok=True)
user_data_dir = data_dir / "users"
user_data_dir.mkdir(exist_ok=True)

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[str] = None

class SubscriptionTier(str):
    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"

class User(BaseModel):
    id: Optional[str] = None
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    subscription_tier: str = SubscriptionTier.FREE
    subscription_start: Optional[datetime] = None
    subscription_end: Optional[datetime] = None
    query_count: int = 0
    hashed_password: Optional[str] = None

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    subscription_tier: str
    subscription_start: Optional[datetime] = None
    subscription_end: Optional[datetime] = None
    query_count: int

class FileResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    upload_date: datetime
    columns: List[str]

class QueryRequest(BaseModel):
    query: str

class InsightResponse(BaseModel):
    insights: List[str]
    recommendations: List[str]


# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI app
app = FastAPI(title="AI Financial Insights API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(email: str):
    user_file = user_data_dir / f"{email}.json"
    if user_file.exists():
        with open(user_file, 'r') as f:
            user_data = json.load(f)
            # Ensure datetime strings are converted back to datetime objects if needed by Pydantic
            if "subscription_start" in user_data and user_data["subscription_start"]:
                user_data["subscription_start"] = datetime.fromisoformat(user_data["subscription_start"])
            if "subscription_end" in user_data and user_data["subscription_end"]:
                user_data["subscription_end"] = datetime.fromisoformat(user_data["subscription_end"])
            return User(**user_data)
    return None

def authenticate_user(email: str, password: str):
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=user_id)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Authentication routes
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    existing_user = get_user(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user_id = str(uuid.uuid4())
    user = User(
        id=user_id,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=get_password_hash(user_data.password),
        subscription_tier=SubscriptionTier.FREE,
        subscription_start=datetime.now(),
        subscription_end=datetime.now() + timedelta(days=365)  # Free tier for 1 year
    )
    
    user_file = user_data_dir / f"{user.email}.json"
    with open(user_file, 'w') as f:
        user_dict = user.dict()
        # Convert datetime objects to ISO format strings before JSON serialization
        if user_dict.get("subscription_start"):
            user_dict["subscription_start"] = user_dict["subscription_start"].isoformat()
        if user_dict.get("subscription_end"):
            user_dict["subscription_end"] = user_dict["subscription_end"].isoformat()
        
        json.dump(user_dict, f)
    
    # Create user data directory
    user_dir = user_data_dir / user_id
    user_dir.mkdir(exist_ok=True)
    
    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        subscription_tier=user.subscription_tier,
        subscription_start=user.subscription_start,
        subscription_end=user.subscription_end,
        query_count=user.query_count
    )


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        subscription_tier=current_user.subscription_tier,
        subscription_start=current_user.subscription_start,
        subscription_end=current_user.subscription_end,
        query_count=current_user.query_count
    )

# File upload and processing
@app.post("/upload", response_model=FileResponse)
async def upload_file(file: UploadFile = File(...), current_user: User = Depends(get_current_user)):
    # Check if user has reached file upload limit (for free tier)
    if current_user.subscription_tier == SubscriptionTier.FREE:
        user_dir = user_data_dir / current_user.id
        files = list(user_dir.glob('*.csv')) + list(user_dir.glob('*.xlsx'))
        if len(files) >= 3:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Free tier limited to 3 files. Please upgrade to upload more files."
            )
    
    # Validate file type
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ['.csv', '.xlsx']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV and Excel files are supported"
        )
    
    # Save the file
    file_id = str(uuid.uuid4())
    file_path = user_data_dir / current_user.id / f"{file_id}{file_extension}"

    
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Process the file
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        else:  # xlsx
            df = pd.read_excel(file_path)
        
        # Simple data cleaning
        # Remove duplicates
        df = df.drop_duplicates()
        # Convert column names to lowercase and replace spaces with underscores
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Save processed data
        processed_path = user_data_dir / current_user.id / f"{file_id}_processed{file_extension}"
        if file_extension == '.csv':
            df.to_csv(processed_path, index=False)
        else:  # xlsx
            df.to_excel(processed_path, index=False)
        
        # Save file metadata
        metadata = {
            "id": file_id,
            "filename": file.filename,
            "file_type": file_extension[1:],  # Remove the dot
            "upload_date": datetime.now().isoformat(),
            "columns": df.columns.tolist(),
            "row_count": len(df)
        }
        
        metadata_path = user_data_dir / current_user.id / f"{file_id}_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f)
        
        return FileResponse(
            id=file_id,
            filename=file.filename,
            file_type=file_extension[1:],
            upload_date=datetime.now(),
            columns=df.columns.tolist()
        )
    
    except Exception as e:
        if file_path.exists():
            os.remove(file_path)
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )


# Get files list
@app.get("/files", response_model=List[FileResponse])
async def get_files(current_user: User = Depends(get_current_user)):
    user_dir = user_data_dir / current_user.id
    if not user_dir.exists():
        return []
    
    files = []
    for metadata_file in user_dir.glob("*_metadata.json"):
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
            files.append(FileResponse(
                id=metadata["id"],
                filename=metadata["filename"],
                file_type=metadata["file_type"],
                upload_date=datetime.fromisoformat(metadata["upload_date"]),
                columns=metadata["columns"]
            ))
    
    return files

# Get a specific file's data
@app.get("/files/{file_id}")
async def get_file_data(file_id: str, current_user: User = Depends(get_current_user)):
    user_dir = user_data_dir / current_user.id
    metadata_path = user_dir / f"{file_id}_metadata.json"
    
    if not metadata_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    
    file_extension = f".{metadata['file_type']}"
    processed_path = user_dir / f"{file_id}_processed{file_extension}"
    
    if not processed_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Processed file not found"
        )
    
    if file_extension == '.csv':
        df = pd.read_csv(processed_path)
    else:  # xlsx
        df = pd.read_excel(processed_path)
    
    return df.head(100).to_dict(orient="records")


# Generate dashboard insights
@app.post("/insight/{file_id}", response_model=InsightResponse)
async def generate_insights(file_id: str, current_user: User = Depends(get_current_user)):
    # Check subscription and query limits
    if current_user.subscription_tier == SubscriptionTier.FREE:
        if current_user.query_count >= 5:  # Free tier limited to 5 queries per month
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Free tier limited to 5 insight generations per month. Please upgrade."
            )
    
    # Load file data
    user_dir = user_data_dir / current_user.id
    metadata_path = user_dir / f"{file_id}_metadata.json"
    
    if not metadata_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    with open(metadata_path, "r") as f:
        metadata = json.load(f)
    
    file_extension = f".{metadata['file_type']}"
    processed_path = user_dir / f"{file_id}_processed{file_extension}"
    
    if file_extension == '.csv':
        df = pd.read_csv(processed_path)
    else:  # xlsx
        df = pd.read_excel(processed_path)
    
    # Create DuckDB connection for data analysis
    conn = duckdb.connect(":memory:")
    conn.execute("CREATE TABLE financial_data AS SELECT * FROM df")
    
    # Get table information
    table_info = conn.execute("DESCRIBE financial_data").fetchall()
    columns_info = [f"{col[0]} ({col[1]})" for col in table_info]
    
    # Run basic analysis based on column names
    numeric_columns = [col[0] for col in table_info if col[1] in ['INTEGER', 'DECIMAL', 'FLOAT', 'DOUBLE']]
    date_columns = [col[0] for col in table_info if col[1] in ['DATE', 'TIMESTAMP']]
    
    analysis_results = []
    
    # Basic stats for numeric columns
    for col in numeric_columns:
        try:
            stats = conn.execute(f"""SELECT 
                MIN({col}) as minimum, 
                MAX({col}) as maximum, 
                AVG({col}) as average, 
                STDDEV({col}) as std_dev 
                FROM financial_data""").fetchone()
            
            analysis_results.append(f"Column {col} - Min: {stats[0]}, Max: {stats[1]}, Avg: {round(stats[2], 2)}, StdDev: {round(stats[3], 2)}")
        except Exception as e:
            analysis_results.append(f"Skipped analysis on {col}: {str(e)}")
    
    # Generate AI insights using OpenAI
    try:
        # Prepare data sample for the AI
        data_sample = df.head(10).to_dict(orient="records")
        column_types = {col[0]: col[1] for col in table_info}
        
        # Create a prompt for the AI
        prompt = f"""You are a financial data analyst. 
        Analyze the following financial data sample:
        
        Table columns: {columns_info}
        
        Data sample: {data_sample}
        
        Basic statistics: {analysis_results}
        
        Please provide:
        1. 3-5 key insights about this financial data
        2. 3 actionable recommendations based on these insights
        
        Format your response as JSON with two arrays: 'insights' and 'recommendations'."""
        
        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial analyst AI assistant that analyzes financial data and provides insights and recommendations in JSON format."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        ai_response = json.loads(response.choices[0].message.content)
        
        # Update user query count
        current_user.query_count += 1
        user_file = user_data_dir / f"{current_user.email}.json"
        with open(user_file, 'w') as f:
            user_dict = current_user.dict()
            # Convert datetime objects to ISO format strings before JSON serialization
            if user_dict.get("subscription_start"):
                user_dict["subscription_start"] = user_dict["subscription_start"].isoformat()
            if user_dict.get("subscription_end"):
                user_dict["subscription_end"] = user_dict["subscription_end"].isoformat()
            json.dump(user_dict, f)
        
        return InsightResponse(
            insights=ai_response.get("insights", ["No insights generated"]),
            recommendations=ai_response.get("recommendations", ["No recommendations generated"])
        )
        
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating insights: {str(e)}"
        )


# Stripe subscription management
@app.post("/create-checkout-session/{plan}")
async def create_checkout_session(plan: str, current_user: User = Depends(get_current_user)):
    if not STRIPE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Stripe integration not configured"
        )
    
    if plan not in ["pro", "business"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan. Choose 'pro' or 'business'"
        )
    
    # Set price based on plan
    price_id = os.getenv(f"STRIPE_{plan.upper()}_PRICE_ID")
    if not price_id:
        # Fallback to default price IDs if environment variables are not set
        price_ids = {
            "pro": "price_1234pro",  # Replace with your actual Stripe price IDs
            "business": "price_1234business"
        }
        price_id = price_ids[plan]
    
    try:
        # Create Checkout Session
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            client_reference_id=current_user.id,
            payment_method_types=["card"],
            line_items=[
                {
                    "price": price_id,
                    "quantity": 1,
                },
            ],
            mode="subscription",
            success_url=os.getenv("FRONTEND_URL", "http://localhost:8501") + "/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=os.getenv("FRONTEND_URL", "http://localhost:8501") + "/cancel",
            metadata={
                "user_id": current_user.id,
                "plan": plan
            }
        )
        return {"checkout_url": checkout_session.url}
    
    except Exception as e:
        logger.error(f"Error creating checkout session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating checkout session: {str(e)}"
        )

# Stripe webhook handler
@app.post("/webhook", status_code=status.HTTP_200_OK)
async def stripe_webhook(request: Dict[str, Any] = Body(...)):
    if not STRIPE_API_KEY or not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Stripe integration not configured"
        )
    
    try:
        event = stripe.Webhook.construct_event(
            json.dumps(request),
            os.getenv("STRIPE_SIGNATURE"),
            STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook error: {str(e)}"
        )
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('metadata', {}).get('user_id')
        plan = session.get('metadata', {}).get('plan')
        
        if user_id and plan:
            # Find user by ID
            user_found = False
            for user_file in user_data_dir.glob("*.json"):
                with open(user_file, 'r') as f:
                    user_data = json.load(f)
                    if user_data.get('id') == user_id:
                        user = User(**user_data)
                        user_found = True
                        break
            
            if user_found:
                # Update subscription
                user.subscription_tier = plan
                user.subscription_start = datetime.now()
                if plan == "pro":
                    user.subscription_end = datetime.now() + timedelta(days=30)  # 1 month
                else:  # business
                    user.subscription_end = datetime.now() + timedelta(days=365)  # 1 year
                
                # Save updated user data
                user_file = user_data_dir / f"{user.email}.json"
                with open(user_file, 'w') as f:
                    user_dict = user.dict()
                    # Convert datetime objects to ISO format strings before JSON serialization
                    if user_dict.get("subscription_start"):
                        user_dict["subscription_start"] = user_dict["subscription_start"].isoformat()
                    if user_dict.get("subscription_end"):
                        user_dict["subscription_end"] = user_dict["subscription_end"].isoformat()
                    json.dump(user_dict, f)
                
                logger.info(f"User {user_id} subscription updated to {plan}")
            else:
                logger.error(f"User {user_id} not found")
    
    return {"status": "success"}

# Customer portal session
@app.post("/create-portal-session")
async def customer_portal_session(current_user: User = Depends(get_current_user)):
    if not STRIPE_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Stripe integration not configured"
        )
    
    # Get Stripe customer ID
    # In a real app, you'd store this with the user, but here we'll just search
    customers = stripe.Customer.list(email=current_user.email, limit=1)
    if not customers.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No Stripe customer found"
        )
    
    customer_id = customers.data[0].id
    
    try:
        # Create portal session
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=os.getenv("FRONTEND_URL", "http://localhost:8501"),
        )
        return {"portal_url": session.url}
    except Exception as e:
        logger.error(f"Error creating portal session: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating portal session: {str(e)}"
        )

# API root and health check endpoints
@app.get("/")
async def read_root():
    return {"status": "ok", "message": "AI Financial Insights API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
