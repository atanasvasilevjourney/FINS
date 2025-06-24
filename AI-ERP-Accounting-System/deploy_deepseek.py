# --- DEPLOYMENT SECTION ---
# Only run this when you're ready to deploy (it will incur costs)

import sagemaker
import boto3
import json
from datetime import datetime
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri
from sagemaker.predictor import Predictor
from sagemaker.serializers import JSONSerializer
from sagemaker.deserializers import JSONDeserializer

# Configuration
target_aws_region = 'eu-central-1'
model_data_s3_path = "s3://finsitcom/deepseek-llm-7b-base/model.tar.gz"

# Setup SageMaker session
boto3_session = boto3.Session(region_name=target_aws_region)
sess = sagemaker.Session(boto_session=boto3_session)
role = sagemaker.get_execution_role()

# Model configuration
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

print(f"🚀 Starting deployment of {endpoint_name}...")
print("This will take 10-15 minutes...")

# Get container image
try:
    container_image_uri = get_huggingface_llm_image_uri(
        "huggingface",
        version="latest",
        region=target_aws_region
    )
except Exception as e:
    print(f"Latest failed, trying 3.2.3: {e}")
    container_image_uri = get_huggingface_llm_image_uri(
        "huggingface", 
        version="3.2.3",
        region=target_aws_region
    )

# Create and deploy model
print("Creating HuggingFaceModel object...")
huggingface_model = HuggingFaceModel(
    image_uri=container_image_uri,
    model_data=model_data_s3_path,
    env=hub,
    role=role,
    sagemaker_session=sess,
    name=f"{model_name}-model-{timestamp}"
)

predictor = huggingface_model.deploy(
    initial_instance_count=initial_instance_count,
    instance_type=instance_type,
    endpoint_name=endpoint_name,
    container_startup_health_check_timeout=600,
    wait=True
)

print(f"✅ Deployment complete: {endpoint_name}")

# Test the endpoint
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
print(f"🔗 Endpoint name: {endpoint_name}")
print(f"🌍 Region: {target_aws_region}") 