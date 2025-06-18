# AI Financial Insights App

A full-stack web application for analyzing financial data with AI-powered insights, visualizations, and subscription-based features.

## Features

- **User Authentication**: Secure login and registration system
- **Data Upload**: Upload and process CSV and Excel financial files
- **Data Visualization**: Interactive charts and data exploration tools
- **AI Insights**: Get AI-powered insights and recommendations from your financial data
- **Subscription Management**: Tiered subscription plans with Stripe integration

## Project Structure

```
.
├── backend/            # FastAPI backend code
│   ├── main.py        # Main backend application
│   └── requirements.txt # Backend dependencies
├── frontend/           # Streamlit frontend code
│   └── app.py         # Main frontend application
├── requirements.txt    # Combined dependencies
└── README.md          # This file
```

## Deployment Instructions

### Prerequisites

- Python 3.8 or higher
- Stripe account (for subscription features)
- OpenAI API key (for AI insights)

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
# API Configuration
SECRET_KEY=your_secret_key_for_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Paths Configuration
DATA_DIR=./data
USER_DATA_DIR=./data/users
UPLOADS_DIR=./data/uploads

# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key

# Stripe Configuration
STRIPE_API_KEY=your_stripe_api_key
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
STRIPE_PRO_PRICE_ID=your_stripe_pro_price_id
STRIPE_BUSINESS_PRICE_ID=your_stripe_business_price_id

# Frontend URL (for redirects)
FRONTEND_URL=http://localhost:8501
```

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai-financial-insights-app.git
   cd ai-financial-insights-app
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create necessary directories:
   ```
   mkdir -p data/users data/uploads
   ```

### Running the Application

#### Development Mode

1. Start the backend server:
   ```
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. In a new terminal, start the frontend:
   ```
   cd frontend
   streamlit run app.py
   ```

3. Access the application at http://localhost:8501

#### Production Deployment

##### Backend Deployment (with Docker)

1. Create a Dockerfile in the backend directory:
   ```
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. Build and run the Docker container:
   ```
   docker build -t financial-insights-backend .
   docker run -d -p 8000:8000 --env-file ../.env --name financial-insights-backend financial-insights-backend
   ```

##### Frontend Deployment

1. For Streamlit, you can use Streamlit Cloud or deploy with Docker:
   ```
   FROM python:3.9-slim

   WORKDIR /app

   COPY ../requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. Build and run the frontend container:
   ```
   docker build -t financial-insights-frontend .
   docker run -d -p 8501:8501 --env-file ../.env --name financial-insights-frontend financial-insights-frontend
   ```

### Setting Up Stripe Webhooks

1. Install the Stripe CLI: https://stripe.com/docs/stripe-cli
2. Login to your Stripe account:
   ```
   stripe login
   ```
3. Forward webhook events to your local endpoint:
   ```
   stripe listen --forward-to localhost:8000/webhook
   ```
4. Use the webhook signing secret provided by the CLI in your `.env` file.

## Usage

1. Register a new account or log in
2. Upload financial data (CSV or Excel)
3. Explore your data with visualizations
4. Generate AI-powered insights
5. Upgrade subscription for more features

## License

MIT
