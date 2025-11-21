"""
Base Agent Module

Defines the foundational agent classes and types for the multi-agent system.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Enumeration of possible agent states"""
    READY = "ready"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRY = "retry"


@dataclass
class AgentResult:
    """Result data structure returned by agent processing"""
    agent_name: str
    status: AgentStatus
    data: Dict[str, Any]
    errors: Optional[List[str]] = None
    processing_time: float = 0.0
    metadata: Optional[Dict[str, Any]] = None


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the system.

    Provides common functionality for state management, input validation,
    and lifecycle operations.
    """

    def __init__(self, name: str):
        """
        Initialize the base agent.

        Args:
            name: Unique identifier for this agent
        """
        self.name = name
        self.status = AgentStatus.READY
        self.state: Dict[str, Any] = {}
        self.logger = logging.getLogger(f"{__name__}.{name}")

    def update_state(self, key: str, value: Any) -> None:
        """Update a single state value"""
        self.state[key] = value

    def get_state(self, key: str, default: Any = None) -> Any:
        """Get a state value with optional default"""
        return self.state.get(key, default)

    def reset(self) -> None:
        """Reset the agent to initial state"""
        self.status = AgentStatus.READY
        self.state = {}

    def validate_input(self, input_data: Any) -> bool:
        """
        Validate input data before processing.

        Args:
            input_data: Data to validate

        Returns:
            True if valid, False otherwise
        """
        # Default implementation: check if input is a dict
        if input_data is None:
            return False
        if not isinstance(input_data, dict):
            return False
        return True

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Execute the agent's core logic.

        This method must be implemented by subclasses.

        Args:
            input_data: Input data to process
            context: Shared context from workflow

        Returns:
            AgentResult containing processing results
        """
        pass

    async def process(self, input_data: Any, context: Dict[str, Any]) -> AgentResult:
        """
        Main processing entry point with validation and error handling.

        Args:
            input_data: Input data to process
            context: Shared context from workflow

        Returns:
            AgentResult with processing results or errors
        """
        # Validate input
        if not self.validate_input(input_data):
            error_msg = f"Invalid input data for {self.name}"
            self.logger.error(error_msg)
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                data={},
                errors=[error_msg]
            )

        # Update status
        self.status = AgentStatus.RUNNING

        try:
            # Execute the agent logic
            result = await self.execute(input_data, context)
            self.status = result.status
            return result
        except Exception as e:
            self.logger.exception(f"Error in {self.name}")
            self.status = AgentStatus.FAILED
            return AgentResult(
                agent_name=self.name,
                status=AgentStatus.FAILED,
                data={},
                errors=[str(e)]
            )

    def __repr__(self) -> str:
        """String representation of the agent"""
        return f"{self.__class__.__name__}(name='{self.name}', status='{self.status.value}')"


class ExampleAgent(BaseAgent):
    """
    Example agent implementation for testing and demonstration.
    """

    def __init__(self):
        super().__init__(name="example_agent")

    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> AgentResult:
        """
        Execute example processing logic.

        Args:
            input_data: Input data to process
            context: Shared context

        Returns:
            AgentResult with processed data
        """
        # Simple processing: echo back the input with a "processed" flag
        processed_data = {
            "processed": True,
            "input": input_data,
            "agent": self.name
        }

        return AgentResult(
            agent_name=self.name,
            status=AgentStatus.SUCCESS,
            data=processed_data
        )
