#!/bin/bash
set -e

# Color definitions
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo -e "${GREEN}Activating virtual environment...${NC}"
    source venv/bin/activate
fi

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -r requirements-dev.txt

# Create directory for test outputs
mkdir -p test-reports

# Run style checks
echo -e "${GREEN}Running style checks...${NC}"
if command -v black &> /dev/null; then
    echo -e "${YELLOW}Running black...${NC}"
    black --check app tests || echo -e "${RED}Black check failed, but continuing...${NC}"
fi

if command -v flake8 &> /dev/null; then
    echo -e "${YELLOW}Running flake8...${NC}"
    flake8 app tests || echo -e "${RED}Flake8 check failed, but continuing...${NC}"
fi

if command -v isort &> /dev/null; then
    echo -e "${YELLOW}Running isort...${NC}"
    isort --check app tests || echo -e "${RED}isort check failed, but continuing...${NC}"
fi

# Run tests
echo -e "${GREEN}Running tests with coverage...${NC}"
pytest --cov=app tests/ --cov-report=term --cov-report=html:test-reports/coverage

# Print test summary
echo -e "${GREEN}Tests completed!${NC}"
echo -e "${YELLOW}Coverage report saved to test-reports/coverage${NC}"
echo -e "${YELLOW}View the HTML report by opening test-reports/coverage/index.html${NC}"

# Optional: Run performance tests if flag is provided
if [ "$1" == "--perf" ]; then
    echo -e "${GREEN}Running performance tests...${NC}"
    pytest tests/test_performance.py -v
fi