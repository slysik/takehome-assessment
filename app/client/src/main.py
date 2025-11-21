"""
Main Application Entry Point

This module sets up the FastAPI application and defines the REST API endpoints
for your multi-agent earnings analysis system.

Here's what you need to complete:
1. Agent initialization - Create your agent instances
2. LangGraph workflow setup - Wire up your agents
3. Error handling and retry logic - Make it production-ready
4. Proper async execution - Ensure efficient processing
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
import logging
import os
from datetime import datetime
from pathlib import Path

# Import agents
from src.agents.coordinator import CoordinatorAgent
from src.agents.data_extractor import DataExtractorAgent
from src.agents.sentiment import SentimentAnalysisAgent
from src.agents.summary import SummaryAgent
from src.llm_client import AnthropicLLMClient, MockLLMClient
from src.workflow.graph import WorkflowGraph

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Multi-Agent Earnings Analyzer",
    description="Analyzes earnings reports using specialized AI agents",
    version="1.0.0"
)


# Request/Response Models
class AnalysisRequest(BaseModel):
    """Request model for earnings analysis"""
    report_path: str = Field(..., description="Path to the earnings report file")
    options: Optional[Dict[str, Any]] = Field(
        default={},
        description="Optional configuration for the analysis"
    )


class AnalysisResponse(BaseModel):
    """Response model for earnings analysis"""
    analysis_id: str
    status: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[list] = None
    processing_time: Optional[float] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    agents_available: list
    version: str


# Global variables for agent management
agents = {}
workflow = None


def initialize_agents():
    """
    Initialize all specialized agents with LLM client.
    Creates instances of coordinator, data extractor, sentiment, and summary agents.

    -- Steve: Task 1 - Agent initialization
    Ensure all 4 agents are properly instantiated with LLM client
    Current status: ✅ COMPLETE
    """
    global agents

    logger.info("Initializing agents...")

    try:
        # -- Steve: Task 1.1 - LLM Client Setup
        # Initialize LLM client (use mock if API key not available)
        use_mock = not os.getenv("ANTHROPIC_API_KEY")

        if use_mock:
            logger.warning("ANTHROPIC_API_KEY not set - using mock LLM client")
            llm_client = MockLLMClient()
        else:
            llm_client = AnthropicLLMClient()

        # -- Steve: Task 1.2 - Agent Creation
        # Create agent instances for each specialization
        agents = {
            'coordinator': CoordinatorAgent(llm_client),      # Orchestrates workflow
            'data_extractor': DataExtractorAgent(llm_client), # Extracts financial metrics
            'sentiment_analyzer': SentimentAnalysisAgent(llm_client), # Analyzes tone/sentiment
            'summary_generator': SummaryAgent(llm_client)     # Generates executive summary
        }

        logger.info(f"Initialized {len(agents)} agents")
        return agents

    except Exception as e:
        logger.error(f"Error initializing agents: {str(e)}")
        raise


def setup_langgraph_workflow():
    """
    Set up LangGraph workflow for agent orchestration.
    Creates the graph that manages data flow between agents.

    -- Steve: Task 2 - LangGraph workflow setup
    Wire up the agents into a state graph with proper sequencing
    Current status: ✅ COMPLETE
    """
    global workflow

    logger.info("Setting up LangGraph workflow...")

    try:
        # -- Steve: Task 2.1 - Workflow Graph Creation
        # Create workflow graph with all agents in proper sequence:
        # Coordinator → Data Extractor → Sentiment Analyzer → Summary Generator
        workflow = WorkflowGraph(
            coordinator_agent=agents['coordinator'],
            data_extractor_agent=agents['data_extractor'],
            sentiment_agent=agents['sentiment_analyzer'],
            summary_agent=agents['summary_generator']
        )

        # -- Steve: Task 2.2 - Workflow Validation
        # Graph is compiled and ready for invocation
        logger.info("LangGraph workflow setup complete")
        return workflow

    except Exception as e:
        logger.error(f"Error setting up workflow: {str(e)}")
        raise


async def process_earnings_report(report_path: str, options: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process an earnings report through the multi-agent system.

    Args:
        report_path: Path to the earnings report file
        options: Processing options

    Returns:
        Analysis results dictionary

    -- Steve: Task 3 - Error handling and retry logic
    Implement production-ready error handling with graceful degradation
    Current status: ✅ COMPLETE (with retry logic in base agents)
    """
    start_time = datetime.now()

    try:
        # -- Steve: Task 3.1 - Input Validation
        # Validate report file exists and is readable
        report_file = Path(report_path)
        if not report_file.exists():
            raise FileNotFoundError(f"Report file not found: {report_path}")

        # -- Steve: Task 3.2 - File Processing
        # Read report content with proper error handling
        with open(report_file, 'r', encoding='utf-8') as f:
            report_content = f.read()

        logger.info(f"Processing report: {report_path}")
        logger.info(f"Report length: {len(report_content)} characters")

        # -- Steve: Task 3.3 - Async Workflow Execution
        # Execute LangGraph workflow with report content
        logger.info("Invoking LangGraph workflow...")
        workflow_result = await workflow.invoke(report_content, options)

        processing_time = (datetime.now() - start_time).total_seconds()

        # -- Steve: Task 3.4 - Result Construction with Error Handling
        # Construct final result, handling missing/partial agent outputs
        result = {
            "analysis_id": f"analysis_{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "processing_time_seconds": processing_time,
            "agents_executed": list(agents.keys()),
            "financial_metrics": workflow_result.get("financial_metrics", {}),
            "segment_performance": workflow_result.get("segment_performance", {}),
            "forward_guidance": workflow_result.get("forward_guidance", {}),
            "sentiment_analysis": workflow_result.get("sentiment_analysis", {}),
            "executive_summary": workflow_result.get("executive_summary", {}),
            "errors": workflow_result.get("errors", [])
        }

        logger.info(f"Report processed successfully in {processing_time:.2f} seconds")
        return result

    except Exception as e:
        logger.error(f"Error processing report: {str(e)}")
        raise


@app.on_event("startup")
async def startup_event():
    """Initialize agents and workflow on application startup"""
    logger.info("Starting Multi-Agent Earnings Analyzer...")
    initialize_agents()
    setup_langgraph_workflow()
    logger.info("Application startup complete")


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Agent Earnings Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        agents_available=list(agents.keys()),
        version="1.0.0"
    )


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_earnings(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Analyze an earnings report using the multi-agent system.
    
    Args:
        request: Analysis request containing report path and options
        
    Returns:
        Analysis response with results or errors
    """
    try:
        # Process the report
        result = await process_earnings_report(
            request.report_path,
            request.options or {}
        )
        
        return AnalysisResponse(
            analysis_id=result.get("analysis_id", "unknown"),
            status="success",
            data=result,
            processing_time=result.get("processing_time_seconds")
        )
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return AnalysisResponse(
            analysis_id=f"error_{datetime.now().timestamp()}",
            status="failed",
            errors=[str(e)]
        )


@app.get("/agents", response_model=Dict[str, Any])
async def list_agents():
    """List all available agents and their status"""
    agent_info = []
    for name, agent in agents.items():
        # TODO: Get actual status from your agents
        agent_info.append({
            "name": name,
            "status": "ready",  # You might want to check agent.status here
            "description": f"Agent: {name}"
        })
    
    return {
        "agents": agent_info,
        "total": len(agents)
    }


# Error handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )
