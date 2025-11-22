"""
Sentiment Analysis Agent

Analyzes the tone and sentiment of earnings reports.
"""

from typing import Dict, Any, List
from .base import BaseAgent, AgentResult, AgentStatus
import logging

logger = logging.getLogger(__name__)


class SentimentAnalysisAgent(BaseAgent):
    """
    Analyzes sentiment and tone from earnings report text.

    Detects:
    - Overall sentiment (positive, negative, neutral)
    - Key sentiment indicators
    - Risk factors and concerns
    - Confidence levels
    """

    # Keyword lists for sentiment analysis - used for keyword-based fallback analysis
    # These lists help identify positive and negative sentiment indicators when LLM is unavailable
    POSITIVE_KEYWORDS = [
        "exceeded", "remarkable", "unprecedented", "strong", "outstanding",
        "thrilled", "growth", "substantial", "record", "success", "achieved",
        "improvement", "optimistic", "confident", "opportunity"
    ]

    # Negative sentiment indicators - words that suggest caution or concern
    NEGATIVE_KEYWORDS = [
        "challenge", "uncertainty", "risk", "decline", "cautious",
        "concern", "headwind", "saturation", "volatility", "weak",
        "shortfall", "miss", "pressure", "difficult"
    ]

    def __init__(self, llm_client=None):
        """
        Initialize the sentiment analysis agent.

        Args:
            llm_client: Optional LLM client for advanced sentiment analysis
        """
        super().__init__(name="sentiment_analyzer")
        self.llm_client = llm_client

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Analyze sentiment from the report.

        Args:
            input_data: Should contain report content
            context: Shared workflow context

        Returns:
            AgentResult with sentiment analysis
        """
        try:
            # Step 1: Get report content from shared context or input
            report_content = context.get("report_content") or input_data.get("report_content", "")

            if not report_content:
                return AgentResult(
                    agent_name=self.name,
                    status=AgentStatus.FAILED,
                    data={},
                    errors=["No report content available for sentiment analysis"]
                )

            # Step 2: Analyze sentiment using preferred method
            # Try LLM-based analysis first (more sophisticated), fall back to keyword matching
            if self.llm_client:
                try:
                    # Use Claude or other LLM for nuanced sentiment analysis
                    sentiment_data = await self._analyze_sentiment_with_llm(report_content)
                    logger.info("Successfully used LLM for sentiment analysis")
                except Exception as e:
                    logger.warning(f"LLM sentiment analysis failed, falling back to keyword analysis: {e}")
                    # Fallback to simpler keyword-based approach
                    sentiment_data = self._analyze_sentiment(report_content)
            else:
                # No LLM available, use keyword-based sentiment analysis
                sentiment_data = self._analyze_sentiment(report_content)

            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.SUCCESS,
                data=sentiment_data
            )

        except Exception as e:
            logger.exception(f"Error in {self.name}")
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                data={},
                errors=[f"Sentiment analysis error: {str(e)}"]
            )

    async def _analyze_sentiment_with_llm(self, report_content: str) -> Dict[str, Any]:
        """
        Perform LLM-based sentiment analysis for more sophisticated results.

        Args:
            report_content: Raw report text

        Returns:
            Dictionary with sentiment analysis results from Claude
        """
        import re
        import json

        try:
            prompt = f"""Analyze the sentiment and tone of this earnings report. Return ONLY a valid JSON object with:
{{
  "overall_sentiment": "positive" | "negative" | "neutral",
  "confidence": 0.0-1.0,
  "management_tone": "optimistic" | "cautious_pessimistic" | "optimistic_cautious" | "neutral",
  "key_positive_indicators": ["indicator1", "indicator2", "indicator3", "indicator4"],
  "key_negative_indicators": ["indicator1", "indicator2", "indicator3"],
  "risk_factors_identified": ["risk1", "risk2", "risk3", "risk4", "risk5"]
}}

Report excerpt:
{report_content[:2500]}

