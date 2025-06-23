# SageMaker DeepSeek Setup Guide

This guide will help you deploy a DeepSeek model to Amazon SageMaker for use with your AI-powered ERP system.

## Prerequisites

1. **AWS Account** with SageMaker access
2. **AWS CLI** configured with appropriate permissions
3. **Python 3.8+** with required packages
4. **Docker** (for local testing)

## Step 1: Prepare DeepSeek Model

### Option A: Using Hugging Face Model

```python
# Create a model preparation script
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def prepare_deepseek_model():
    model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    
    # Save model and tokenizer
    model.save_pretrained("./deepseek-model")
    tokenizer.save_pretrained("./deepseek-model")
```

### Option B: Using SageMaker JumpStart

1. Go to SageMaker Console
2. Navigate to JumpStart
3. Search for "DeepSeek"
4. Deploy the model directly

## Step 2: Create SageMaker Endpoint

### Using AWS CLI

```bash
# Create model
aws sagemaker create-model \
    --model-name deepseek-erp-model \
    --primary-container Image=763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:2.0.0-transformers4.28.1-gpu-py310-cu118-ubuntu20.04 \
    --execution-role-arn arn:aws:iam::YOUR_ACCOUNT:role/SageMakerExecutionRole

# Create endpoint configuration
aws sagemaker create-endpoint-config \
    --endpoint-config-name deepseek-erp-config \
    --production-variants VariantName=default,ModelName=deepseek-erp-model,InitialInstanceCount=1,InstanceType=ml.g5.xlarge

# Create endpoint
aws sagemaker create-endpoint \
    --endpoint-name deepseek-erp-endpoint \
    --endpoint-config-name deepseek-erp-config
```

### Using Python SDK

```python
import sagemaker
from sagemaker.huggingface import HuggingFaceModel

def deploy_deepseek_model():
    # Initialize SageMaker session
    sagemaker_session = sagemaker.Session()
    
    # Define model
    huggingface_model = HuggingFaceModel(
        model_data='s3://your-bucket/deepseek-model.tar.gz',
        role='arn:aws:iam::YOUR_ACCOUNT:role/SageMakerExecutionRole',
        transformers_version='4.28.1',
        pytorch_version='2.0.0',
        py_version='py310',
        entry_point='inference.py',
        source_dir='./code'
    )
    
    # Deploy model
    predictor = huggingface_model.deploy(
        initial_instance_count=1,
        instance_type='ml.g5.xlarge',
        endpoint_name='deepseek-erp-endpoint'
    )
    
    return predictor
```

## Step 3: Create Inference Script

Create `inference.py` for the SageMaker endpoint:

```python
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

def model_fn(model_dir):
    """Load the model and tokenizer"""
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForCausalLM.from_pretrained(
        model_dir,
        torch_dtype=torch.float16,
        device_map="auto"
    )
    return model, tokenizer

def input_fn(request_body, request_content_type):
    """Parse input data"""
    if request_content_type == 'application/json':
        input_data = json.loads(request_body)
        return input_data
    else:
        raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model_tokenizer):
    """Generate prediction"""
    model, tokenizer = model_tokenizer
    
    prompt = input_data.get('prompt', '')
    max_tokens = input_data.get('max_tokens', 512)
    temperature = input_data.get('temperature', 0.7)
    top_p = input_data.get('top_p', 0.9)
    
    # Tokenize input
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode response
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return generated_text

def output_fn(prediction, content_type):
    """Format output"""
    if content_type == 'application/json':
        return json.dumps({'generated_text': prediction})
    else:
        raise ValueError(f"Unsupported content type: {content_type}")
```

## Step 4: Configure Streamlit Secrets

Create `.streamlit/secrets.toml`:

```toml
AWS_REGION = "us-east-1"
SAGEMAKER_ENDPOINT_NAME = "deepseek-erp-endpoint"
AWS_ACCESS_KEY_ID = "your-access-key"
AWS_SECRET_ACCESS_KEY = "your-secret-key"
```

## Step 5: Test the Integration

```python
# Test script
from ai.agent import AIAgent

# Initialize agent
agent = AIAgent(region_name='us-east-1')
agent.load_models(endpoint_name='deepseek-erp-endpoint')

# Test SQL generation
columns = ['date', 'amount', 'category', 'description']
question = "What is the total amount spent in January 2024?"

sql_query = agent.generate_sql_from_natural_language(columns, question)
print(f"Generated SQL: {sql_query}")
```

## Cost Optimization

1. **Use Spot Instances**: For non-production workloads
2. **Auto Scaling**: Configure based on traffic patterns
3. **Model Quantization**: Use INT8 quantization for faster inference
4. **Endpoint Scheduling**: Stop endpoints during off-hours

## Monitoring

1. **CloudWatch Metrics**: Monitor endpoint performance
2. **SageMaker Model Monitor**: Detect data drift
3. **Custom Logging**: Track inference requests and responses

## Security Considerations

1. **IAM Roles**: Use least privilege principle
2. **VPC Configuration**: Deploy in private subnets
3. **Encryption**: Enable encryption at rest and in transit
4. **Access Logging**: Monitor endpoint access

## Troubleshooting

### Common Issues

1. **Endpoint Creation Fails**
   - Check IAM permissions
   - Verify model artifacts are accessible
   - Ensure instance type is available

2. **Inference Errors**
   - Check input format
   - Verify model loading
   - Monitor memory usage

3. **Performance Issues**
   - Scale up instance type
   - Optimize model size
   - Use model caching

### Useful Commands

```bash
# Check endpoint status
aws sagemaker describe-endpoint --endpoint-name deepseek-erp-endpoint

# View endpoint logs
aws logs describe-log-groups --log-group-name-prefix /aws/sagemaker/Endpoints

# Delete endpoint (cleanup)
aws sagemaker delete-endpoint --endpoint-name deepseek-erp-endpoint
``` 