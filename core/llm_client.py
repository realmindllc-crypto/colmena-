"""LLM client wrapper for PROYECTO COLMENA."""

import os
from typing import Optional, Dict, Any, List
import logging
from openai import OpenAI
from shared.exceptions import LLMException, ConfigException


class LLMClient:
    """Wrapper around OpenAI API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.logger = logging.getLogger("LLMClient")

        if not self.api_key:
            raise ConfigException("OPENAI_API_KEY not found in environment")

        self.client = OpenAI(api_key=self.api_key)
        self.logger.info(f"LLM client initialized with model: {self.model}")

    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
    ) -> str:
        """Send chat message to LLM."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"LLM error: {e}")
            raise LLMException(f"LLM call failed: {e}")

    def analyze_text(
        self,
        text: str,
        instruction: str = "Analyze the following text:",
    ) -> str:
        """Analyze text with LLM."""
        messages = [
            {"role": "system", "content": "You are a financial analyst expert."},
            {"role": "user", "content": f"{instruction}\n\n{text}"},
        ]
        return self.chat(messages)

    def extract_json(
        self,
        text: str,
        instruction: str = "Extract key information from the following text and return as JSON:",
    ) -> Dict[str, Any]:
        """Extract structured JSON from text."""
        messages = [
            {"role": "system", "content": "You are a data extraction expert. Always return valid JSON."},
            {"role": "user", "content": f"{instruction}\n\n{text}"},
        ]
        response = self.chat(messages)
        
        try:
            import json
            return json.loads(response)
        except json.JSONDecodeError:
            self.logger.warning(f"Failed to parse JSON response: {response}")
            return {"raw_response": response}
