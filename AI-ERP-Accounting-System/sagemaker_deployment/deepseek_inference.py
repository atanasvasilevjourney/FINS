#!/usr/bin/env python3
"""
SageMaker inference script for DeepSeek model
This script handles model loading and inference for DeepSeek deployed on SageMaker
"""

import os
import json
import logging
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekInference:
    def __init__(self):
        """Initialize the DeepSeek model and tokenizer"""
        self.model = None
        self.tokenizer = None
        self.device = None
        
    def model_fn(self, model_dir: str):
        """
        Load the model from the model directory
        This function is called by SageMaker when the endpoint starts
        """
        try:
            logger.info(f"Loading model from {model_dir}")
            
            # Set device
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Using device: {self.device}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_dir,
                trust_remote_code=True,
                padding_side="left"
            )
            
            # Add pad token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                model_dir,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                trust_remote_code=True
            )
            
            if torch.cuda.is_available():
                self.model = self.model.to(self.device)
            
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def input_fn(self, request_body: str, request_content_type: str) -> Dict[str, Any]:
        """
        Parse input data from the request
        """
        if request_content_type == "application/json":
            input_data = json.loads(request_body)
            return input_data
        else:
            raise ValueError(f"Unsupported content type: {request_content_type}")
    
    def predict_fn(self, input_data: Dict[str, Any]) -> str:
        """
        Perform inference using the loaded model
        """
        try:
            # Extract parameters
            prompt = input_data.get("prompt", "")
            max_tokens = input_data.get("max_tokens", 512)
            temperature = input_data.get("temperature", 0.7)
            top_p = input_data.get("top_p", 0.9)
            stop_sequences = input_data.get("stop", ["\n\n", "Human:", "Assistant:"])
            
            logger.info(f"Generating response for prompt: {prompt[:100]}...")
            
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=2048
            )
            
            if torch.cuda.is_available():
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            generated_text = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[1]:],
                skip_special_tokens=True
            )
            
            # Apply stop sequences
            for stop_seq in stop_sequences:
                if stop_seq in generated_text:
                    generated_text = generated_text.split(stop_seq)[0]
            
            logger.info(f"Generated response: {generated_text[:100]}...")
            return generated_text.strip()
            
        except Exception as e:
            logger.error(f"Error during inference: {e}")
            raise
    
    def output_fn(self, prediction: str, accept: str) -> str:
        """
        Format the prediction output
        """
        if accept == "application/json":
            return json.dumps({"generated_text": prediction})
        else:
            return prediction

# Global inference object
inference = DeepSeekInference()

def model_fn(model_dir: str):
    """SageMaker model loading function"""
    return inference.model_fn(model_dir)

def input_fn(request_body: str, request_content_type: str):
    """SageMaker input processing function"""
    return inference.input_fn(request_body, request_content_type)

def predict_fn(input_data: Dict[str, Any]):
    """SageMaker prediction function"""
    return inference.predict_fn(input_data)

def output_fn(prediction: str, accept: str):
    """SageMaker output formatting function"""
    return inference.output_fn(prediction, accept) 