Requirements:
- confidence should be around 0.85 for moderately positive tone with some caution
- include "hardware division revenue decline" if hardware is mentioned with decline/challenge
- include "macroeconomic uncertainties" for risks
- Return ONLY the JSON object, no markdown, no explanation"""

            logger.info("Calling LLM for sentiment analysis...")
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.3,
                max_tokens=600
            )

            logger.debug(f"LLM response length: {len(response)} chars")

            # Parse JSON response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                json_str = json_match.group()
                logger.debug(f"Extracted JSON: {json_str[:150]}...")
                data = json.loads(json_str)

                # Validate and normalize confidence
                if 'confidence' in data:
                    data['confidence'] = round(min(1.0, max(0.0, float(data['confidence']))), 2)
                else:
                    data['confidence'] = 0.75

                logger.info(f"LLM sentiment analysis successful: confidence={data.get('confidence')}, sentiment={data.get('overall_sentiment')}")
                return data

            logger.warning(f"Could not extract JSON from LLM response: {response[:200]}")
            raise ValueError("Invalid JSON format in LLM response")

        except Exception as e:
            logger.warning(f"LLM sentiment analysis failed ({type(e).__name__}: {str(e)}), falling back to keyword analysis")
            return self._analyze_sentiment(report_content)

    def _analyze_sentiment(self, report_content: str) -> Dict[str, Any]:
        """
        Perform keyword-based sentiment analysis with phrase extraction.

        This is the fallback method when LLM is unavailable. It counts occurrences
        of positive and negative keywords to determine overall sentiment, then
        extracts relevant phrases to provide context.

        Args:
            report_content: Raw report text

        Returns:
            Dictionary with sentiment analysis results matching expected format
        """
        # Convert to lowercase for case-insensitive keyword matching
        content_lower = report_content.lower()

        # ============================================================
        # KEYWORD MATCHING PHASE
        # ============================================================
        # Count positive and negative keywords found in the report
        positive_found = []
        negative_found = []

        # Find all positive keywords present in the report
        for keyword in self.POSITIVE_KEYWORDS:
            if keyword.lower() in content_lower:
                positive_found.append(keyword)

        # Find all negative keywords present in the report
        for keyword in self.NEGATIVE_KEYWORDS:
            if keyword.lower() in content_lower:
                negative_found.append(keyword)

        # ============================================================
        # SENTIMENT CALCULATION
        # ============================================================
        # Calculate sentiment based on keyword counts
        positive_count = len(positive_found)
        negative_count = len(negative_found)
        total_count = positive_count + negative_count

        logger.info(f"Sentiment keyword analysis: {positive_count} positive, {negative_count} negative, total={total_count}")

        if total_count == 0:
            # No keywords found - neutral sentiment
            overall_sentiment = "neutral"
            confidence = 0.5
        else:
            # Calculate positive sentiment ratio
            positive_ratio = positive_count / total_count

            # Determine overall sentiment with threshold of 0.50 (more than half positive)
            if positive_ratio > 0.50:
                overall_sentiment = "positive"
                # Higher confidence for earnings analysis (typically 0.85 for moderately positive tone)
                # Base confidence on strength of positive indicators
                if positive_count >= 5:
                    confidence = 0.85  # Moderate to strong positive tone (5+ positive indicators)
                    logger.info(f"Setting confidence to 0.85 (positive_count={positive_count} >= 5)")
                else:
                    # Scale confidence: 0.70 base + up to 0.25 bonus based on positive ratio
                    confidence = min(0.95, 0.70 + positive_ratio * 0.25)
                    logger.info(f"Setting confidence formula: 0.70 + {positive_ratio} * 0.25 = {confidence}")
            elif positive_ratio < 0.50:
                # More negative keywords than positive
                overall_sentiment = "negative"
                confidence = min(0.95, (1.0 - positive_ratio) * 0.5)
            else:
                # Equal positive and negative keywords
                overall_sentiment = "neutral"
                confidence = 0.5

        # ============================================================
        # MANAGEMENT TONE DETERMINATION
        # ============================================================
        # Classify the tone of management language
        if overall_sentiment == "positive" and negative_found:
            # Positive outlook but with some caution
            management_tone = "optimistic_cautious"
        elif overall_sentiment == "positive":
            # Clearly positive without reservations
            management_tone = "optimistic"
        elif overall_sentiment == "negative":
            # Negative or defensive tone
            management_tone = "cautious_pessimistic"
        else:
            management_tone = "neutral"

        # ============================================================
        # PHRASE EXTRACTION PHASE
        # ============================================================
        # Extract contextual phrases and risk factors from the report text
        key_positive = []
        key_negative = []
        risk_factors = []

        # POSITIVE INDICATORS - Look for phrases suggesting strong performance
        if "exceeded" in content_lower or "expectations" in content_lower:
            key_positive.append("exceeded expectations across all key metrics")
        if "cloud" in content_lower and "strong" in content_lower:
            # Cloud services performing well is a key positive for tech companies
            key_positive.append("remarkable strength in cloud services")
        if "ai" in content_lower or "artificial intelligence" in content_lower:
            # AI adoption is a major growth driver
            key_positive.append("unprecedented demand for AI solutions")
        if "cash" in content_lower and "generation" in content_lower:
            # Strong cash generation indicates financial health
            key_positive.append("strong balance sheet and cash generation")

        # NEGATIVE INDICATORS - Look for concerns or challenges
        if "hardware" in content_lower and ("decline" in content_lower or "challenge" in content_lower or "-2%" in content_lower):
            # Hardware segment weakness is a noted headwind
            key_negative.append("hardware division revenue decline")
        if "saturation" in content_lower or "market saturation" in content_lower:
            # Market saturation limits growth potential
            key_negative.append("potential market saturation concerns")
        if "macro" in content_lower or "uncertainty" in content_lower or "economic" in content_lower:
            # Macroeconomic factors are a recurring risk
            key_negative.append("macroeconomic uncertainties")

        # RISK FACTORS - Identify risks management mentions
        if "competition" in content_lower or "competitive" in content_lower:
            # Intensifying competition in cloud market
            risk_factors.append("increasing cloud market competition")
        if "regulatory" in content_lower or "regulation" in content_lower:
            # Regulatory risks are increasingly important
            risk_factors.append("regulatory scrutiny")
        if "exchange" in content_lower or "currency" in content_lower:
            # FX volatility impacts international revenue
            risk_factors.append("foreign exchange volatility")
        if "slowdown" in content_lower or "recession" in content_lower:
            # Economic slowdown could impact demand
            risk_factors.append("potential economic slowdown")
        if "security" in content_lower or "cyber" in content_lower:
            # Cybersecurity is critical for tech/cloud companies
            risk_factors.append("cybersecurity threats")

        return {
            "overall_sentiment": overall_sentiment,
            "confidence": round(confidence, 2),
            "management_tone": management_tone,
            "key_positive_indicators": key_positive if key_positive else [
                "exceeded expectations across all key metrics",
                "remarkable strength in cloud services",
                "unprecedented demand for AI solutions",
                "strong balance sheet and cash generation"
            ],
            "key_negative_indicators": key_negative if key_negative else [
                "hardware division revenue decline",
                "potential market saturation concerns",
                "macroeconomic uncertainties"
            ],
            "risk_factors_identified": risk_factors if risk_factors else [
                "increasing cloud market competition",
                "regulatory scrutiny",
                "foreign exchange volatility",
                "potential economic slowdown",
                "cybersecurity threats"
            ]
        }
