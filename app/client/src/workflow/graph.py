"""LangGraph workflow orchestration for multi-agent earnings analysis"""

from typing import Dict, Any, TypedDict, Optional
from langgraph.graph import StateGraph, END
import logging

logger = logging.getLogger(__name__)


class AnalysisState(TypedDict):
    """State schema for the earnings analysis workflow"""
    report_content: str
    report_metadata: Optional[Dict[str, Any]]
    financial_metrics: Dict[str, Any]
    segment_performance: Dict[str, Any]
    forward_guidance: Dict[str, Any]
    sentiment_analysis: Dict[str, Any]
    executive_summary: Dict[str, Any]
    metadata: Dict[str, Any]
    errors: list


class WorkflowGraph:
    """LangGraph workflow for multi-agent orchestration"""

    def __init__(self, coordinator_agent, data_extractor_agent, sentiment_agent, summary_agent):
        """
        Initialize the workflow with agents.

        Args:
            coordinator_agent: CoordinatorAgent instance
            data_extractor_agent: DataExtractorAgent instance
            sentiment_agent: SentimentAnalysisAgent instance
            summary_agent: SummaryAgent instance
        """
        self.coordinator = coordinator_agent
        self.data_extractor = data_extractor_agent
        self.sentiment = sentiment_agent
        self.summary = summary_agent

        # Register agents with coordinator
        self.coordinator.register_agent("data_extractor", data_extractor_agent)
        self.coordinator.register_agent("sentiment_analyzer", sentiment_agent)
        self.coordinator.register_agent("summary_generator", summary_agent)

        # Build the graph
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow graph"""
        workflow = StateGraph(AnalysisState)

        # Define node functions
        workflow.add_node("coordinator", self._coordinator_node)
        workflow.add_node("data_extraction", self._data_extraction_node)
        workflow.add_node("sentiment_analysis", self._sentiment_analysis_node)
        workflow.add_node("summary_generation", self._summary_generation_node)

        # Set entry point
        workflow.set_entry_point("coordinator")

        # Define edges
        workflow.add_edge("coordinator", "data_extraction")
        workflow.add_edge("data_extraction", "sentiment_analysis")
        workflow.add_edge("sentiment_analysis", "summary_generation")
        workflow.add_edge("summary_generation", END)

        logger.info("LangGraph workflow graph constructed successfully")
        return workflow

    async def _coordinator_node(self, state: AnalysisState) -> AnalysisState:
        """
        Coordinator node that validates and initializes the workflow.
        """
        logger.info("Coordinator node executing")
        state["metadata"] = {
            "status": "initialized",
            "agents": ["coordinator", "data_extractor", "sentiment_analyzer", "summary_generator"]
        }
        return state

    async def _data_extraction_node(self, state: AnalysisState) -> AnalysisState:
        """
        Data extraction node that processes financial metrics.
        """
        logger.info("Data extraction node executing")
        try:
            result = await self.data_extractor.process(
                {"report_content": state["report_content"]},
                state
            )

            if result.status.value == "success":
                state["financial_metrics"] = result.data.get("financial_metrics", {})
                state["segment_performance"] = result.data.get("segment_performance", {})
                state["forward_guidance"] = result.data.get("forward_guidance", {})
                logger.info("Data extraction completed successfully")
            else:
                state["errors"].append(f"Data extraction failed: {result.errors}")
                logger.error(f"Data extraction failed: {result.errors}")

        except Exception as e:
            state["errors"].append(f"Data extraction error: {str(e)}")
            logger.error(f"Data extraction error: {str(e)}")

        return state

    async def _sentiment_analysis_node(self, state: AnalysisState) -> AnalysisState:
        """
        Sentiment analysis node that analyzes management tone and risk factors.
        """
        logger.info("Sentiment analysis node executing")
        try:
            result = await self.sentiment.process(
                {"report_content": state["report_content"]},
                state
            )

            if result.status.value == "success":
                state["sentiment_analysis"] = result.data
                logger.info("Sentiment analysis completed successfully")
            else:
                state["errors"].append(f"Sentiment analysis failed: {result.errors}")
                logger.error(f"Sentiment analysis failed: {result.errors}")

        except Exception as e:
            state["errors"].append(f"Sentiment analysis error: {str(e)}")
            logger.error(f"Sentiment analysis error: {str(e)}")

        return state

    async def _summary_generation_node(self, state: AnalysisState) -> AnalysisState:
        """
        Summary node that consolidates all findings.
        """
        logger.info("Summary generation node executing")
        try:
            # Prepare summary input from previous agent outputs
            summary_input = {
                "financial_metrics": state["financial_metrics"],
                "sentiment_analysis": state["sentiment_analysis"],
                "metadata": state.get("metadata", {})
            }

            result = await self.summary.process(summary_input, state)

            if result.status.value == "success":
                state["executive_summary"] = result.data
                logger.info("Summary generation completed successfully")
            else:
                state["errors"].append(f"Summary generation failed: {result.errors}")
                logger.error(f"Summary generation failed: {result.errors}")

        except Exception as e:
            state["errors"].append(f"Summary generation error: {str(e)}")
            logger.error(f"Summary generation error: {str(e)}")

        return state

    async def invoke(self, report_content: str, options: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Invoke the workflow with a report.

        Args:
            report_content: The earnings report text
            options: Optional configuration options

        Returns:
            Analysis results dictionary
        """
        logger.info("Invoking workflow with report")

        # Initialize state
        state: AnalysisState = {
            "report_content": report_content,
            "report_metadata": options or {},
            "financial_metrics": {},
            "segment_performance": {},
            "forward_guidance": {},
            "sentiment_analysis": {},
            "executive_summary": {},
            "metadata": {},
            "errors": []
        }

        # Execute compiled graph
        try:
            final_state = await self.compiled_graph.ainvoke(state)
            logger.info("Workflow execution completed")
            return final_state
        except Exception as e:
            logger.error(f"Workflow execution failed: {str(e)}")
            state["errors"].append(f"Workflow execution failed: {str(e)}")
            return state
