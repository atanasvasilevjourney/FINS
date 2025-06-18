import streamlit as st
import requests
import pandas as pd
import json
import os
import io
import plotly.express as px
import plotly.graph_objects as go
import base64
from datetime import datetime
import time

# Configure the app
st.set_page_config(
    page_title="AI Financial Insights App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_URL = os.environ.get("API_URL", "http://localhost:8000")

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"
if "files" not in st.session_state:
    st.session_state.files = []
if "current_file" not in st.session_state:
    st.session_state.current_file = None
if "file_data" not in st.session_state:
    st.session_state.file_data = None
if "insights" not in st.session_state:
    st.session_state.insights = None

# Theme and styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
    }
    .card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f9f9f9;
        border: 1px solid #e0e0e0;
        margin-bottom: 1rem;
    }
    .insight-card {
        background-color: #e3f2fd;
        border-left: 4px solid #1E88E5;
    }
    .recommendation-card {
        background-color: #e8f5e9;
        border-left: 4px solid #43A047;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
        border-radius: 0.3rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
        border: none;
    }
    .stButton button:hover {
        background-color: #1565C0;
    }
    .warning {
        color: #FF5722;
        font-weight: bold;
    }
    .footer {
        text-align: center;
        color: #9e9e9e;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)


# Helper functions
def login_user(email, password):
    response = requests.post(
        f"{API_URL}/token",
        data={"username": email, "password": password}
    )
    if response.status_code == 200:
        token_data = response.json()
        st.session_state.authenticated = True
        st.session_state.token = token_data["access_token"]
        # Get user data
        user_response = requests.get(
            f"{API_URL}/users/me",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )
        if user_response.status_code == 200:
            st.session_state.user = user_response.json()
        return True
    return False

def register_user(email, password, first_name, last_name):
    response = requests.post(
        f"{API_URL}/register",
        json={
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }
    )
    if response.status_code == 201:
        return True
    return False

def get_files():
    response = requests.get(
        f"{API_URL}/files",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    if response.status_code == 200:
        st.session_state.files = response.json()
    else:
        st.session_state.files = []

def get_file_data(file_id):
    response = requests.get(
        f"{API_URL}/files/{file_id}",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    if response.status_code == 200:
        st.session_state.file_data = response.json()
        return True
    return False

def generate_insights(file_id):
    response = requests.post(
        f"{API_URL}/insight/{file_id}",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    if response.status_code == 200:
        st.session_state.insights = response.json()
        return True
    elif response.status_code == 403:
        st.error("Free tier limited to 5 insight generations per month. Please upgrade.")
        return False
    else:
        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
        return False

def create_checkout_session(plan):
    response = requests.post(
        f"{API_URL}/create-checkout-session/{plan}",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    if response.status_code == 200:
        return response.json().get("checkout_url")
    return None

def create_portal_session():
    response = requests.post(
        f"{API_URL}/create-portal-session",
        headers={"Authorization": f"Bearer {st.session_state.token}"}
    )
    if response.status_code == 200:
        return response.json().get("portal_url")
    return None

# Navigation functions
def go_to_dashboard():
    st.session_state.current_page = "dashboard"
    get_files()

def go_to_file_upload():
    st.session_state.current_page = "file_upload"

def go_to_file_view(file_id):
    st.session_state.current_page = "file_view"
    st.session_state.current_file = file_id
    get_file_data(file_id)

def go_to_insights(file_id):
    st.session_state.current_page = "insights"
    st.session_state.current_file = file_id
    get_file_data(file_id)
    generate_insights(file_id)

def go_to_subscription():
    st.session_state.current_page = "subscription"

def logout():
    st.session_state.authenticated = False
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.current_page = "login"
    st.session_state.files = []
    st.session_state.current_file = None
    st.session_state.file_data = None
    st.session_state.insights = None


# Page components
def render_sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/financial-growth.png", width=80)
        st.markdown("<h2 class='sub-header'>AI Financial Insights</h2>", unsafe_allow_html=True)
        
        if st.session_state.authenticated and st.session_state.user:
            st.markdown(f"**Welcome, {st.session_state.user.get('first_name', '')}**")
            st.markdown(f"Subscription: **{st.session_state.user.get('subscription_tier', 'free').capitalize()}**")
            
            st.divider()
            
            if st.button("📊 Dashboard", key="btn_dashboard"):
                go_to_dashboard()
            
            if st.button("📁 Upload File", key="btn_upload"):
                go_to_file_upload()
            
            if st.button("💳 Subscription", key="btn_subscription"):
                go_to_subscription()
            
            st.divider()
            
            if st.button("🚪 Logout", key="btn_logout"):
                logout()
        
        st.markdown("<div class='footer'>© 2023 AI Financial Insights</div>", unsafe_allow_html=True)

def render_login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-header'>AI Financial Insights</h1>", unsafe_allow_html=True)
        st.markdown("<p>Unlock the power of AI to analyze your financial data</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login")
                
                if submitted:
                    if email and password:
                        with st.spinner("Logging in..."):
                            if login_user(email, password):
                                st.success("Login successful!")
                                time.sleep(1)
                                go_to_dashboard()
                                st.experimental_rerun()
                            else:
                                st.error("Invalid email or password")
                    else:
                        st.warning("Please enter your email and password")
        
        with tab2:
            with st.form("register_form"):
                email = st.text_input("Email", key="reg_email")
                password = st.text_input("Password", type="password", key="reg_pwd")
                confirm_password = st.text_input("Confirm Password", type="password")
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                submitted = st.form_submit_button("Register")
                
                if submitted:
                    if email and password and confirm_password and first_name:
                        if password != confirm_password:
                            st.error("Passwords do not match")
                        else:
                            with st.spinner("Creating account..."):
                                if register_user(email, password, first_name, last_name):
                                    st.success("Account created successfully!")
                                    time.sleep(1)
                                    if login_user(email, password):
                                        go_to_dashboard()
                                        st.experimental_rerun()
                                else:
                                    st.error("Registration failed. Email may already be registered.")
                    else:
                        st.warning("Please fill all required fields")


def render_dashboard():
    st.markdown("<h1 class='main-header'>Financial Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p>View and analyze your financial data</p>", unsafe_allow_html=True)
    
    # Refresh files list
    get_files()
    
    if not st.session_state.files:
        st.info("You haven't uploaded any financial files yet. Start by uploading a CSV or Excel file.")
        if st.button("Upload your first file"):
            go_to_file_upload()
    else:
        # Display files in a grid
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Your Files")
        with col2:
            st.button("Upload New File", key="new_file", on_click=go_to_file_upload)
        
        st.divider()
        
        # Create a grid of cards for the files
        cols = st.columns(3)
        for i, file in enumerate(st.session_state.files):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
                    st.subheader(file.get("filename", "Unnamed File"))
                    st.caption(f"Uploaded on {file.get('upload_date', '').split('T')[0]}")
                    st.write(f"Type: {file.get('file_type', '').upper()}")
                    st.write(f"Columns: {len(file.get('columns', []))}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.button("View Data", key=f"view_{file.get('id')}", 
                                on_click=go_to_file_view, args=(file.get('id'),))
                    with col2:
                        st.button("AI Insights", key=f"insights_{file.get('id')}", 
                                on_click=go_to_insights, args=(file.get('id'),))
                    
                    st.markdown(f"</div>", unsafe_allow_html=True)

def render_file_upload():
    st.markdown("<h1 class='main-header'>Upload Financial Data</h1>", unsafe_allow_html=True)
    st.markdown("<p>Upload your financial CSV or Excel files for analysis</p>", unsafe_allow_html=True)
    
    # Show subscription limits
    if st.session_state.user.get('subscription_tier') == "free":
        st.warning("Free plan: Limited to 3 files and 5 AI insights per month")
    elif st.session_state.user.get('subscription_tier') == "pro":
        st.success("Pro plan: Up to 10 files and 50 AI insights per month")
    elif st.session_state.user.get('subscription_tier') == "business":
        st.success("Business plan: Unlimited files and AI insights")
    
    uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            # Preview the data
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:  # Excel file
                df = pd.read_excel(uploaded_file)
            
            st.subheader("Data Preview")
            st.write(df.head(5))
            
            st.write(f"Columns: {', '.join(df.columns)}")
            st.write(f"Rows: {len(df)}")
            
            # Upload button
            if st.button("Upload and Process"):
                with st.spinner("Uploading and processing your file..."):
                    # Reset the file pointer to the beginning
                    uploaded_file.seek(0)
                    
                    files = {"file": uploaded_file}
                    response = requests.post(
                        f"{API_URL}/upload",
                        headers={"Authorization": f"Bearer {st.session_state.token}"},
                        files=files
                    )
                    
                    if response.status_code == 200 or response.status_code == 201:
                        st.success("File uploaded successfully!")
                        time.sleep(1)
                        go_to_dashboard()
                        st.experimental_rerun()
                    else:
                        error_msg = "Unknown error"
                        try:
                            error_msg = response.json().get("detail", "Unknown error")
                        except:
                            pass
                        st.error(f"Error uploading file: {error_msg}")
                        
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    else:
        st.info("Please upload a CSV or Excel file containing your financial data")


def render_file_view():
    if not st.session_state.current_file or not st.session_state.file_data:
        st.error("File not found")
        go_to_dashboard()
        st.experimental_rerun()
        return
    
    # Get current file metadata
    current_file_info = None
    for file in st.session_state.files:
        if file.get('id') == st.session_state.current_file:
            current_file_info = file
            break
    
    if not current_file_info:
        st.error("File metadata not found")
        go_to_dashboard()
        st.experimental_rerun()
        return
    
    st.markdown(f"<h1 class='main-header'>{current_file_info.get('filename')}</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"Uploaded on {current_file_info.get('upload_date', '').split('T')[0]}")
    with col2:
        st.caption(f"Type: {current_file_info.get('file_type', '').upper()}")
    with col3:
        if st.button("Generate AI Insights"):
            go_to_insights(st.session_state.current_file)
            st.experimental_rerun()
    
    st.divider()
    
    # Load the data
    df = pd.DataFrame(st.session_state.file_data)
    
    # Data exploration tools
    st.subheader("Data Explorer")
    
    tab1, tab2, tab3 = st.tabs(["Table View", "Basic Statistics", "Quick Visualizations"])
    
    with tab1:
        st.dataframe(df, use_container_width=True)
    
    with tab2:
        st.write("Basic Statistics")
        st.write(df.describe())
        
        # Missing values
        st.write("Missing Values")
        missing_values = df.isna().sum().reset_index()
        missing_values.columns = ['Column', 'Missing Values']
        missing_values['Missing Percentage'] = (missing_values['Missing Values'] / len(df) * 100).round(2)
        st.dataframe(missing_values, use_container_width=True)
    
    with tab3:
        col1, col2 = st.columns(2)
        
        # Select columns for plotting
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        if numeric_columns:
            with col1:
                x_axis = st.selectbox("Select X-axis", df.columns.tolist())
            
            with col2:
                if x_axis in numeric_columns:
                    available_y = [col for col in numeric_columns if col != x_axis]
                    y_axis = st.selectbox("Select Y-axis", available_y) if available_y else None
                else:
                    available_y = numeric_columns
                    y_axis = st.selectbox("Select Y-axis", available_y) if available_y else None
            
            # Chart type
            chart_type = st.radio("Select Chart Type", ["Bar Chart", "Scatter Plot", "Line Chart", "Histogram"], horizontal=True)
            
            if y_axis:
                if chart_type == "Bar Chart":
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
                    st.plotly_chart(fig, use_container_width=True)
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, title=f"{y_axis} vs {x_axis}")
                    st.plotly_chart(fig, use_container_width=True)
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, title=f"{y_axis} over {x_axis}")
                    st.plotly_chart(fig, use_container_width=True)
                elif chart_type == "Histogram":
                    fig = px.histogram(df, x=x_axis, title=f"Distribution of {x_axis}")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Please select valid X and Y axis columns")
        else:
            st.info("No numeric columns found for visualization")


def render_insights_page():
    if not st.session_state.current_file or not st.session_state.file_data:
        st.error("File not found")
        go_to_dashboard()
        st.experimental_rerun()
        return
    
    # Get current file metadata
    current_file_info = None
    for file in st.session_state.files:
        if file.get('id') == st.session_state.current_file:
            current_file_info = file
            break
    
    if not current_file_info:
        st.error("File metadata not found")
        go_to_dashboard()
        st.experimental_rerun()
        return
    
    st.markdown(f"<h1 class='main-header'>AI Insights: {current_file_info.get('filename')}</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"Uploaded on {current_file_info.get('upload_date', '').split('T')[0]}")
    with col2:
        if st.button("Back to Data View"):
            go_to_file_view(st.session_state.current_file)
            st.experimental_rerun()
    
    st.divider()
    
    # Check if insights are available
    if not st.session_state.insights:
        st.info("Generating insights...")
        if generate_insights(st.session_state.current_file):
            st.experimental_rerun()
        return
    
    # Display insights
    st.subheader("AI Generated Insights")
    
    # Insights
    st.markdown("<h3>📈 Key Insights</h3>", unsafe_allow_html=True)
    for i, insight in enumerate(st.session_state.insights.get("insights", [])):
        st.markdown(f"<div class='card insight-card'>{insight}</div>", unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("<h3>💡 Recommendations</h3>", unsafe_allow_html=True)
    for i, recommendation in enumerate(st.session_state.insights.get("recommendations", [])):
        st.markdown(f"<div class='card recommendation-card'>{recommendation}</div>", unsafe_allow_html=True)
    
    # Data summary
    if st.session_state.file_data:
        st.divider()
        st.subheader("Data Summary")
        
        df = pd.DataFrame(st.session_state.file_data)
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        if not numeric_cols.empty:
            summary_stats = df[numeric_cols].describe().T
            fig = go.Figure()
            
            for col in numeric_cols[:5]:  # Limit to first 5 numeric columns
                fig.add_trace(go.Box(y=df[col].dropna(), name=col))
            
            fig.update_layout(title="Distribution of Key Numeric Fields", height=400)
            st.plotly_chart(fig, use_container_width=True)

def render_subscription_page():
    st.markdown("<h1 class='main-header'>Subscription Plans</h1>", unsafe_allow_html=True)
    st.markdown("<p>Upgrade your plan to unlock more features and AI-powered insights</p>", unsafe_allow_html=True)
    
    # Current subscription info
    current_plan = st.session_state.user.get('subscription_tier', 'free')
    st.write(f"Your current plan: **{current_plan.capitalize()}**")
    
    # Create columns for the pricing cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Free")
        st.markdown("$0 / month")
        st.markdown("#### Features:")
        st.markdown("- 3 data file uploads")
        st.markdown("- 5 AI analyses per month")
        st.markdown("- Basic visualizations")
        st.markdown("- Email support")
        
        if current_plan == "free":
            st.success("Current Plan")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Pro")
        st.markdown("$12.99 / month")
        st.markdown("#### Features:")
        st.markdown("- 10 data file uploads")
        st.markdown("- 50 AI analyses per month")
        st.markdown("- Advanced visualizations")
        st.markdown("- Priority email support")
        st.markdown("- Data export options")
        
        if current_plan == "pro":
            st.success("Current Plan")
        elif current_plan == "free":
            if st.button("Upgrade to Pro"):
                checkout_url = create_checkout_session("pro")
                if checkout_url:
                    st.success("Redirecting to checkout...")
                    st.markdown(f"[Click here if you are not redirected automatically]({checkout_url})")
                    # In a real app, you would use JavaScript to redirect automatically
                else:
                    st.error("Error creating checkout session")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Business")
        st.markdown("$29.99 / month")
        st.markdown("#### Features:")
        st.markdown("- Unlimited data file uploads")
        st.markdown("- Unlimited AI analyses")
        st.markdown("- Advanced visualizations")
        st.markdown("- Priority support")
        st.markdown("- Data export & API access")
        st.markdown("- Team collaboration")
        
        if current_plan == "business":
            st.success("Current Plan")
        elif current_plan in ["free", "pro"]:
            if st.button("Upgrade to Business"):
                checkout_url = create_checkout_session("business")
                if checkout_url:
                    st.success("Redirecting to checkout...")
                    st.markdown(f"[Click here if you are not redirected automatically]({checkout_url})")
                    # In a real app, you would use JavaScript to redirect automatically
                else:
                    st.error("Error creating checkout session")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Manage subscription
    if current_plan in ["pro", "business"]:
        st.divider()
        st.subheader("Manage Your Subscription")
        if st.button("Manage Billing"):
            portal_url = create_portal_session()
            if portal_url:
                st.success("Redirecting to customer portal...")
                st.markdown(f"[Click here if you are not redirected automatically]({portal_url})")
            else:
                st.error("Error creating customer portal session")


# Main app logic
def main():
    # Render sidebar
    render_sidebar()
    
    # Main content based on current page
    if not st.session_state.authenticated:
        render_login_page()
    elif st.session_state.current_page == "dashboard":
        render_dashboard()
    elif st.session_state.current_page == "file_upload":
        render_file_upload()
    elif st.session_state.current_page == "file_view":
        render_file_view()
    elif st.session_state.current_page == "insights":
        render_insights_page()
    elif st.session_state.current_page == "subscription":
        render_subscription_page()
    else:
        # Default to dashboard
        go_to_dashboard()
        st.experimental_rerun()

# Run the app
if __name__ == "__main__":
    main()
