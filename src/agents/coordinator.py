"""
Coordinator Agent

Orchestrates the multi-agent workflow for earnings analysis.
Validates inputs and coordinates execution across specialized agents.
"""

from typing import Dict, Any
from .base import BaseAgent, AgentResult, AgentStatus
import logging

logger = logging.getLogger(__name__)


class CoordinatorAgent(BaseAgent):
    """
    Coordinates the earnings analysis workflow across multiple agents.

    Responsibilities:
    - Validate input report data
    - Initialize workflow state
    - Coordinate agent execution order
    - Aggregate results from all agents
    """

    def __init__(self, llm_client=None):
        """
        Initialize the coordinator agent.

        Args:
            llm_client: Optional LLM client for advanced coordination logic
        """
        super().__init__(name="coordinator")
        self.llm_client = llm_client
        self.registered_agents = {}

    def register_agent(self, agent_name: str, agent: BaseAgent) -> None:
        """
        Register an agent with the coordinator.

        Args:
            agent_name: Name to register the agent under
            agent: Agent instance to register
        """
        self.registered_agents[agent_name] = agent
        logger.info(f"Registered agent: {agent_name}")

    def validate_input(self, input_data: Any) -> bool:
        """
        Validate that input contains a valid report path or content.

        Args:
            input_data: Input to validate

        Returns:
            True if valid, False otherwise
        """
        if not super().validate_input(input_data):
            return False

        # Check for either report_path or report_content
        has_path = "report_path" in input_data
        has_content = "report_content" in input_data

        return has_path or has_content

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Execute coordination logic.

        Args:
            input_data: Contains report_path or report_content
            context: Shared workflow context

        Returns:
            AgentResult with coordination instructions
        """
        try:
            # Extract report content
            if "report_content" in input_data:
                report_content = input_data["report_content"]
            elif "report_path" in input_data:
                # Read report from file
                report_path = input_data["report_path"]
                try:
                    with open(report_path, 'r') as f:
                        report_content = f.read()
                except Exception as e:
                    return AgentResult(
                        agent_name=self.name,
                        status=AgentStatus.FAILED,
                        data={},
                        errors=[f"Failed to read report file: {str(e)}"]
                    )
            else:
                return AgentResult(
                    agent_name=self.name,
                    status=AgentStatus.FAILED,
                    data={},
                    errors=["No report_path or report_content provided"]
                )

            # Store report content in context for other agents
            context["report_content"] = report_content
            context["workflow_initiated_by"] = self.name

            # Prepare workflow execution plan
            execution_plan = {
                "agents_to_execute": [
                    "data_extractor",
                    "sentiment_analyzer",
                    "summary_generator"
                ],
                "report_length": len(report_content),
                "initialized_at": context.get("timestamp", "unknown")
            }

            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.SUCCESS,
                data={
                    "coordination_status": "ready",
                    "execution_plan": execution_plan
                }
            )

        except Exception as e:
            logger.exception(f"Error in {self.name}")
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                data={},
                errors=[f"Coordination error: {str(e)}"]
            )
