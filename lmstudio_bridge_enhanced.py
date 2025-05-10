#!/usr/bin/env python3
# lmstudio_bridge_enhanced.py - Enhanced functionality for lmstudio_bridge

from lmstudio_bridge import mcp, LMSTUDIO_API_BASE, log_error, log_info

import requests
import json
from typing import List, Dict, Any, Optional

# 여기서는 새로운 mcp 인스턴스를 만들지 않고, 기존 인스턴스를 재사용합니다

@mcp.tool()
async def enhanced_chat_completion(
    prompt: str, 
    system_prompt: str = "", 
    temperature: float = 0.7, 
    max_tokens: int = 1024,
    model: str = None,
    stop_sequences: List[str] = None,
    top_p: float = 1.0
) -> str:
    """Generate a completion with enhanced options from the LM Studio model.
    
    Args:
        prompt: The user's prompt to send to the model
        system_prompt: Optional system instructions for the model
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum number of tokens to generate
        model: Specific model to use (if None, uses default loaded model)
        stop_sequences: Optional list of sequences where the API will stop generating
        top_p: Nucleus sampling parameter
        
    Returns:
        The model's response to the prompt
    """
    try:
        messages = []
        
        # Add system message if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add user message
        messages.append({"role": "user", "content": prompt})
        
        log_info(f"Sending enhanced request to LM Studio with {len(messages)} messages")
        
        # Prepare request payload with enhanced parameters
        payload = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }
        
        # Add optional parameters if provided
        if model:
            payload["model"] = model
            
        if stop_sequences:
            payload["stop"] = stop_sequences
        
        response = requests.post(
            f"{LMSTUDIO_API_BASE}/chat/completions",
            json=payload
        )
        
        if response.status_code != 200:
            log_error(f"LM Studio API error: {response.status_code}")
            return f"Error: LM Studio returned status code {response.status_code}"
        
        response_json = response.json()
        log_info(f"Received response from LM Studio")
        
        # Extract the assistant's message
        choices = response_json.get("choices", [])
        if not choices:
            return "Error: No response generated"
        
        message = choices[0].get("message", {})
        content = message.get("content", "")
        
        if not content:
            return "Error: Empty response from model"
        
        return content
    except Exception as e:
        log_error(f"Error in enhanced_chat_completion: {str(e)}")
        return f"Error generating completion: {str(e)}"

@mcp.tool()
async def batch_chat_completion(prompts: List[str], system_prompt: str = "") -> List[str]:
    """Process multiple prompts in a batch.
    
    Args:
        prompts: List of prompts to process
        system_prompt: Optional system instructions to apply to all prompts
        
    Returns:
        List of model responses corresponding to each prompt
    """
    results = []
    for prompt in prompts:
        try:
            # lmstudio_bridge의 chat_completion을 직접 호출하지 않고
            # API를 직접 호출합니다 (동일한 로직 사용)
            messages = []
            
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            messages.append({"role": "user", "content": prompt})
            
            response = requests.post(
                f"{LMSTUDIO_API_BASE}/chat/completions",
                json={
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
            )
            
            if response.status_code != 200:
                results.append(f"Error: Status code {response.status_code}")
                continue
                
            response_json = response.json()
            choices = response_json.get("choices", [])
            if not choices:
                results.append("Error: No response generated")
                continue
                
            message = choices[0].get("message", {})
            content = message.get("content", "")
            
            if not content:
                results.append("Error: Empty response")
                continue
                
            results.append(content)
                
        except Exception as e:
            log_error(f"Error in batch processing: {str(e)}")
            results.append(f"Error: {str(e)}")
    
    return results
