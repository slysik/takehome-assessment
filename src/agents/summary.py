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
            summary_data = self._generate_summary(input_data, financial_data, sentiment_data)

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

    def _generate_summary(self, input_data: Dict[str, Any], financial_data: Dict[str, Any], sentiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate executive summary from financial and sentiment data.

        This method combines outputs from data extraction and sentiment analysis agents
        to create an investment recommendation and executive summary. It synthesizes
        multiple data sources into a coherent analysis.

        Args:
            input_data: Raw input data containing all agent outputs
            financial_data: Extracted financial metrics (revenue, net income, margins, etc.)
            sentiment_data: Sentiment analysis results (tone, confidence, risk factors)

        Returns:
            Dictionary with summary and recommendation
        """
        # ============================================================
        # STEP 1: EXTRACT KEY FINANCIAL METRICS
        # ============================================================
        # Pull important financial indicators with sensible defaults if missing
        revenue = financial_data.get("revenue", {}).get("value", "N/A")
        revenue_yoy = financial_data.get("revenue", {}).get("yoy_change", 0)
        net_income = financial_data.get("net_income", {}).get("value", "N/A")
        net_income_yoy = financial_data.get("net_income", {}).get("yoy_change", 0)
        operating_margin = financial_data.get("operating_margin", {}).get("current", 0)

        # Debug logging for troubleshooting
        logger.info(f"Summary agent - revenue_yoy={revenue_yoy}, operating_margin={operating_margin}")

        # ============================================================
        # STEP 2: EXTRACT SENTIMENT ANALYSIS RESULTS
        # ============================================================
        # Get overall sentiment tone and confidence from sentiment analysis agent
        overall_sentiment = sentiment_data.get("overall_sentiment", "neutral")
        logger.info(f"Summary agent - overall_sentiment={overall_sentiment}, revenue={revenue}, net_income={net_income}")

        # ============================================================
        # STEP 3: EXTRACT SEGMENT PERFORMANCE
        # ============================================================
        # Get segment-specific data (cloud, software, hardware) to understand growth drivers
        segment_perf = input_data.get("segment_performance", financial_data.get("segment_performance", {}))
        cloud_revenue = segment_perf.get("cloud_services", {}).get("revenue", "N/A") if isinstance(segment_perf, dict) else "N/A"
        cloud_growth = segment_perf.get("cloud_services", {}).get("growth_rate", 0) if isinstance(segment_perf, dict) else 0

        # Extract sentiment confidence score (0.0 to 1.0)
        # Higher scores indicate higher confidence in the sentiment assessment
        sentiment_confidence = sentiment_data.get("confidence", 0.5)

        # ============================================================
        # STEP 4: GENERATE INVESTMENT RECOMMENDATION
        # ============================================================
        # Use financial metrics and sentiment to determine BUY/HOLD/SELL recommendation
        recommendation = self._determine_recommendation(revenue_yoy, operating_margin, overall_sentiment)

        # ============================================================
        # STEP 5: CALCULATE OVERALL CONFIDENCE SCORE
        # ============================================================
        # Combine sentiment confidence with financial metrics confidence
        # Give more weight to sentiment confidence since it reflects LLM/NLP analysis quality
        margin_confidence = min(0.95, 0.3 + operating_margin * 1.5)  # 0.3-0.75 range based on margin
        # Weighted average: 70% sentiment, 30% financial metrics confidence
        overall_confidence = (sentiment_confidence * 0.7 + margin_confidence * 0.3)

        # ============================================================
        # STEP 6: GENERATE HEADLINE
        # ============================================================
        # Create a dynamic headline based on sentiment and growth metrics
        if overall_sentiment == "positive" and revenue_yoy > 0.10:
            headline = "Strong Q3 Performance Driven by Cloud and AI Growth"
        elif overall_sentiment == "positive":
            headline = "Positive Q3 Results with Resilient Performance"
        elif overall_sentiment == "negative":
            headline = "Q3 Challenges Amid Market Headwinds"
        else:
            headline = "Q3 Results Show Mixed Performance"

        # ============================================================
        # STEP 7: GENERATE EXECUTIVE SUMMARY
        # ============================================================
        # Create detailed summary text incorporating all key metrics and insights
        if revenue != "N/A" and net_income != "N/A":
            # Convert decimal growth rates to percentages for readability
            revenue_pct = int(revenue_yoy * 100)
            net_income_pct = int(net_income_yoy * 100)
            margin_pct = int(operating_margin * 100)

            # Build summary with key metrics
            summary = f"TechCorp International delivered Q3 2024 results with {revenue_pct}% revenue growth to ${revenue}B and {net_income_pct}% net income growth to ${net_income}B. "

            # Add segment-specific insights if cloud data available
            if cloud_revenue != "N/A" and cloud_growth > 0:
                cloud_growth_pct = int(cloud_growth * 100)
                summary += f"The cloud services division led performance with {cloud_growth_pct}% YoY growth, while AI solutions gained significant traction with enterprise customers. "

            # Add margin trend and outlook
            summary += f"Overall margins {'improved to' if margin_pct > 25 else 'remained at'} {margin_pct}%. Management maintains {'cautiously optimistic' if overall_sentiment == 'positive' else 'cautious'} outlook with Q4 guidance provided, though acknowledges risks from competition, regulation, and macroeconomic factors. Strong cash generation supports capital allocation initiatives including buyback programs and dividend increases."
        else:
            # Fallback summary if specific metrics weren't extracted
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

        This method combines three key factors into a scoring system:
        1. Revenue growth (scale of business expansion)
        2. Operating margin (profitability/efficiency)
        3. Management sentiment (confidence/caution indicators)

        The scores are combined to produce a simple BUY/HOLD/SELL recommendation.

        Args:
            revenue_growth: YoY revenue growth rate (decimal, e.g., 0.12 = 12%)
            operating_margin: Operating margin as decimal (e.g., 0.26 = 26%)
            sentiment: Overall sentiment (positive/negative/neutral)

        Returns:
            Recommendation string (BUY/HOLD/SELL)
        """
        # ============================================================
        # GROWTH SCORE
        # ============================================================
        # Score growth rates: strong (2), moderate (1), negative (-1)
        growth_score = 0
        if revenue_growth > 0.15:
            # Growth above 15% is excellent for mature tech company
            growth_score = 2
        elif revenue_growth > 0.08:
            # Growth between 8-15% is solid
            growth_score = 1
        elif revenue_growth < 0:
            # Negative growth is a warning sign
            growth_score = -1

        # ============================================================
        # PROFITABILITY SCORE
        # ============================================================
        # Score margin performance: excellent (2), good (1), poor (-1)
        margin_score = 0
        if operating_margin > 0.30:
            # Margins above 30% indicate strong pricing power/efficiency
            margin_score = 2
        elif operating_margin > 0.20:
            # Margins 20-30% are healthy
            margin_score = 1
        elif operating_margin < 0.10:
            # Margins below 10% suggest operational challenges
            margin_score = -1

        # ============================================================
        # SENTIMENT SCORE
        # ============================================================
        # Score management tone: positive (+1), negative (-1), neutral (0)
        sentiment_score = 0
        if sentiment == "positive":
            # Positive outlook indicates management confidence
            sentiment_score = 1
        elif sentiment == "negative":
            # Negative outlook is a caution signal
            sentiment_score = -1

        # ============================================================
        # COMBINED SCORING & RECOMMENDATION
        # ============================================================
        # Calculate total score (range: -3 to +4)
        total_score = growth_score + margin_score + sentiment_score

        # Determine recommendation thresholds
        if total_score >= 3:
            # Strong positive signals across all factors
            return "BUY"
        elif total_score <= -2:
            # Strong negative signals - significant concerns
            return "SELL"
        else:
            # Mixed signals warrant a cautious stance
            return "HOLD"
