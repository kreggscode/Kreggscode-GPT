"""
AI Client for KreggsScode GPT
Handles communication with Pollinations.AI API
"""

import requests
import json
from typing import Optional, List, Dict


class AIClient:
    """Client for interacting with Pollinations.AI API"""
    
    def __init__(self, model: str = "openai", temperature: float = 1.0):
        """
        Initialize AI Client
        
        Args:
            model: AI model to use (default: openai)
            temperature: Creativity level 0.0-3.0 (default: 1.0)
        """
        self.base_url = "https://text.pollinations.ai"
        self.model = model
        self.temperature = temperature
        self.conversation_history: List[Dict[str, str]] = []
        
    def chat(self, user_message: str, system_prompt: Optional[str] = None) -> str:
        """
        Send a message to the AI and get a response
        
        Args:
            user_message: The user's message
            system_prompt: Optional system prompt to guide AI behavior
            
        Returns:
            AI's response as a string
        """
        try:
            # Build messages array
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add conversation history
            messages.extend(self.conversation_history)
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "stream": False
            }
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/openai",
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            # Update conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            # Keep only last 10 messages to avoid token limits
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            return ai_response
            
        except requests.exceptions.RequestException as e:
            return f"Error communicating with AI: {str(e)}"
        except (KeyError, json.JSONDecodeError) as e:
            return f"Error parsing AI response: {str(e)}"
    
    def simple_query(self, prompt: str) -> str:
        """
        Simple query without conversation history
        
        Args:
            prompt: The prompt to send
            
        Returns:
            AI's response as a string
        """
        try:
            # Use simple GET endpoint
            from urllib.parse import quote
            url = f"{self.base_url}/{quote(prompt)}"
            params = {
                "model": self.model,
                "temperature": self.temperature
            }
            
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            
            return response.text
            
        except requests.exceptions.RequestException as e:
            return f"Error communicating with AI: {str(e)}"
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def set_temperature(self, temperature: float):
        """
        Set the temperature (creativity level)
        
        Args:
            temperature: Value between 0.0 (strict) and 3.0 (creative)
        """
        self.temperature = max(0.0, min(3.0, temperature))
    
    def set_model(self, model: str):
        """
        Change the AI model
        
        Args:
            model: Model name (e.g., 'openai', 'mistral')
        """
        self.model = model
