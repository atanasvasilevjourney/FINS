import sagemaker
import boto3
import os
import json
from datetime import datetime
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri

# Simple validation functions
def validate_s3_path(s3_path, region):
    """Validate that the S3 model path exists and is accessible"""
    print(f"Checking S3 path: {s3_path}")
    try:
        s3_client = boto3.client('s3', region_name=region)
        bucket_name = s3_path.replace('s3://', '').split('/')[0]
        key = '/'.join(s3_path.replace('s3://', '').split('/')[1:])
        s3_client.head_object(Bucket=bucket_name, Key=key)
        print(f"✓ Model data verified at {s3_path}")
        return True
    except Exception as e:
        print(f"⚠️  Could not verify model data: {str(e)}")
        return False

print("Starting DeepSeek deployment script...")
print("="*50)

# --- 1. Configuration ---
target_aws_region = 'eu-central-1'
model_data_s3_path = "s3://finsitcom/deepseek-llm-7b-base/model.tar.gz"

print(f"Target region: {target_aws_region}")
print(f"Model S3 path: {model_data_s3_path}")

# Validate S3 path
validate_s3_path(model_data_s3_path, target_aws_region)

# --- 2. Setup SageMaker Session ---
print("\nSetting up SageMaker session...")
try:
    boto3_session = boto3.Session(region_name=target_aws_region)
    sess = sagemaker.Session(boto_session=boto3_session)
    aws_region = sess.boto_region_name
    
    # Try to get execution role
    try:
        role = sagemaker.get_execution_role()
        print(f"✓ Execution role: {role}")
    except:
        print("⚠️  Could not auto-detect role. Using manual method...")
        # Manual role detection
        iam = boto3.client('iam', region_name=target_aws_region)
        roles = iam.list_roles()['Roles']
        sagemaker_roles = [r for r in roles if 'SageMaker' in r['RoleName'] and 'ExecutionRole' in r['RoleName']]
        if sagemaker_roles:
            role = sagemaker_roles[0]['Arn']
            print(f"✓ Found role: {role}")
        else:
            raise Exception("No SageMaker execution role found")
    
    print(f"✓ Region: {aws_region}")
    print(f"✓ Session bucket: {sess.default_bucket()}")
    
except Exception as e:
    print(f"❌ Setup failed: {e}")
    raise

# --- 3. Model Configuration ---
hub = {
    'HF_MODEL_ID': 'deepseek-ai/deepseek-llm-7b-base',
    'SM_NUM_GPUS': json.dumps(1),
    'MAX_INPUT_LENGTH': '2048',
    'MAX_TOTAL_TOKENS': '4096',
    'TRUST_REMOTE_CODE': 'true'
}

instance_type = "ml.g5.2xlarge"
initial_instance_count = 1

# Create unique endpoint name
model_name = hub['HF_MODEL_ID'].split('/')[-1].replace('.', '-')
timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
endpoint_name = f"{model_name}-{timestamp}"

print(f"\n--- Model Configuration ---")
print(f"Model ID: {hub['HF_MODEL_ID']}")
print(f"Instance: {instance_type}")
print(f"Endpoint: {endpoint_name}")

# --- 4. Get Container Image ---
print(f"\nGetting container image...")
try:
    container_image_uri = get_huggingface_llm_image_uri(
        "huggingface",
        version="latest",
        region=target_aws_region
    )
    print(f"✓ Container: {container_image_uri}")
except Exception as e:
    print(f"⚠️  Latest failed, trying 3.2.3: {e}")
    container_image_uri = get_huggingface_llm_image_uri(
        "huggingface", 
        version="3.2.3",
        region=target_aws_region
    )
    print(f"✓ Container: {container_image_uri}")

print("\n🚀 Ready to deploy! Run next cell to start deployment.")
print("⚠️  Deployment will take 10-15 minutes and incur costs.")

# DEPLOYMENT CELL - Run this in a separate cell when ready to deploy
"""
# --- DEPLOYMENT SECTION ---
# Only run this when you're ready to deploy (it will incur costs)

print("Creating HuggingFaceModel object...")
huggingface_model = HuggingFaceModel(
    image_uri=container_image_uri,
    model_data=model_data_s3_path,
    env=hub,
    role=role,
    sagemaker_session=sess,
    name=f"{model_name}-model-{timestamp}"
)

print(f"🚀 Starting deployment of {endpoint_name}...")
print("This will take 10-15 minutes...")

predictor = huggingface_model.deploy(
    initial_instance_count=initial_instance_count,
    instance_type=instance_type,
    endpoint_name=endpoint_name,
    container_startup_health_check_timeout=600,
    wait=True
)

print(f"✅ Deployment complete: {endpoint_name}")

# Test the endpoint
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer

predictor = Predictor(
    endpoint_name=endpoint_name,
    sagemaker_session=sess,
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
print(f"Test response: {response}")

print(f"✅ Endpoint {endpoint_name} is ready for use!")
""" 