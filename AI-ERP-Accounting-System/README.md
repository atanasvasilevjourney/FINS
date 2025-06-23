# AI-Powered ERP Accounting System (FINS)

A comprehensive AI-powered Enterprise Resource Planning (ERP) system with advanced financial insights and data analysis capabilities.

## Features

### 🚀 Core ERP Functionality
- **Accounting Engine**: Core financial processing and management
- **AI Agent**: Intelligent data analysis and insights
- **Security**: AES encryption and compliance frameworks (GDPR, CCPA, SOC2)
- **Dashboard**: Modern UI for data visualization and management

### 📊 Data Analysis & Visualization
- **File Upload**: Support for CSV and XLSX files
- **Interactive Charts**: Timeline visualizations with matplotlib
- **SQL Queries**: Direct database querying with DuckDB
- **Natural Language Queries**: AI-powered data interrogation using OpenAI

### 🤖 AI-Powered Features
- **Natural Language Processing**: Ask questions about your data in plain English
- **Automated SQL Generation**: AI converts natural language to SQL queries
- **Intelligent Data Insights**: Advanced analytics and pattern recognition

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AI-ERP-Accounting-System
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

## Usage

### Running the Streamlit Application
```bash
streamlit run app.py
```

### Running the Django Backend
```bash
python main.py
```

## Project Structure

```
AI-ERP-Accounting-System/
├── app.py                 # Streamlit frontend application
├── main.py               # Django backend entry point
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── accounting/
│   └── core.py          # Accounting engine implementation
├── ai/
│   └── agent.py         # AI agent and model management
├── security/
│   └── encryption.py    # Security and encryption utilities
└── ui/
    └── dashboard.py     # Dashboard management system
```

## API Requirements

- **OpenAI API Key**: Required for natural language query processing
- **DuckDB**: Embedded database for data analysis
- **Streamlit**: Web application framework

## Security & Compliance

- **AES Encryption**: Secure data handling
- **GDPR Compliance**: European data protection standards
- **CCPA Compliance**: California consumer privacy
- **SOC2 Compliance**: Security and availability controls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For support and questions, please contact [your contact information]. 