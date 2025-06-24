# DeepSeek SageMaker Deployment

This directory contains all the necessary files to deploy DeepSeek models to AWS SageMaker for use with the FINS ERP system.

## 📁 Files Overview

- `deepseek_inference.py` - SageMaker inference script for DeepSeek model
- `deploy_deepseek.py` - Deployment script to create and manage SageMaker endpoints
- `requirements.txt` - Dependencies for the inference container
- `deployment_requirements.txt` - Dependencies for the deployment script
- `README.md` - This documentation

## 🚀 Quick Start

### Prerequisites

1. **AWS Account** with SageMaker access
2. **AWS CLI** configured with appropriate credentials
3. **Python 3.10+** with required packages
4. **DeepSeek model files** (downloaded from Hugging Face)

### Installation

1. **Install deployment dependencies:**
   ```bash
   pip install -r deployment_requirements.txt
   ```

2. **Install inference dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Deployment Steps

1. **Download DeepSeek Model:**
   ```bash
   # Create a directory for the model
   mkdir deepseek-model
   cd deepseek-model
   
   # Download from Hugging Face (example for DeepSeek-Coder-6.7B-Instruct)
   git lfs install
   git clone https://huggingface.co/deepseek-ai/deepseek-coder-6.7b-instruct .
   ```

2. **Deploy to SageMaker:**
   ```bash
   python deploy_deepseek.py \
     --model-name deepseek-coder-6.7b-instruct \
     --model-path ./deepseek-model \
     --s3-bucket your-s3-bucket-name \
     --instance-type ml.g5.xlarge \
     --region us-east-1 \
     --test
   ```

3. **Configure Streamlit App:**
   Add the endpoint name to your Streamlit secrets:
   ```toml
   # .streamlit/secrets.toml
   AWS_REGION = "us-east-1"
   SAGEMAKER_ENDPOINT_NAME = "deepseek-coder-6.7b-instruct-endpoint"
   ```

## 🔧 Configuration

### Instance Types

Recommended instance types for DeepSeek models:

| Model Size | Instance Type | Memory | GPU |
|------------|---------------|---------|-----|
| 6.7B | ml.g5.xlarge | 24GB | 1x A10G |
| 33B | ml.g5.2xlarge | 48GB | 1x A10G |
| 67B | ml.g5.4xlarge | 96GB | 1x A10G |

### Environment Variables

The inference script supports these environment variables:

- `SAGEMAKER_CONTAINER_LOG_LEVEL`: Logging level (default: 20)
- `SAGEMAKER_REGION`: AWS region (default: us-east-1)

## 📊 Usage Examples

### Testing the Endpoint

```python
import boto3
import json

# Create SageMaker runtime client
runtime_client = boto3.client('sagemaker-runtime', region_name='us-east-1')

# Prepare payload
payload = {
    "prompt": "Write a Python function to calculate fibonacci numbers",
    "max_tokens": 200,
    "temperature": 0.7,
    "top_p": 0.9
}

# Invoke endpoint
response = runtime_client.invoke_endpoint(
    EndpointName='deepseek-coder-6.7b-instruct-endpoint',
    ContentType='application/json',
    Body=json.dumps(payload)
)

# Parse response
result = json.loads(response['Body'].read().decode('utf-8'))
print(result['generated_text'])
```

### Integration with FINS ERP

The deployed endpoint can be used with the FINS ERP system through the `SageMakerDeepSeekClient` class:

```python
from ai.sagemaker_client import SageMakerDeepSeekClient

# Initialize client
client = SageMakerDeepSeekClient(region_name='us-east-1')

# Generate SQL from natural language
sql_query = client.generate_sql_query(
    endpoint_name='deepseek-coder-6.7b-instruct-endpoint',
    columns=['date', 'amount', 'category', 'description'],
    question="Show me the total expenses by category for last month"
)

print(sql_query)
```

## 🛠️ Management

### List Endpoints

```bash
aws sagemaker list-endpoints --region us-east-1
```

### Check Endpoint Status

