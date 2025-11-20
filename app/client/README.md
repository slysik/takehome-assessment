# Multi-Agent Earnings Analyzer

A production-ready multi-agent system for analyzing company earnings reports using LangGraph and Claude AI.

## Overview

This application demonstrates a sophisticated multi-agent orchestration system that processes quarterly earnings reports using specialized AI agents working in coordination. Each agent has a specific role in analyzing financial documents and producing actionable insights.

## Architecture

### Agent System

The system consists of four specialized agents:

- **Coordinator Agent**: Orchestrates the workflow and manages state between agents
- **Data Extractor Agent**: Extracts key financial metrics (revenue, profit, EPS, etc.)
- **Sentiment Analysis Agent**: Analyzes management commentary and identifies sentiment
- **Summary Agent**: Consolidates findings and produces executive summaries

### Technology Stack

- **LangGraph**: Multi-agent orchestration and state management
- **Claude AI (Anthropic)**: Language model for analysis tasks
- **FastAPI**: REST API framework
- **Pydantic**: Data validation
- **Docker**: Containerization for production deployment

## Project Structure

```
.
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── __init__.py
│   │   ├── base.py          # Base agent class
│   │   ├── coordinator.py   # Coordinator agent
│   │   ├── data_extractor.py
│   │   ├── sentiment.py
│   │   └── summary.py
│   ├── workflow/            # LangGraph workflow
│   │   └── graph.py
│   ├── llm_client.py        # LLM client wrapper
│   └── main.py              # FastAPI application
├── data/                    # Sample data
│   ├── earnings_report_sample.txt
│   └── expected_output.json
├── Dockerfile              # Container configuration
├── docker-compose.yml      # Docker Compose setup
├── requirements.txt        # Python dependencies
├── run.sh                  # Startup script
└── .env.example            # Environment variable template
```

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- Anthropic API key

### Using Docker (Recommended)

```bash
# Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Build and run with the provided script
bash run.sh
```

The application will be available at `http://localhost:8000`

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ANTHROPIC_API_KEY="your-api-key"

# Run locally
python -m uvicorn src.main:app --reload
```

## API Endpoints

### Health Check
```bash
GET /health
```

### Analyze Earnings Report
```bash
POST /analyze
Content-Type: application/json

{
  "report_path": "/app/data/earnings_report_sample.txt",
  "options": {}
}
```

### List Agents
```bash
GET /agents
```

### Root Endpoint
```bash
GET /
```

## API Documentation

Interactive API documentation available at `http://localhost:8000/docs` when the server is running.

## Configuration

Environment variables:

- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 0.0.0.0)

## Development

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
ruff format src/

# Lint
ruff check src/
```

## Production Considerations

### Scaling
- Implement request queueing for high-volume scenarios
- Use worker pools for parallel processing
- Add caching layer for common analysis patterns

### Monitoring
- Implement structured logging for all agent activities
- Track LLM API usage and costs
- Monitor agent performance metrics

### Security
- Validate and sanitize all input data
- Implement rate limiting on API endpoints
- Use API key management service for credentials
- Encrypt sensitive financial data at rest

### Cost Optimization
- Batch multiple reports for analysis
- Implement prompt caching for repeated patterns
- Monitor token usage and optimize prompts
- Use model-appropriate for task complexity

## Troubleshooting

### Docker BuildKit Issues

If you encounter Docker BuildKit permission errors:

```bash
DOCKER_BUILDKIT=0 docker build -t earnings-analyzer:latest .
```

### Import Errors

Ensure `PYTHONPATH` is set correctly. The Dockerfile includes:
```
ENV PYTHONPATH=/app
```

### Health Check Timeout

The health check may timeout on first startup while agents initialize. This is normal. Check logs:

```bash
docker logs earnings-analyzer
```

## Future Enhancements

- Add persistence layer for analysis results
- Implement agent memory/learning capabilities
- Add more specialized agents (risk analysis, competitive analysis)
- Support multiple document formats (PDF, DOCX)
- Implement long-running job processing with webhooks
- Add audit trail and compliance features

## License

This project is provided as-is for evaluation purposes.

## Support

For issues or questions, refer to the logs and API documentation at `/docs` endpoint.
