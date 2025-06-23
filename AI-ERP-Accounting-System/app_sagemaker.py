import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import os
from ai.agent import AIAgent

st.title("FINS - AI-Powered ERP (SageMaker DeepSeek)")

st.write("Welcome to the FINS Insights App powered by SageMaker DeepSeek.")

# Initialize AI Agent
@st.cache_resource
def init_ai_agent():
    """Initialize AI Agent with SageMaker integration"""
    region = st.secrets.get("AWS_REGION", "us-east-1")
    endpoint_name = st.secrets.get("SAGEMAKER_ENDPOINT_NAME", "")
    
    agent = AIAgent(region_name=region)
    if endpoint_name:
        agent.load_models(endpoint_name=endpoint_name)
    
    return agent

# Initialize AI Agent
ai_agent = init_ai_agent()

# Display AI Model Status
with st.sidebar:
    st.subheader("🤖 AI Model Status")
    status = ai_agent.get_model_status()
    
    if status["models_loaded"]:
        st.success("✅ DeepSeek Model Ready")
        st.info(f"Endpoint: {status['endpoint_name']}")
        st.info(f"Region: {status['region']}")
    else:
        st.error("❌ DeepSeek Model Not Available")
        st.info("Please configure SageMaker endpoint in secrets")

uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=['csv', 'xlsx'])

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.dataframe(df)

    # --- Data Visualization Section ---
    st.subheader("📊 Data Visualization")

    # Try to automatically identify date and amount columns
    date_column = st.selectbox("Select the date column for the timeline:", df.columns)
    amount_column = st.selectbox("Select the amount column for the timeline:", df.columns)

    if st.button("Generate Timeline Chart"):
        if date_column and amount_column:
            try:
                # Convert date column to datetime
                df[date_column] = pd.to_datetime(df[date_column])
                
                # Plot
                fig, ax = plt.subplots()
                ax.plot(df[date_column], df[amount_column])
                ax.set(xlabel=date_column, ylabel=amount_column,
                       title=f"{amount_column} over Time")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Error generating chart: {e}")
        else:
            st.warning("Please select both a date and an amount column.")

    st.subheader("🔍 Query with SQL")
    query = st.text_area("Enter your SQL query:", "SELECT * FROM df LIMIT 5;")
    if st.button("Run SQL Query"):
        if query:
            try:
                result_df = duckdb.query(query).to_df()
                st.write("Query Result:")
                st.dataframe(result_df)
            except Exception as e:
                st.error(f"Error executing query: {e}")

    st.subheader("🤖 Query with Natural Language (DeepSeek)")
    nl_query = st.text_input("Ask a question about your data:")
    if st.button("Run NL Query"):
        if nl_query:
            if ai_agent.get_model_status()["models_loaded"]:
                with st.spinner("Generating SQL query with DeepSeek..."):
                    sql_query = ai_agent.generate_sql_from_natural_language(
                        columns=list(df.columns),
                        question=nl_query
                    )
                
                if sql_query:
                    st.write("Generated SQL Query:")
                    st.code(sql_query, language="sql")
                    
                    try:
                        result_df = duckdb.query(sql_query).to_df()
                        st.write("Query Result:")
                        st.dataframe(result_df)
                    except Exception as e:
                        st.error(f"Error executing generated query: {e}")
                else:
                    st.error("Failed to generate SQL query from DeepSeek model")
            else:
                st.error("DeepSeek model is not available. Please check your SageMaker endpoint configuration.")
        else:
            st.warning("Please enter a question to analyze your data.")

    # --- Financial Analysis Section ---
    st.subheader("💰 Financial Analysis with DeepSeek")
    
    if ai_agent.get_model_status()["models_loaded"]:
        analysis_request = st.text_input("What financial analysis would you like to perform?")
        
        if st.button("Run Financial Analysis") and analysis_request:
            with st.spinner("Analyzing financial data with DeepSeek..."):
                # Create a summary of the data
                data_summary = f"""
                Dataset: {uploaded_file.name}
                Shape: {df.shape}
                Columns: {', '.join(df.columns)}
                Data Types: {dict(df.dtypes)}
                Sample Data: {df.head().to_dict()}
                """
                
                analysis_result = ai_agent.analyze_financial_data(
                    data_summary=data_summary,
                    analysis_request=analysis_request
                )
                
                if analysis_result:
                    st.write("### Analysis Results:")
                    st.write(analysis_result)
                else:
                    st.error("Failed to analyze financial data")
    else:
        st.info("DeepSeek model required for financial analysis")

# Configuration section
with st.expander("⚙️ Configuration"):
    st.write("### SageMaker Configuration")
    st.write("""
    To use this app with SageMaker DeepSeek:
    
    1. Deploy a DeepSeek model to SageMaker
    2. Configure the following in your Streamlit secrets:
       - `AWS_REGION`: Your AWS region (e.g., us-east-1)
       - `SAGEMAKER_ENDPOINT_NAME`: Your SageMaker endpoint name
    
    3. Ensure your AWS credentials are configured
    """)
    
    # Show current configuration
    st.write("**Current Configuration:**")
    st.write(f"- AWS Region: {st.secrets.get('AWS_REGION', 'Not configured')}")
    st.write(f"- Endpoint Name: {st.secrets.get('SAGEMAKER_ENDPOINT_NAME', 'Not configured')}") 