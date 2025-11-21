"""Anthropic LLM Client for agent interactions"""

import os
import logging
from typing import Dict, Any, Optional
import json

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

logger = logging.getLogger(__name__)


class AnthropicLLMClient:
    """
    Client for interacting with Anthropic's Claude models.
    """

    def __init__(self, model: str = "claude-sonnet-4-5-20250929", api_key: Optional[str] = None):
        """
        Initialize the Anthropic LLM client.

        Args:
            model: Model ID to use (defaults to claude-sonnet-4-5)
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        if Anthropic is None:
            raise ImportError("anthropic package not installed. Install with: pip install anthropic")

        self.model = model
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")

        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not provided. Set it via parameter or environment variable."
            )

        self.client = Anthropic(api_key=self.api_key)
        logger.info(f"Initialized Anthropic LLM client with model: {model}")

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system: Optional[str] = None
    ) -> str:
        """
        Generate text using Claude.

        Args:
            prompt: The input prompt
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            system: Optional system prompt

        Returns:
            Generated text response
        """
        try:
            messages = [{"role": "user", "content": prompt}]

            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system or self._get_default_system_prompt(),
                messages=messages
            )

            # Extract text from response
            text = response.content[0].text if response.content else ""
            logger.debug(f"Generated {len(text)} characters of text")
            return text

        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise

    async def extract_json(
        self,
        text: str,
        schema: Dict[str, Any],
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """
        Extract structured data (JSON) from text.

        Args:
            text: Text to extract from
            schema: Expected JSON schema
            temperature: Sampling temperature

        Returns:
            Extracted JSON data
        """
        try:
            prompt = f"""Extract structured data from the following text. Return only valid JSON matching this schema:

Schema: {json.dumps(schema)}

Text:
{text}

Return ONLY the JSON object, no additional text."""

            response = await self.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=1000
            )

            # Parse JSON response
            import re
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())

            logger.warning("Could not extract JSON from response")
            return {}

        except Exception as e:
            logger.error(f"Error extracting JSON: {str(e)}")
            return {}

    def _get_default_system_prompt(self) -> str:
        """Get default system prompt for financial analysis"""
        return """You are an expert financial analyst specializing in earnings reports analysis.
Your role is to:
1. Extract key financial metrics accurately
2. Analyze sentiment and tone in management commentary
3. Identify risks and opportunities
4. Provide clear, structured insights

Always respond with clear, factual analysis based on the provided data.
Format structured data as JSON when requested.
Be precise with numbers and percentages.
Highlight important context and trends."""

    def health_check(self) -> bool:
        """Check if the client is properly configured"""
        try:
            # Try a simple message to verify connectivity
            response = self.client.messages.create(
                model=self.model,
                max_tokens=10,
                messages=[{"role": "user", "content": "ok"}]
            )
            return bool(response)
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False


class MockLLMClient:
    """
    Mock LLM client for testing without API calls.
    """

    def __init__(self):
        """Initialize mock client"""
        logger.info("Initialized Mock LLM client")

    async def generate(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        system: Optional[str] = None
    ) -> str:
        """Generate mock response"""
        # Return structured mock data based on prompt
        if "financial" in prompt.lower() or "metric" in prompt.lower():
            return json.dumps({
                "financial_metrics": {
                    "revenue": {"value": 15.2, "unit": "billion USD", "yoy_change": 0.12},
                    "net_income": {"value": 3.8, "unit": "billion USD", "yoy_change": 0.18},
                    "eps": {"value": 4.52, "analyst_estimate": 4.30, "beat_estimate": True},
                    "operating_margin": {"current": 0.285, "previous": 0.262}
                },
                "segment_performance": {
                    "cloud_services": {"revenue": 6.8, "growth_rate": 0.35}
                },
                "forward_guidance": {
                    "q4_2024": {"revenue_range": [16.0, 16.5]}
                }
            })
        elif "sentiment" in prompt.lower():
            return json.dumps({
                "overall_sentiment": "positive",
                "confidence": 0.85,
                "management_tone": "optimistic_cautious",
                "key_positive_indicators": [
                    "exceeded expectations",
                    "remarkable cloud growth",
                    "strong cash generation"
                ],
                "key_negative_indicators": [
                    "hardware decline",
                    "competition increasing"
                ],
                "risk_factors_identified": [
                    "market competition",
                    "regulatory scrutiny",
                    "economic uncertainty"
                ]
            })
        else:
            return "Mock LLM response"

    async def extract_json(
        self,
        text: str,
        schema: Dict[str, Any],
        temperature: float = 0.2
    ) -> Dict[str, Any]:
        """Extract mock JSON"""
        return {"mock": "data"}

    def health_check(self) -> bool:
        """Mock health check"""
        return True
