#!/bin/bash

# Demo Script for Self-Healing CI/CD Agent
# This script demonstrates the agent's capabilities

set -e

echo "🤖 Self-Healing CI/CD Agent Demo"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if agent is running
echo -e "${BLUE}Checking if agent is running...${NC}"
if curl -s http://localhost:8000/health > /dev/null; then
    echo -e "${GREEN}✓ Agent is running${NC}"
else
    echo -e "${YELLOW}⚠ Agent is not running. Start it with: cd agent-core && python main.py${NC}"
    exit 1
fi

# Check if dashboard is accessible
echo -e "${BLUE}Checking if dashboard is accessible...${NC}"
if curl -s http://localhost:3000 > /dev/null; then
    echo -e "${GREEN}✓ Dashboard is accessible${NC}"
else
    echo -e "${YELLOW}⚠ Dashboard is not running. Start it with: cd dashboard && npm run dev${NC}"
fi

echo ""
echo -e "${BLUE}Fetching current statistics...${NC}"
curl -s http://localhost:8000/api/v1/stats | python -m json.tool

echo ""
echo -e "${BLUE}Recent pipelines:${NC}"
curl -s http://localhost:8000/api/v1/pipelines?limit=5 | python -m json.tool

echo ""
echo -e "${BLUE}Recent failures:${NC}"
curl -s http://localhost:8000/api/v1/failures?limit=5 | python -m json.tool

echo ""
echo -e "${BLUE}Applied fixes:${NC}"
curl -s http://localhost:8000/api/v1/fixes?limit=5 | python -m json.tool

echo ""
echo "================================"
echo -e "${GREEN}Demo complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Open dashboard: http://localhost:3000"
echo "2. Trigger a test failure in your repository"
echo "3. Watch the agent detect and fix it automatically"
echo "4. Check the dashboard for results"
echo ""
echo "For test scenarios, see: examples/test-scenarios.md"