```bash
aws sagemaker describe-endpoint --endpoint-name deepseek-coder-6.7b-instruct-endpoint --region us-east-1
```

### Delete Endpoint

```bash
python deploy_deepseek.py --delete --endpoint-name deepseek-coder-6.7b-instruct-endpoint
```

## 💰 Cost Optimization

### Auto Scaling

Configure auto scaling to reduce costs:

```bash
aws sagemaker put-scaling-policy \
  --endpoint-name deepseek-coder-6.7b-instruct-endpoint \
  --scaling-policy-name scale-down \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{
    "TargetValue": 0.5,
    "ScaleInCooldown": 300,
    "ScaleOutCooldown": 300,
    "PredefinedMetricSpecification": {
      "PredefinedMetricType": "SageMakerVariantInvocationsPerInstance"
    }
  }'
```

### Spot Instances

For cost savings, consider using spot instances during development:

```bash
python deploy_deepseek.py \
  --model-name deepseek-coder-6.7b-instruct \
  --model-path ./deepseek-model \
  --s3-bucket your-s3-bucket-name \
  --instance-type ml.g5.xlarge \
  --use-spot-instances
```

## 🔒 Security

### IAM Permissions

Ensure your SageMaker execution role has these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "sagemaker:CreateEndpoint",
        "sagemaker:CreateEndpointConfig",
        "sagemaker:CreateModel",
        "sagemaker:DeleteEndpoint",
        "sagemaker:DeleteEndpointConfig",
        "sagemaker:DeleteModel",
        "sagemaker:DescribeEndpoint",
        "sagemaker:DescribeEndpointConfig",
        "sagemaker:DescribeModel",
        "sagemaker:InvokeEndpoint",
        "sagemaker:ListEndpoints",
        "sagemaker:ListEndpointConfigs",
        "sagemaker:ListModels"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::your-s3-bucket/*"
    }
  ]
}
```

### VPC Configuration

For enhanced security, deploy in a VPC:

```python
# Add to deploy_deepseek.py
vpc_config = {
    'SecurityGroupIds': ['sg-xxxxxxxxx'],
    'Subnets': ['subnet-xxxxxxxxx', 'subnet-yyyyyyyyy']
}

predictor = pytorch_model.deploy(
    initial_instance_count=1,
    instance_type=instance_type,
    endpoint_name=endpoint_name,
    vpc_config=vpc_config,
    wait=True
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Out of Memory Errors:**
   - Use a larger instance type
   - Reduce model precision (float16 instead of float32)
   - Use model quantization

2. **Cold Start Delays:**
   - Keep endpoint running during business hours
   - Use provisioned concurrency for critical applications

3. **Authentication Errors:**
   - Verify AWS credentials are configured
   - Check IAM permissions
   - Ensure region matches your configuration

### Logs

View SageMaker logs:

```bash
aws logs describe-log-groups --log-group-name-prefix /aws/sagemaker/Endpoints/deepseek-coder-6.7b-instruct-endpoint
```

## 📈 Monitoring

### CloudWatch Metrics

Monitor these key metrics:

- `Invocations`: Number of endpoint invocations
- `ModelLatency`: Time to generate response
- `Invocation4XXErrors`: Client errors
- `Invocation5XXErrors`: Server errors

### Custom Metrics

Add custom metrics to track:

- Response quality
- User satisfaction
- Cost per request

## 🔄 Updates

### Model Updates

To update the deployed model:

1. Download new model version
2. Create new model artifact
3. Deploy new endpoint
4. Test new endpoint
5. Update application configuration
6. Delete old endpoint

### Code Updates

To update the inference code:

1. Modify `deepseek_inference.py`
2. Redeploy the endpoint
3. Test the changes

## 📞 Support

For issues with:

- **SageMaker**: Check AWS documentation and support
- **DeepSeek Models**: Refer to Hugging Face model pages
- **FINS Integration**: Check the main project documentation

## 📄 License

This deployment code is part of the FINS ERP system and follows the same license terms. 