#!/bin/bash
# Quick Start Script for Remaining ADW Phases
# Issue #4 | ADW ID: 7b0c1699
# Multi-Agent Earnings Analyzer

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="/Users/slysik/tac/steve"
ISSUE_NUMBER="4"
ADW_ID="7b0c1699"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}ADW Remaining Phases Quick Start${NC}"
echo -e "${BLUE}Issue #$ISSUE_NUMBER | ADW ID: $ADW_ID${NC}"
echo -e "${BLUE}========================================${NC}\n"

# Function to run a phase
run_phase() {
    local phase=$1
    local phase_script=$2
    local phase_num=$3

    echo -e "${YELLOW}=== Phase $phase_num: $phase ===${NC}"
    echo "Running: uv run adws/$phase_script $ISSUE_NUMBER $ADW_ID"
    echo ""

    cd "$PROJECT_ROOT"

    if [ "$phase" == "TEST" ]; then
        uv run "adws/$phase_script" "$ISSUE_NUMBER" "$ADW_ID" --skip-e2e
    else
        uv run "adws/$phase_script" "$ISSUE_NUMBER" "$ADW_ID"
    fi

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $phase phase completed successfully${NC}\n"
        return 0
    else
        echo -e "${RED}❌ $phase phase failed${NC}\n"
        return 1
    fi
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}\n"

# Check environment variables
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}ERROR: ANTHROPIC_API_KEY not set${NC}"
    exit 1
fi
echo -e "${GREEN}✓ ANTHROPIC_API_KEY is set${NC}"

if [ -z "$CLAUDE_CODE_PATH" ]; then
    echo -e "${RED}ERROR: CLAUDE_CODE_PATH not set${NC}"
    exit 1
fi
echo -e "${GREEN}✓ CLAUDE_CODE_PATH is set${NC}"

# Check git status
echo -e "${YELLOW}Checking git status...${NC}"
cd "$PROJECT_ROOT"
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" == *"7b0c1699"* ]]; then
    echo -e "${GREEN}✓ On correct branch: $CURRENT_BRANCH${NC}"
else
    echo -e "${YELLOW}⚠️  Current branch: $CURRENT_BRANCH${NC}"
    echo -e "${YELLOW}   Expected: chore-issue-4-adw-7b0c1699-*${NC}"
fi

echo ""

# Ask which phases to run
echo -e "${BLUE}Which phases would you like to run?${NC}"
echo "1. TEST only (--skip-e2e)"
echo "2. REVIEW only"
echo "3. DOCUMENT only"
echo "4. All remaining phases (TEST → REVIEW → DOCUMENT)"
echo ""
read -p "Select (1-4) [4]: " PHASE_CHOICE
PHASE_CHOICE=${PHASE_CHOICE:-4}

echo ""

case $PHASE_CHOICE in
    1)
        run_phase "TEST" "adw_test.py" "3"
        ;;
    2)
        run_phase "REVIEW" "adw_review.py" "4"
        ;;
    3)
        run_phase "DOCUMENT" "adw_document.py" "5"
        ;;
    4)
        run_phase "TEST" "adw_test.py" "3" && \
        run_phase "REVIEW" "adw_review.py" "4" && \
        run_phase "DOCUMENT" "adw_document.py" "5"

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}========================================${NC}"
            echo -e "${GREEN}✅ ALL PHASES COMPLETED SUCCESSFULLY${NC}"
            echo -e "${GREEN}========================================${NC}"
            echo ""
            echo "Final status:"
            git log --oneline -5
            echo ""
            echo "Branch is ready for PR merge!"
        else
            echo -e "${RED}One or more phases failed${NC}"
            exit 1
        fi
        ;;
    *)
        echo -e "${RED}Invalid selection${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${BLUE}Git log (last 5 commits):${NC}"
cd "$PROJECT_ROOT"
git log --oneline -5
echo ""

echo -e "${BLUE}Current git status:${NC}"
git status --short
echo ""

echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review the generated files:"
echo "   - Check test results"
echo "   - Review auto-fixes (if any)"
echo "   - Check generated documentation"
echo ""
echo "2. Push to remote:"
echo "   git push origin $(git rev-parse --abbrev-ref HEAD)"
echo ""
echo "3. Create/update PR:"
echo "   gh pr create --fill"
echo "   # or update existing:"
echo "   gh pr view --web"
