#!/bin/bash

# Multi-Agent Earnings Analyzer - Run Script
# This script demonstrates the complete solution working end-to-end

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================"
echo "Multi-Agent Earnings Analyzer"
echo "======================================"
echo ""

# Check prerequisites
echo -e "${BLUE}Checking prerequisites...${NC}"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker not found. Please install Docker.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker found${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}Please update .env with your ANTHROPIC_API_KEY${NC}"
fi

echo ""
echo -e "${BLUE}Building Docker image...${NC}"
# Use BuildKit for better performance
DOCKER_BUILDKIT=1 docker build -t earnings-analyzer:latest .

echo ""
echo -e "${BLUE}Starting Docker container...${NC}"
DOCKER_BUILDKIT=1 docker-compose up -d

echo ""
echo -e "${GREEN}✓ Container started${NC}"
echo "  Application available at: http://localhost:8000"
echo "  API documentation at: http://localhost:8000/docs"
echo "  Health check endpoint: http://localhost:8000/health"

# Wait for container to be healthy
echo ""
echo -e "${BLUE}Waiting for container to be healthy...${NC}"
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
    if docker exec earnings-analyzer python -c "import requests; requests.get('http://localhost:8000/health')" 2>/dev/null; then
        echo -e "${GREEN}✓ Container is healthy${NC}"
        break
    fi
    attempt=$((attempt + 1))
    echo -n "."
    sleep 1
done

if [ $attempt -eq $max_attempts ]; then
    echo -e "${YELLOW}⚠️  Container health check timed out${NC}"
fi

echo ""
echo -e "${BLUE}Testing the analysis endpoint...${NC}"

# Test with sample earnings report
TEST_RESPONSE=$(curl -s -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"report_path": "/app/data/earnings_report_sample.txt"}')

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Analysis request successful${NC}"
    echo ""
    echo "Response:"
    echo "$TEST_RESPONSE" | python -m json.tool
else
    echo -e "${YELLOW}⚠️  Analysis request failed${NC}"
fi

echo ""
echo "======================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "======================================"
echo ""
echo "Available endpoints:"
echo "  GET  http://localhost:8000/              - Root endpoint"
echo "  GET  http://localhost:8000/health        - Health check"
echo "  GET  http://localhost:8000/agents        - List available agents"
echo "  POST http://localhost:8000/analyze       - Analyze earnings report"
echo ""
echo "Next steps:"
echo "  1. View logs: docker logs earnings-analyzer"
echo "  2. Interactive API docs: http://localhost:8000/docs"
echo "  3. Stop container: docker-compose down"
echo ""
