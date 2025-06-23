import logging
from typing import Optional, Dict, Any
from .sagemaker_client import SageMakerDeepSeekClient

class AIAgent:
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize AI Agent with SageMaker DeepSeek integration
        
        Args:
            region_name: AWS region for SageMaker endpoint
        """
        self.logger = logging.getLogger(__name__)
        self.sagemaker_client = SageMakerDeepSeekClient(region_name=region_name)
        self.endpoint_name: Optional[str] = None
        self.models_loaded = False
        
    def load_models(self, endpoint_name: Optional[str] = None):
        """
        Load AI models and check endpoint availability
        
        Args:
            endpoint_name: SageMaker endpoint name for DeepSeek model
        """
        try:
            if endpoint_name:
                self.endpoint_name = endpoint_name
                
            if self.endpoint_name:
                # Check if endpoint is available
                if self.sagemaker_client.check_endpoint_status(self.endpoint_name):
                    self.models_loaded = True
                    self.logger.info(f"DeepSeek model loaded successfully from endpoint: {self.endpoint_name}")
                else:
                    self.logger.warning(f"DeepSeek endpoint {self.endpoint_name} is not available")
            else:
                self.logger.warning("No SageMaker endpoint specified")
                
        except Exception as e:
            self.logger.error(f"Error loading AI models: {e}")
            self.models_loaded = False
    
    def generate_sql_from_natural_language(self, columns: list, question: str) -> Optional[str]:
        """
        Generate SQL query from natural language using DeepSeek
        
        Args:
            columns: List of available columns in the dataset
            question: Natural language question
            
        Returns:
            Generated SQL query or None if error
        """
        if not self.models_loaded or not self.endpoint_name:
            self.logger.error("AI models not loaded or endpoint not available")
            return None
            
        return self.sagemaker_client.generate_sql_query(
            endpoint_name=self.endpoint_name,
            columns=columns,
            question=question
        )
    
    def analyze_financial_data(self, data_summary: str, analysis_request: str) -> Optional[str]:
        """
        Analyze financial data using DeepSeek
        
        Args:
            data_summary: Summary of the financial data
            analysis_request: What analysis to perform
            
        Returns:
            Analysis results or None if error
        """
        if not self.models_loaded or not self.endpoint_name:
            self.logger.error("AI models not loaded or endpoint not available")
            return None
            
        return self.sagemaker_client.analyze_financial_data(
            endpoint_name=self.endpoint_name,
            data_summary=data_summary,
            analysis_request=analysis_request
        )
    
    def get_model_status(self) -> Dict[str, Any]:
        """
        Get the status of loaded AI models
        
        Returns:
            Dictionary with model status information
        """
        return {
            "models_loaded": self.models_loaded,
            "endpoint_name": self.endpoint_name,
            "region": self.sagemaker_client.region_name
        } 