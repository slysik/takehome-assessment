"""
Tests for the multi-agent system components.

This test suite validates:
- Agent initialization and configuration
- Base agent functionality
- Agent status management
- Input validation
"""

import pytest
from src.agents.base import BaseAgent, AgentStatus, AgentResult, ExampleAgent


class TestBaseAgent:
    """Test suite for the BaseAgent class"""

    @pytest.mark.asyncio
    async def test_example_agent_initialization(self):
        """Test that example agent initializes correctly"""
        agent = ExampleAgent()
        assert agent.name == "example_agent"
        assert agent.status == AgentStatus.READY
        assert isinstance(agent.state, dict)
        assert len(agent.state) == 0

    @pytest.mark.asyncio
    async def test_example_agent_state_management(self):
        """Test agent state update and retrieval"""
        agent = ExampleAgent()

        # Test state update
        agent.update_state("test_key", "test_value")
        assert agent.get_state("test_key") == "test_value"

        # Test state default value
        assert agent.get_state("nonexistent", "default") == "default"

    @pytest.mark.asyncio
    async def test_example_agent_reset(self):
        """Test agent reset functionality"""
        agent = ExampleAgent()

        # Update state
        agent.update_state("key", "value")
        agent.status = AgentStatus.RUNNING

        # Reset
        agent.reset()
        assert agent.status == AgentStatus.READY
        assert len(agent.state) == 0

    @pytest.mark.asyncio
    async def test_example_agent_validate_input_valid(self):
        """Test input validation with valid data"""
        agent = ExampleAgent()
        valid_input = {"key": "value"}
        assert agent.validate_input(valid_input) is True

    @pytest.mark.asyncio
    async def test_example_agent_validate_input_invalid(self):
        """Test input validation with invalid data"""
        agent = ExampleAgent()

        # Test None input
        assert agent.validate_input(None) is False

        # Test non-dict input
        assert agent.validate_input("not a dict") is False
        assert agent.validate_input([1, 2, 3]) is False

    @pytest.mark.asyncio
    async def test_example_agent_process_success(self):
        """Test successful agent processing"""
        agent = ExampleAgent()
        input_data = {"test": "data"}
        context = {}

        result = await agent.process(input_data, context)

        assert isinstance(result, AgentResult)
        assert result.agent_name == "example_agent"
        assert result.status == AgentStatus.SUCCESS
        assert "processed" in result.data

    @pytest.mark.asyncio
    async def test_example_agent_process_invalid_input(self):
        """Test agent processing with invalid input"""
        agent = ExampleAgent()
        invalid_input = None
        context = {}

        result = await agent.process(invalid_input, context)

        assert isinstance(result, AgentResult)
        assert result.status == AgentStatus.FAILED
        assert result.errors is not None
        assert len(result.errors) > 0

    @pytest.mark.asyncio
    async def test_agent_repr(self):
        """Test agent string representation"""
        agent = ExampleAgent()
        repr_str = repr(agent)
        assert "ExampleAgent" in repr_str
        assert "example_agent" in repr_str
        assert "ready" in repr_str


class TestAgentStatus:
    """Test suite for AgentStatus enum"""

    def test_agent_status_values(self):
        """Test that all expected status values exist"""
        assert AgentStatus.READY.value == "ready"
        assert AgentStatus.RUNNING.value == "running"
        assert AgentStatus.SUCCESS.value == "success"
        assert AgentStatus.FAILED.value == "failed"
        assert AgentStatus.RETRY.value == "retry"


class TestAgentResult:
    """Test suite for AgentResult dataclass"""

    def test_agent_result_creation(self):
        """Test AgentResult initialization"""
        result = AgentResult(
            agent_name="test_agent",
            status=AgentStatus.SUCCESS,
            data={"result": "data"}
        )

        assert result.agent_name == "test_agent"
        assert result.status == AgentStatus.SUCCESS
        assert result.data == {"result": "data"}
        assert result.errors is None
        assert result.processing_time == 0.0
        assert result.metadata is None

    def test_agent_result_with_errors(self):
        """Test AgentResult with error information"""
        result = AgentResult(
            agent_name="test_agent",
            status=AgentStatus.FAILED,
            data={},
            errors=["Error message 1", "Error message 2"]
        )

        assert result.status == AgentStatus.FAILED
        assert len(result.errors) == 2
        assert "Error message 1" in result.errors
