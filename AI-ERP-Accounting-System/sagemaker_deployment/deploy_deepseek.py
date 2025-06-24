#!/usr/bin/env python3
"""
SageMaker deployment script for DeepSeek model
This script handles the deployment of DeepSeek model to SageMaker
"""

import boto3
import sagemaker
from sagemaker.pytorch import PyTorchModel
from sagemaker import get_execution_role
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekSageMakerDeployment:
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize SageMaker deployment
        
        Args:
            region_name: AWS region for deployment
        """
        self.region_name = region_name
        self.sagemaker_session = sagemaker.Session(boto3.Session(region_name=region_name))
        self.role = get_execution_role()
        
    def create_model_artifact(self, model_name: str, model_path: str, output_path: str):
        """
        Create model artifact for SageMaker deployment
        
        Args:
            model_name: Name of the model
            model_path: Local path to the model files
            output_path: S3 path for the model artifact
        """
        try:
            logger.info(f"Creating model artifact for {model_name}")
            
            # Create a tar.gz file containing the model
            import tarfile
            import tempfile
            
            with tempfile.NamedTemporaryFile(suffix='.tar.gz', delete=False) as tmp_file:
                with tarfile.open(tmp_file.name, 'w:gz') as tar:
                    tar.add(model_path, arcname='.')
                
                # Upload to S3
                s3_client = boto3.client('s3', region_name=self.region_name)
                bucket_name = output_path.split('/')[2]
                key = '/'.join(output_path.split('/')[3:])
                
                s3_client.upload_file(tmp_file.name, bucket_name, key)
                
                # Clean up
                os.unlink(tmp_file.name)
                
            logger.info(f"Model artifact uploaded to {output_path}")
            
        except Exception as e:
            logger.error(f"Error creating model artifact: {e}")
            raise
    
    def deploy_model(self, 
                    model_name: str,
                    model_artifact_path: str,
                    instance_type: str = 'ml.g5.xlarge',
                    endpoint_name: Optional[str] = None) -> str:
        """
        Deploy DeepSeek model to SageMaker
        
        Args:
            model_name: Name of the model
            model_artifact_path: S3 path to the model artifact
            instance_type: SageMaker instance type
            endpoint_name: Name for the endpoint (optional)
            
        Returns:
            Endpoint name
        """
        try:
            logger.info(f"Deploying {model_name} to SageMaker")
            
            # Create PyTorch model
            pytorch_model = PyTorchModel(
                model_data=model_artifact_path,
                role=self.role,
                entry_point='deepseek_inference.py',
                source_dir='.',
                framework_version='2.0.0',
                py_version='py310',
                env={
                    'SAGEMAKER_CONTAINER_LOG_LEVEL': '20',
                    'SAGEMAKER_REGION': self.region_name
                }
            )
            
            # Deploy the model
            if endpoint_name is None:
                endpoint_name = f"{model_name}-endpoint"
            
            predictor = pytorch_model.deploy(
                initial_instance_count=1,
                instance_type=instance_type,
                endpoint_name=endpoint_name,
                wait=True
            )
            
            logger.info(f"Model deployed successfully to endpoint: {endpoint_name}")
            return endpoint_name
            
        except Exception as e:
            logger.error(f"Error deploying model: {e}")
            raise
    
    def test_endpoint(self, endpoint_name: str, test_prompt: str = "Hello, how are you?"):
        """
        Test the deployed endpoint
        
        Args:
            endpoint_name: Name of the endpoint to test
            test_prompt: Test prompt to send
        """
        try:
            logger.info(f"Testing endpoint: {endpoint_name}")
            
            # Create SageMaker runtime client
            runtime_client = boto3.client('sagemaker-runtime', region_name=self.region_name)
            
            # Prepare test payload
            import json
            payload = {
                "prompt": test_prompt,
                "max_tokens": 100,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            # Invoke endpoint
            response = runtime_client.invoke_endpoint(
                EndpointName=endpoint_name,
                ContentType='application/json',
                Body=json.dumps(payload)
            )
            
            # Parse response
            response_body = response['Body'].read().decode('utf-8')
            result = json.loads(response_body)
            
            logger.info(f"Test successful! Response: {result.get('generated_text', 'No response')}")
            return result
            
        except Exception as e:
            logger.error(f"Error testing endpoint: {e}")
            raise
    
    def delete_endpoint(self, endpoint_name: str):
        """
        Delete the SageMaker endpoint
        
        Args:
            endpoint_name: Name of the endpoint to delete
        """
        try:
            logger.info(f"Deleting endpoint: {endpoint_name}")
            
            # Delete endpoint
            sagemaker_client = boto3.client('sagemaker', region_name=self.region_name)
            sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
            
            # Delete endpoint configuration
            try:
                sagemaker_client.delete_endpoint_config(EndpointConfigName=endpoint_name)
            except:
                pass
            
            logger.info(f"Endpoint {endpoint_name} deleted successfully")
            
        except Exception as e:
            logger.error(f"Error deleting endpoint: {e}")
            raise

def main():
    """Main deployment function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Deploy DeepSeek model to SageMaker')
    parser.add_argument('--model-name', required=True, help='Name of the model')
    parser.add_argument('--model-path', required=True, help='Local path to model files')
    parser.add_argument('--s3-bucket', required=True, help='S3 bucket for model artifacts')
    parser.add_argument('--instance-type', default='ml.g5.xlarge', help='SageMaker instance type')
    parser.add_argument('--region', default='us-east-1', help='AWS region')
    parser.add_argument('--endpoint-name', help='Endpoint name (optional)')
    parser.add_argument('--test', action='store_true', help='Test the endpoint after deployment')
    parser.add_argument('--delete', action='store_true', help='Delete the endpoint after testing')
    
    args = parser.parse_args()
    
    # Initialize deployment
    deployment = DeepSeekSageMakerDeployment(region_name=args.region)
    
    try:
        # Create model artifact path
        model_artifact_path = f"s3://{args.s3_bucket}/models/{args.model_name}/model.tar.gz"
        
        # Create model artifact
        deployment.create_model_artifact(
            model_name=args.model_name,
            model_path=args.model_path,
            output_path=model_artifact_path
        )
        
        # Deploy model
        endpoint_name = deployment.deploy_model(
            model_name=args.model_name,
            model_artifact_path=model_artifact_path,
            instance_type=args.instance_type,
            endpoint_name=args.endpoint_name
        )
        
        # Test endpoint if requested
        if args.test:
            deployment.test_endpoint(endpoint_name)
        
        # Delete endpoint if requested
        if args.delete:
            deployment.delete_endpoint(endpoint_name)
        
        print(f"Deployment completed successfully!")
        print(f"Endpoint name: {endpoint_name}")
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        raise

if __name__ == "__main__":
    main() 