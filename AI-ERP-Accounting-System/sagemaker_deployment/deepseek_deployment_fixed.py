#!/usr/bin/env python3
"""
Enhanced DeepSeek SageMaker Deployment Script
Deploys DeepSeek model from S3 to SageMaker endpoint
"""

import sagemaker
import boto3
import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DeepSeekDeployment:
    def __init__(self, region: str = 'eu-central-1'):
        """
        Initialize DeepSeek deployment
        
        Args:
            region: AWS region for deployment
        """
        self.region = region
        self.sess = None
        self.role = None
        self.container_image_uri = None
        
    def setup_sagemaker_session(self) -> bool:
        """Setup SageMaker session and validate permissions"""
        try:
            logger.info(f"Setting up SageMaker session in {self.region}")
            
            # Create boto3 session
            boto3_session = boto3.Session(region_name=self.region)
            self.sess = sagemaker.Session(boto_session=boto3_session)
            
            # Get execution role
            try:
                self.role = sagemaker.get_execution_role()
                logger.info(f"✓ Execution role: {self.role}")
            except Exception as e:
                logger.warning(f"Could not auto-detect role: {e}")
                # Manual role detection
                iam = boto3.client('iam', region_name=self.region)
                roles = iam.list_roles()['Roles']
                sagemaker_roles = [r for r in roles if 'SageMaker' in r['RoleName'] and 'ExecutionRole' in r['RoleName']]
                if sagemaker_roles:
                    self.role = sagemaker_roles[0]['Arn']
                    logger.info(f"✓ Found role: {self.role}")
                else:
                    raise Exception("No SageMaker execution role found")
            
            logger.info(f"✓ Region: {self.sess.boto_region_name}")
            logger.info(f"✓ Session bucket: {self.sess.default_bucket()}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Setup failed: {e}")
            return False
    
    def validate_s3_path(self, s3_path: str) -> bool:
        """Validate that the S3 model path exists and is accessible"""
        logger.info(f"Validating S3 path: {s3_path}")
        try:
            s3_client = boto3.client('s3', region_name=self.region)
            bucket_name = s3_path.replace('s3://', '').split('/')[0]
            key = '/'.join(s3_path.replace('s3://', '').split('/')[1:])
            
            # Check if object exists
            s3_client.head_object(Bucket=bucket_name, Key=key)
            
            # Get object size
            response = s3_client.head_object(Bucket=bucket_name, Key=key)
            size_mb = response['ContentLength'] / (1024 * 1024)
            logger.info(f"✓ Model data verified at {s3_path} (Size: {size_mb:.1f} MB)")
            return True
            
        except Exception as e:
            logger.error(f"❌ Could not verify model data: {str(e)}")
            return False
    
    def get_container_image(self) -> bool:
        """Get the appropriate HuggingFace container image"""
        logger.info("Getting container image...")
        try:
            self.container_image_uri = get_huggingface_llm_image_uri(
                "huggingface",
                version="latest",
                region=self.region
            )
            logger.info(f"✓ Container: {self.container_image_uri}")
            return True
        except Exception as e:
            logger.warning(f"Latest version failed, trying 3.2.3: {e}")
            try:
                self.container_image_uri = get_huggingface_llm_image_uri(
                    "huggingface", 
                    version="3.2.3",
                    region=self.region
                )
                logger.info(f"✓ Container: {self.container_image_uri}")
                return True
            except Exception as e2:
                logger.error(f"❌ Failed to get container image: {e2}")
                return False
    
    def create_model_config(self, model_id: str = 'deepseek-ai/deepseek-llm-7b-base') -> Dict[str, Any]:
        """Create model configuration"""
        return {
            'HF_MODEL_ID': model_id,
            'SM_NUM_GPUS': json.dumps(1),
            'MAX_INPUT_LENGTH': '2048',
            'MAX_TOTAL_TOKENS': '4096',
            'TRUST_REMOTE_CODE': 'true'
        }
    
    def deploy_model(self, 
                    model_data_s3_path: str,
                    model_config: Dict[str, Any],
                    instance_type: str = "ml.g5.2xlarge",
                    endpoint_name: Optional[str] = None) -> Optional[str]:
        """
        Deploy the model to SageMaker
        
        Args:
            model_data_s3_path: S3 path to model.tar.gz
            model_config: Model configuration dictionary
            instance_type: SageMaker instance type
            endpoint_name: Optional endpoint name
            
        Returns:
            Endpoint name if successful, None otherwise
        """
        try:
            # Create unique endpoint name if not provided
            if endpoint_name is None:
                model_name = model_config['HF_MODEL_ID'].split('/')[-1].replace('.', '-')
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                endpoint_name = f"{model_name}-{timestamp}"
            
            logger.info(f"Creating HuggingFaceModel object...")
            huggingface_model = HuggingFaceModel(
                image_uri=self.container_image_uri,
                model_data=model_data_s3_path,
                env=model_config,
                role=self.role,
                sagemaker_session=self.sess,
                name=f"{model_name}-model-{timestamp}"
            )
            
            logger.info(f"🚀 Starting deployment of {endpoint_name}...")
            logger.info("This will take 10-15 minutes...")
            
            predictor = huggingface_model.deploy(
                initial_instance_count=1,
                instance_type=instance_type,
                endpoint_name=endpoint_name,
                container_startup_health_check_timeout=600,
                wait=True
            )
            
            logger.info(f"✅ Deployment complete: {endpoint_name}")
            return endpoint_name
            
        except Exception as e:
            logger.error(f"❌ Deployment failed: {e}")
            return None
    
    def test_endpoint(self, endpoint_name: str) -> bool:
        """Test the deployed endpoint"""
        try:
            logger.info(f"Testing endpoint: {endpoint_name}")
            
            predictor = Predictor(
                endpoint_name=endpoint_name,
                sagemaker_session=self.sess,
                serializer=JSONSerializer(),
                deserializer=JSONDeserializer()
            )
            
            test_payload = {
                "inputs": "The future of AI is",
                "parameters": {
                    "max_new_tokens": 50,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = predictor.predict(test_payload)
            logger.info(f"✅ Test successful! Response: {response}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            return False
    
    def cleanup_endpoint(self, endpoint_name: str) -> bool:
        """Clean up the endpoint"""
        try:
            logger.info(f"Cleaning up endpoint: {endpoint_name}")
            
            # Delete endpoint
            sagemaker_client = boto3.client('sagemaker', region_name=self.region)
            sagemaker_client.delete_endpoint(EndpointName=endpoint_name)
            
            # Delete endpoint configuration
            try:
                sagemaker_client.delete_endpoint_config(EndpointConfigName=endpoint_name)
            except:
                pass
            
            logger.info(f"✅ Endpoint {endpoint_name} cleaned up successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Cleanup failed: {e}")
            return False

def main():
    """Main deployment function"""
    # Configuration
    target_aws_region = 'eu-central-1'
    model_data_s3_path = "s3://finsitcom/deepseek-llm-7b-base/model.tar.gz"
    instance_type = "ml.g5.2xlarge"
    
    logger.info("Starting DeepSeek deployment script...")
    logger.info("="*50)
    
    # Initialize deployment
    deployment = DeepSeekDeployment(region=target_aws_region)
    
    # Setup SageMaker session
    if not deployment.setup_sagemaker_session():
        logger.error("Failed to setup SageMaker session")
        return False
    
    # Validate S3 path
    if not deployment.validate_s3_path(model_data_s3_path):
        logger.error("S3 validation failed")
        return False
    
    # Get container image
    if not deployment.get_container_image():
        logger.error("Failed to get container image")
        return False
    
    # Create model configuration
    model_config = deployment.create_model_config()
    
    logger.info(f"--- Model Configuration ---")
    logger.info(f"Model ID: {model_config['HF_MODEL_ID']}")
    logger.info(f"Instance: {instance_type}")
    logger.info(f"S3 Path: {model_data_s3_path}")
    
    # Deploy model
    endpoint_name = deployment.deploy_model(
        model_data_s3_path=model_data_s3_path,
        model_config=model_config,
        instance_type=instance_type
    )
    
    if endpoint_name is None:
        logger.error("Deployment failed")
        return False
    
    # Test endpoint
    if not deployment.test_endpoint(endpoint_name):
        logger.warning("Endpoint test failed")
    
    logger.info(f"✅ Deployment completed successfully!")
    logger.info(f"🔗 Endpoint name: {endpoint_name}")
    logger.info(f"🌍 Region: {target_aws_region}")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1) 