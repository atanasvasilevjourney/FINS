import streamlit as st
import pandas as pd
import duckdb
import openai
import matplotlib.pyplot as plt

st.title("FINS - AI-Powered ERP")

st.write("Welcome to the FINS Insights App.")

api_key = st.text_input("Enter your OpenAI API key:", type="password")

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

    st.subheader("Query with Natural Language")
    nl_query = st.text_input("Ask a question about your data:")
    if st.button("Run NL Query"):
        if nl_query and api_key:
            openai.api_key = api_key
            
            # Create a prompt for the LLM
            prompt = f"""
            Given the following dataframe columns: {', '.join(df.columns)},
            write a DuckDB SQL query to answer the following question: "{nl_query}"
            
            The table is named "df".
            
            SQL Query:
            """
            
            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=prompt,
                    max_tokens=150,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
                
                sql_query = response.choices[0].text.strip()
                st.write("Generated SQL Query:")
                st.code(sql_query, language="sql")
                
                result_df = duckdb.query(sql_query).to_df()
                st.write("Query Result:")
                st.dataframe(result_df)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
        elif not api_key:
            st.warning("Please enter your OpenAI API key to use this feature.") 