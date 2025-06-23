import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Optional

class DashboardManager:
    def __init__(self):
        self.charts = {}
        self.data_sources = {}
        
    def create_chart(self, data: pd.DataFrame, chart_type: str = "line", 
                    x_column: Optional[str] = "", y_column: Optional[str] = "", title: str = ""):
        """Create a chart from data"""
        try:
            fig, ax = plt.subplots(figsize=(10, 6))
            if chart_type == "line":
                ax.plot(data[x_column], data[y_column])
            elif chart_type == "bar":
                ax.bar(data[x_column], data[y_column])
            elif chart_type == "scatter":
                ax.scatter(data[x_column], data[y_column])
                
            ax.set_title(title)
            ax.set_xlabel(x_column if x_column is not None else '')
            ax.set_ylabel(y_column if y_column is not None else '')
            plt.xticks(rotation=45)
            
            return fig
        except Exception as e:
            print(f"Chart creation failed: {e}")
            return None
            
    def display_summary_stats(self, data: pd.DataFrame) -> Dict:
        """Calculate and return summary statistics"""
        try:
            stats = {
                'total_rows': len(data),
                'total_columns': len(data.columns),
                'missing_values': data.isnull().sum().sum(),
                'numeric_columns': len(data.select_dtypes(include=['number']).columns)
            }
            return stats
        except Exception as e:
            print(f"Stats calculation failed: {e}")
            return {}
            
    def create_dashboard(self, data: pd.DataFrame):
        """Create a complete dashboard"""
        st.title("FINS ERP Dashboard")
        
        # Summary statistics
        stats = self.display_summary_stats(data)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Rows", stats.get('total_rows', 0))
        with col2:
            st.metric("Total Columns", stats.get('total_columns', 0))
        with col3:
            st.metric("Missing Values", stats.get('missing_values', 0))
        with col4:
            st.metric("Numeric Columns", stats.get('numeric_columns', 0))
            
        # Data preview
        st.subheader("Data Preview")
        st.dataframe(data.head())
        
        return True 