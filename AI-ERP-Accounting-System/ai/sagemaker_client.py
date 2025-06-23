import boto3
import json
import logging
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError

class SageMakerDeepSeekClient:
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize SageMaker client for DeepSeek model
        
        Args:
            region_name: AWS region where SageMaker endpoint is deployed
        """
        self.region_name = region_name
        self.sagemaker_runtime = boto3.client('sagemaker-runtime', region_name=region_name)
        self.logger = logging.getLogger(__name__)
        
    def invoke_model(self, 
                    endpoint_name: str, 
                    prompt: str, 
                    max_tokens: int = 512,
                    temperature: float = 0.7,
                    top_p: float = 0.9) -> Optional[str]:
        """
        Invoke DeepSeek model through SageMaker endpoint
        
        Args:
            endpoint_name: Name of the SageMaker endpoint
            prompt: Input prompt for the model
            max_tokens: Maximum number of tokens to generate
            temperature: Controls randomness (0.0 = deterministic, 1.0 = very random)
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated response text or None if error
        """
        try:
            # Prepare the payload for DeepSeek model
            payload = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stop": ["\n\n", "Human:", "Assistant:"]
            }
            
            # Convert to JSON string
            payload_json = json.dumps(payload)
            
            # Invoke the endpoint
            response = self.sagemaker_runtime.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType='application/json',
                Body=payload_json
            )
            
            # Parse the response
            response_body = response['Body'].read().decode('utf-8')
            response_data = json.loads(response_body)
            
            # Extract the generated text
            generated_text = response_data.get('generated_text', '')
            
            self.logger.info(f"Successfully generated response from DeepSeek model")
            return generated_text
            
        except ClientError as e:
            self.logger.error(f"AWS ClientError: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error invoking DeepSeek model: {e}")
            return None
    
    def generate_sql_query(self, 
                          endpoint_name: str, 
                          columns: list, 
                          question: str) -> Optional[str]:
        """
        Generate SQL query from natural language using DeepSeek
        
        Args:
            endpoint_name: SageMaker endpoint name
            columns: List of available columns
            question: Natural language question
            
        Returns:
            Generated SQL query or None if error
        """
        prompt = f"""
        Given the following dataframe columns: {', '.join(columns)},
        write a DuckDB SQL query to answer the following question: "{question}"
        
        The table is named "df".
        
        SQL Query:
        """
        
        response = self.invoke_model(
            endpoint_name=endpoint_name,
            prompt=prompt,
            max_tokens=200,
            temperature=0.3  # Lower temperature for more consistent SQL generation
        )
        
        if response:
            # Clean up the response to extract just the SQL query
            sql_query = response.strip()
            # Remove any markdown formatting if present
            if sql_query.startswith('```sql'):
                sql_query = sql_query[6:]
            if sql_query.endswith('```'):
                sql_query = sql_query[:-3]
            
            return sql_query.strip()
        
        return None
    
    def analyze_financial_data(self, 
                             endpoint_name: str, 
                             data_summary: str, 
                             analysis_request: str) -> Optional[str]:
        """
        Analyze financial data using DeepSeek
        
        Args:
            endpoint_name: SageMaker endpoint name
            data_summary: Summary of the financial data
            analysis_request: What analysis to perform
            
        Returns:
            Analysis results or None if error
        """
        prompt = f"""
        You are a financial analyst. Given the following financial data summary:
        {data_summary}
        
        Please provide insights on: {analysis_request}
        
        Provide a detailed analysis with actionable insights:
        """
        
        return self.invoke_model(
            endpoint_name=endpoint_name,
            prompt=prompt,
            max_tokens=500,
            temperature=0.5
        )
    
    def check_endpoint_status(self, endpoint_name: str) -> bool:
        """
        Check if SageMaker endpoint is available
        
        Args:
            endpoint_name: Name of the endpoint to check
            
        Returns:
            True if endpoint is available, False otherwise
        """
        try:
            sagemaker = boto3.client('sagemaker', region_name=self.region_name)
            response = sagemaker.describe_endpoint(EndpointName=endpoint_name)
            status = response['EndpointStatus']
            
            if status == 'InService':
                self.logger.info(f"Endpoint {endpoint_name} is available")
                return True
            else:
                self.logger.warning(f"Endpoint {endpoint_name} status: {status}")
                return False
                
        except ClientError as e:
            self.logger.error(f"Error checking endpoint status: {e}")
            return False 