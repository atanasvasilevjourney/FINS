import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
from datetime import datetime

# Import ERP system components
from main_noai import main as initialize_erp_system

st.set_page_config(page_title="FINS ERP System", layout="wide")

# Initialize ERP system
@st.cache_resource
def get_erp_system():
    return initialize_erp_system()

erp_system = get_erp_system()

st.title("FINS - ERP System (No AI)")
st.write("Welcome to the FINS ERP App. AI features are currently disabled.")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Data Upload & Analysis", "Accounting", "Security", "Dashboard"]
)

if page == "Data Upload & Analysis":
    st.header("Data Upload & Analysis")
    
    uploaded_file = st.file_uploader("Choose a CSV or XLSX file", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.dataframe(df)

        # --- Data Visualization Section ---
        st.subheader("Data Visualization")

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

        st.subheader("Query with SQL")
        query = st.text_area("Enter your SQL query:", "SELECT * FROM df LIMIT 5;")
        if st.button("Run SQL Query"):
            if query:
                try:
                    result_df = duckdb.query(query).to_df()
                    st.write("Query Result:")
                    st.dataframe(result_df)
                except Exception as e:
                    st.error(f"Error executing query: {e}")

elif page == "Accounting":
    st.header("Accounting Module")
    
    # Add transaction form
    st.subheader("Add New Transaction")
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Transaction Date", datetime.now())
        description = st.text_input("Description")
    with col2:
        amount = st.number_input("Amount", value=0.0, step=0.01)
        account = st.selectbox("Account", ["Cash", "Bank", "Accounts Receivable", "Accounts Payable", "Expenses"])
        transaction_type = st.selectbox("Type", ["expense", "income", "transfer"])
    
    if st.button("Add Transaction"):
        if description and amount != 0:
            erp_system.accounting_engine.add_transaction(
                str(date), description, amount, account, transaction_type
            )
            st.success("Transaction added successfully!")
        else:
            st.error("Please fill in all required fields.")
    
    # Display accounting reports
    st.subheader("Financial Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Generate Balance Sheet"):
            balance_sheet = erp_system.accounting_engine.get_balance_sheet()
            if not balance_sheet.empty:
                st.dataframe(balance_sheet)
            else:
                st.info("No transactions to display.")
    
    with col2:
        if st.button("Generate Income Statement"):
            income_stmt = erp_system.accounting_engine.get_income_statement()
            if not income_stmt.empty:
                st.dataframe(income_stmt)
            else:
                st.info("No transactions to display.")

elif page == "Security":
    st.header("Security Module")
    
    st.subheader("Data Encryption")
    
    # Test encryption
    test_data = st.text_input("Enter text to encrypt:", "Hello World")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Encrypt Data"):
            encrypted = erp_system.encryption.encrypt_data(test_data)
            if encrypted:
                st.success("Data encrypted successfully!")
                st.code(encrypted)
            else:
                st.error("Encryption failed!")
    
    with col2:
        encrypted_input = st.text_input("Enter encrypted data to decrypt:")
        if st.button("Decrypt Data"):
            decrypted = erp_system.encryption.decrypt_data(encrypted_input)
            if decrypted:
                st.success("Data decrypted successfully!")
                st.code(decrypted)
            else:
                st.error("Decryption failed!")
    
    st.subheader("Password Hashing")
    password = st.text_input("Enter password to hash:", type="password")
    if st.button("Hash Password"):
        hashed = erp_system.encryption.hash_password(password)
        st.code(hashed)

elif page == "Dashboard":
    st.header("System Dashboard")
    
    # System status
    st.subheader("System Status")
    status = erp_system.get_system_status()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Accounting Engine", status['accounting_engine'])
    with col2:
        st.metric("Encryption", status['encryption'])
    with col3:
        st.metric("Dashboard", status['dashboard'])
    with col4:
        st.metric("AI Features", status['ai_features'])
    
    # Transaction summary
    st.subheader("Transaction Summary")
    transactions = erp_system.accounting_engine.transactions
    if transactions:
        df_transactions = pd.DataFrame(transactions)
        st.dataframe(df_transactions)
        
        # Summary chart
        if len(transactions) > 0:
            fig, ax = plt.subplots()
            df_transactions['amount'].hist(ax=ax, bins=10)
            ax.set_title("Transaction Amount Distribution")
            ax.set_xlabel("Amount")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
    else:
        st.info("No transactions recorded yet.")

st.sidebar.info("AI features (natural language query, DeepSeek analysis) are currently disabled. Contact your admin to enable AI integration.") 