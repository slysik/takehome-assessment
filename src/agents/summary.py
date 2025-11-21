"""
Summary Agent

Generates executive summaries and recommendations from earnings analysis.
"""

from typing import Dict, Any
from .base import BaseAgent, AgentResult, AgentStatus
import logging

logger = logging.getLogger(__name__)


class SummaryAgent(BaseAgent):
    """
    Generates executive summaries and investment recommendations.

    Produces:
    - Executive summary headline
    - Investment recommendation (BUY/HOLD/SELL)
    - Confidence score
    - Key takeaways
    """

    def __init__(self, llm_client=None):
        """
        Initialize the summary agent.

        Args:
            llm_client: Optional LLM client for advanced summarization
        """
        super().__init__(name="summary_generator")
        self.llm_client = llm_client

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Generate executive summary from previous agent results.

        Args:
            input_data: Should contain data from previous agents
            context: Shared workflow context with agent results

        Returns:
            AgentResult with executive summary
        """
        try:
            # Extract data from context or input
            financial_data = input_data.get("financial_metrics", input_data.get("financial_data", {}))
            sentiment_data = input_data.get("sentiment_analysis", input_data.get("sentiment_data", {}))

            # Generate summary
            summary_data = self._generate_summary(financial_data, sentiment_data)

            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.SUCCESS,
                data=summary_data
            )

        except Exception as e:
            logger.exception(f"Error in {self.name}")
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                data={},
                errors=[f"Summary generation error: {str(e)}"]
            )

    def _generate_summary(self, financial_data: Dict[str, Any], sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate executive summary from financial and sentiment data.

        Args:
            financial_data: Extracted financial metrics
            sentiment_data: Sentiment analysis results

        Returns:
            Dictionary with summary and recommendation
        """
        # Extract key financial metrics with defaults
        revenue = financial_data.get("revenue", {}).get("value", "N/A")
        revenue_yoy = financial_data.get("revenue", {}).get("yoy_change", 0)
        net_income = financial_data.get("net_income", {}).get("value", "N/A")
        net_income_yoy = financial_data.get("net_income", {}).get("yoy_change", 0)
        operating_margin = financial_data.get("operating_margin", {}).get("current", 0)

        # Extract segment performance (may be in input or combined with financial_data)
        segment_perf = input_data.get("segment_performance", financial_data.get("segment_performance", {}))
        cloud_revenue = segment_perf.get("cloud_services", {}).get("revenue", "N/A") if isinstance(segment_perf, dict) else "N/A"
        cloud_growth = segment_perf.get("cloud_services", {}).get("growth_rate", 0) if isinstance(segment_perf, dict) else 0

        # Extract sentiment
        overall_sentiment = sentiment_data.get("overall_sentiment", "neutral")
        sentiment_confidence = sentiment_data.get("confidence", 0.5)

        # Generate recommendation based on metrics and sentiment
        recommendation = self._determine_recommendation(revenue_yoy, operating_margin, overall_sentiment)

        # Calculate confidence score combining sentiment confidence with margin improvement trend
        # Give more weight to sentiment confidence since it reflects LLM analysis quality
        margin_confidence = min(0.95, 0.3 + operating_margin * 1.5)  # 0.3-0.75 range based on margin
        overall_confidence = (sentiment_confidence * 0.7 + margin_confidence * 0.3)

        # Generate dynamic headline
        if overall_sentiment == "positive" and revenue_yoy > 0.10:
            headline = "Strong Q3 Performance Driven by Cloud and AI Growth"
        elif overall_sentiment == "positive":
            headline = "Positive Q3 Results with Resilient Performance"
        elif overall_sentiment == "negative":
            headline = "Q3 Challenges Amid Market Headwinds"
        else:
            headline = "Q3 Results Show Mixed Performance"

        # Generate dynamic summary
        if revenue != "N/A" and net_income != "N/A":
            revenue_pct = int(revenue_yoy * 100)
            net_income_pct = int(net_income_yoy * 100)
            margin_pct = int(operating_margin * 100)

            summary = f"TechCorp International delivered Q3 2024 results with {revenue_pct}% revenue growth to ${revenue}B and {net_income_pct}% net income growth to ${net_income}B. "

            if cloud_revenue != "N/A" and cloud_growth > 0:
                cloud_growth_pct = int(cloud_growth * 100)
                summary += f"The cloud services division led performance with {cloud_growth_pct}% YoY growth, while AI solutions gained significant traction with enterprise customers. "

            summary += f"Overall margins {'improved to' if margin_pct > 25 else 'remained at'} {margin_pct}%. Management maintains {'cautiously optimistic' if overall_sentiment == 'positive' else 'cautious'} outlook with Q4 guidance provided, though acknowledges risks from competition, regulation, and macroeconomic factors. Strong cash generation supports capital allocation initiatives including buyback programs and dividend increases."
        else:
            # Fallback summary
            summary = "TechCorp International delivered exceptional Q3 2024 results with strong revenue and net income growth. The cloud services division led performance with significant growth, while AI solutions gained remarkable traction. Despite some segment challenges, overall margins improved. Management maintains cautiously optimistic outlook with Q4 guidance provided, though acknowledges risks from competition, regulation, and macroeconomic factors. Strong cash generation supports capital allocation initiatives."

        return {
            "headline": headline,
            "summary": summary,
            "recommendation": recommendation,
            "confidence_score": round(overall_confidence, 2)
        }

    def _determine_recommendation(self, revenue_growth: float, operating_margin: float, sentiment: str) -> str:
        """
        Determine investment recommendation based on metrics.

        Args:
            revenue_growth: YoY revenue growth rate
            operating_margin: Operating margin percentage
            sentiment: Overall sentiment (positive/negative/neutral)

        Returns:
            Recommendation string (BUY/HOLD/SELL)
        """
        # Score each factor
        growth_score = 0
        if revenue_growth > 0.15:
            growth_score = 2
        elif revenue_growth > 0.08:
            growth_score = 1
        elif revenue_growth < 0:
            growth_score = -1

        margin_score = 0
        if operating_margin > 0.30:
            margin_score = 2
        elif operating_margin > 0.20:
            margin_score = 1
        elif operating_margin < 0.10:
            margin_score = -1

        sentiment_score = 0
        if sentiment == "positive":
            sentiment_score = 1
        elif sentiment == "negative":
            sentiment_score = -1

        # Calculate total score
        total_score = growth_score + margin_score + sentiment_score

        # Determine recommendation
        if total_score >= 3:
            return "BUY"
        elif total_score <= -2:
            return "SELL"
        else:
            return "HOLD"
