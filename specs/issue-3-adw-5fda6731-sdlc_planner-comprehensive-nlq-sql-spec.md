# Chore: Create Comprehensive Specification for Natural Language SQL Interface

## Metadata
issue_number: `3`
adw_id: `5fda6731`
issue_json: `{"number":3,"title":"Documentation: Create comprehensive specification for Natural Language SQL Interface","body":"# Natural Language SQL Interface\n\nA web application that converts natural language queries to SQL using AI, built with FastAPI and Vite + TypeScript.\n\n## Features\n\n- 🗣️ Natural language to SQL conversion using OpenAI or Anthropic\n- 📁 Drag-and-drop file upload (.csv and .json)\n- 📊 Interactive table results display\n- 🔒 SQL injection protection\n- ⚡ Fast development with Vite and uv\n\n## Prerequisites\n\n- Python 3.10+\n- uv (Python package manager)\n- Node.js 18+\n- Bun (or your preferred npm tool: npm, yarn, etc.)\n- OpenAI API key and/or Anthropic API key\n\n## Setup\n\n### 1. Install Dependencies\n\n```bash\n# Backend\ncd app/server\nuv sync --all-extras\n\n# Frontend\ncd app/client\nbun install\n```\n\n### 2. Environment Configuration\n\nSet up your API keys in the server directory:\n\n```bash\ncd app/server\ncp .env.sample .env\n# Edit .env and add your API keys\n```\n\n## Quick Start\n\nUse the provided script to start both services:\n\n```bash\n./scripts/start.sh\n```\n\nPress `Ctrl+C` to stop both services.\n\nThe script will:\n- Check that `.env` exists in `app/server/`\n- Start the backend on http://localhost:8000\n- Start the frontend on http://localhost:5173\n- Handle graceful shutdown when you exit\n\n## Manual Start (Alternative)\n\n### Backend\n```bash\ncd app/server\n# .env is loaded automatically by python-dotenv\nuv run python server.py\n```\n\n### Frontend\n```bash\ncd app/client\nbun run dev\n```\n\n## Usage\n\n1. **Upload Data**: Click \"Upload Data\" to open the modal\n   - Use sample data buttons for quick testing\n   - Or drag and drop your own .csv or .json files\n   - Uploading a file with the same name will overwrite the existing table\n2. **Query Your Data**: Type a natural language query like \"Show me all users who signed up last week\"\n   - Press `Cmd+Enter` (Mac) or `Ctrl+Enter` (Windows/Linux) to run the query\n3. **View Results**: See the generated SQL and results in a table format\n4. **Manage Tables**: Click the × button on any table to remove it\n\n## Development\n\n### Backend Commands\n```bash\ncd app/server\nuv run python server.py      # Start server with hot reload\nuv run pytest               # Run tests\nuv add <package>            # Add package to project\nuv remove <package>         # Remove package from project\nuv sync --all-extras        # Sync all extras\n```\n\n### Frontend Commands\n```bash\ncd app/client\nbun run dev                 # Start dev server\nbun run build              # Build for production\nbun run preview            # Preview production build\n```\n\n## Project Structure\n\n```\n.\n├── app/                    # Main application\n│   ├── client/             # Vite + TypeScript frontend\n│   └── server/             # FastAPI backend\n│\n├── adws/                   # AI Developer Workflow (ADW) - GitHub issue automation system\n├── scripts/                # Utility scripts (start.sh, stop_apps.sh)\n├── specs/                  # Feature specifications\n├── ai_docs/                # AI/LLM documentation\n├── agents/                 # Agent execution logging\n└── logs/                   # Structured session logs\n```\n\n## API Endpoints\n\n- `POST /api/upload` - Upload CSV/JSON file\n- `POST /api/query` - Process natural language query\n- `GET /api/schema` - Get database schema\n- `POST /api/insights` - Generate column insights\n- `GET /api/health` - Health check\n\n## Security\n\n### SQL Injection Protection\n\nThe application implements comprehensive SQL injection protection through multiple layers:\n\n1. **Centralized Security Module** (`core/sql_security.py`):\n   - Identifier validation for table and column names\n   - Safe query execution with parameterized queries\n   - Proper escaping for identifiers using SQLite's square bracket notation\n   - Dangerous operation detection and blocking\n\n2. **Input Validation**:\n   - All table and column names are validated against a whitelist pattern\n   - SQL keywords cannot be used as identifiers\n   - File names are sanitized before creating tables\n   - User queries are validated for dangerous operations\n\n3. **Query Execution Safety**:\n   - Parameterized queries used wherever possible\n   - Identifiers (table/column names) are properly escaped\n   - Multiple statement execution is blocked\n   - SQL comments are not allowed in queries\n\n4. **Protected Operations**:\n   - File uploads with malicious names are sanitized\n   - Natural language queries cannot inject SQL\n   - Table deletion uses validated identifiers\n   - Data insights generation validates all inputs\n\n### Security Best Practices for Development\n\nWhen adding new SQL functionality:\n1. Always use the `sql_security` module functions\n2. Never concatenate user input directly into SQL strings\n3. Use `execute_query_safely()` for all database operations\n4. Validate all identifiers with `validate_identifier()`\n5. For DDL operations, use `allow_ddl=True` explicitly\n\n### Testing Security\n\nRun the comprehensive security tests:\n```bash\ncd app/server\nuv run pytest tests/test_sql_injection.py -v\n```\n\n\n### Additional Security Features\n\n- CORS configured for local development only\n- File upload validation (CSV and JSON only)\n- Comprehensive error logging without exposing sensitive data\n- Database operations are isolated with proper connection handling\n\n## AI Developer Workflow (ADW)\n\nThe ADW system is a comprehensive automation framework that integrates GitHub issues with Claude Code CLI to classify issues, generate implementation plans, and automatically create pull requests. ADW processes GitHub issues by classifying them as `/chore`, `/bug`, or `/feature` commands and then implementing solutions autonomously.\n\n### Prerequisites\n\nBefore using ADW, ensure you have the following installed and configured:\n\n- **GitHub CLI**: `brew install gh` (macOS) or equivalent for your OS\n- **Claude Code CLI**: Install from [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)\n- **Python with uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`\n- **GitHub authentication**: `gh auth login`\n\n### Environment Variables\n\nSet these environment variables before running ADW:\n\n```bash\nexport GITHUB_REPO_URL=\"https://github.com/owner/repository\"\nexport ANTHROPIC_API_KEY=\"sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\"\nexport CLAUDE_CODE_PATH=\"/path/to/claude\"  # Optional, defaults to \"claude\"\nexport GITHUB_PAT=\"ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\"  # Optional, only if using different account than 'gh auth login'\n```\n\n### Usage Modes\n\nADW supports three main operation modes:\n\n#### 1. Manual Processing\nProcess a single GitHub issue manually:\n```bash\ncd adws/\nuv run adw_plan_build.py <issue-number>\n```\n\n#### 2. Automated Monitoring\nContinuously monitor GitHub for new issues (polls every 20 seconds):\n```bash\ncd adws/\nuv run trigger_cron.py\n```\n\n#### 3. Webhook Server\nStart a webhook server for real-time GitHub event processing:\n```bash\ncd adws/\nuv run trigger_webhook.py\n```\n\n### How ADW Works\n\n1. **Issue Classification**: Analyzes GitHub issues and determines type (`/chore`, `/bug`, `/feature`)\n2. **Planning**: Generates detailed implementation plans using Claude Code CLI\n3. **Implementation**: Executes the plan by making code changes, running tests, and ensuring quality\n4. **Integration**: Creates git commits and pull requests with semantic commit messages\n\n### For More Information\n\nFor detailed technical documentation, configuration options, and troubleshooting, see [`adws/README.md`](adws/README.md).\n\n## Troubleshooting\n\n**Backend won't start:**\n- Check Python version: `python --version` (requires 3.12+)\n- Verify API keys are set: `echo $OPENAI_API_KEY`\n\n**Frontend errors:**\n- Clear node_modules: `rm -rf node_modules && bun install`\n- Check Node version: `node --version` (requires 18+)\n\n**CORS issues:**\n- Ensure backend is running on port 8000\n- Check vite.config.ts proxy settings# multi-agent-workflow-company-earnings"}`

## Chore Description

The GitHub issue requests creation of comprehensive documentation for a "Natural Language SQL Interface". However, after analyzing the codebase, the actual application in `app/client/` is a **Multi-Agent Earnings Analyzer** system, not a Natural Language SQL Interface.

**Discrepancy Identified:**
- The root `README.md` describes a Natural Language SQL Interface with CSV/JSON upload and SQL query capabilities
- The actual `app/client/` implementation is a multi-agent LangGraph system for analyzing company earnings reports
- The existing `specs/readme-specification.md` already contains comprehensive documentation for the described SQL interface

**Chore Objective:**
This chore will reconcile this documentation discrepancy by:
1. Creating a comprehensive specification that accurately documents the **actual** application (Multi-Agent Earnings Analyzer)
2. Updating the root `README.md` to correctly describe the actual application
3. Archiving or removing the outdated `specs/readme-specification.md` that describes a different application
4. Creating new comprehensive documentation in `specs/` that matches the real codebase

## Relevant Files

### Existing Documentation (To Be Updated/Archived)
- `README.md` - Root project README describing incorrect application (Natural Language SQL Interface)
  - **Why relevant**: Contains incorrect description that must be updated to match actual application
- `specs/readme-specification.md` - Comprehensive spec for non-existent Natural Language SQL Interface
  - **Why relevant**: This 799-line specification documents an application that doesn't exist in the codebase and should be archived

### Actual Application Files (To Be Documented)
- `app/client/README.md` - Current README for Multi-Agent Earnings Analyzer
  - **Why relevant**: Contains correct description of actual application architecture
- `app/client/src/main.py` - FastAPI application entry point
  - **Why relevant**: Defines API endpoints and application structure
- `app/client/src/agents/*.py` - Agent implementations (coordinator, data_extractor, sentiment, summary, base)
  - **Why relevant**: Core functionality of the multi-agent system
- `app/client/src/workflow/graph.py` - LangGraph workflow orchestration
  - **Why relevant**: Defines how agents work together
- `app/client/src/llm_client.py` - LLM client wrapper
  - **Why relevant**: Integration with Anthropic Claude API
- `app/client/Dockerfile` - Container configuration
  - **Why relevant**: Deployment and production setup
- `app/client/docker-compose.yml` - Docker Compose setup
  - **Why relevant**: Service orchestration
- `app/client/run.sh` - Startup script
  - **Why relevant**: Application bootstrap process
- `app/client/data/earnings_report_sample.txt` - Sample earnings report
  - **Why relevant**: Example input data format
- `app/client/data/expected_output.json` - Expected analysis output
  - **Why relevant**: Output format specification

### New Files

- `specs/issue-3-adw-5fda6731-comprehensive-earnings-analyzer-spec.md` - New comprehensive specification for the actual Multi-Agent Earnings Analyzer application
- `specs/archive/readme-specification-archived.md` - Archived outdated specification for reference

## Step by Step Tasks

IMPORTANT: Execute every step in order, top to bottom.

### Step 1: Analyze Current Application Architecture
- Read all agent implementation files in `app/client/src/agents/` to understand functionality
- Read `app/client/src/workflow/graph.py` to understand LangGraph orchestration
- Read `app/client/src/main.py` to understand API structure and endpoints
- Read `app/client/src/llm_client.py` to understand LLM integration
- Read sample data files to understand input/output formats
- Document the complete agent workflow and data flow

### Step 2: Create Comprehensive Specification
- Create `specs/issue-3-adw-5fda6731-comprehensive-earnings-analyzer-spec.md`
- Include sections for:
  - **Project Overview**: Title, purpose, key features, target users
  - **Architecture & Design**: System components diagram, agent roles, technology stack, design patterns, data models
  - **Implementation Requirements**: Core features with acceptance criteria for each agent, API specifications, agent interactions
  - **Dependencies and Prerequisites**: System requirements, external APIs (Anthropic), development tools
  - **Integration Points**: Agent-to-agent communication, LangGraph state management, LLM provider integration
  - **API Specifications**: Detailed documentation of all FastAPI endpoints with request/response examples
  - **Development Phases**: Phased implementation plan for building the system
  - **Testing Strategy**: Unit testing approach (per agent), integration testing, E2E scenarios, performance benchmarks
  - **Success Criteria**: Definition of done, performance benchmarks, quality metrics, user acceptance criteria
  - **Known Risks & Mitigation**: Technical risks (LLM failures, agent coordination), scheduling risks, mitigation strategies
  - **References**: Framework documentation, LangGraph docs, Anthropic API docs, related projects
  - **Appendices**: Directory structure, environment variables, agent prompt templates, sample workflows
- Ensure specification is production-ready and implementation-focused

### Step 3: Archive Outdated Specification
- Create directory `specs/archive/` if it doesn't exist
- Move `specs/readme-specification.md` to `specs/archive/readme-specification-archived.md`
- Add header note to archived file explaining it documents a different application
- Update any references to the archived specification in other documentation

### Step 4: Update Root README
- Replace content in `README.md` with accurate description of Multi-Agent Earnings Analyzer
- Use content from `app/client/README.md` as foundation
- Add enhanced sections for:
  - Clear project title and description
  - Architecture overview with agent descriptions
  - Quick start guide
  - API documentation
  - Development workflow
  - Production considerations
  - Link to comprehensive specification in `specs/`
- Remove all references to "Natural Language SQL Interface", CSV/JSON upload, SQL queries, etc.
- Ensure ADW section remains intact

### Step 5: Enhance Application-Level Documentation
- Review and enhance `app/client/README.md` if needed for consistency
- Ensure it references the comprehensive specification
- Add any missing production deployment details
- Verify all instructions are accurate and tested

### Step 6: Validate Documentation Accuracy
- Cross-reference all documented features with actual code implementation
- Verify all API endpoints mentioned in docs exist in `app/client/src/main.py`
- Verify all agent descriptions match implementation in `app/client/src/agents/`
- Check that all configuration examples match actual `.env.example`
- Ensure all commands and scripts referenced actually exist and work

## Validation Commands

Execute every command to validate the chore is complete with zero regressions.

- `cd app/client && cat README.md | grep -i "earnings"` - Verify client README describes earnings analyzer
- `cd app/client && cat README.md | grep -i "sql"` - Verify no SQL references in client README (should be empty)
- `cat README.md | grep -i "earnings"` - Verify root README describes earnings analyzer
- `cat README.md | grep -i "natural language sql"` - Verify no Natural Language SQL references in root README (should be empty)
- `test -f specs/issue-3-adw-5fda6731-comprehensive-earnings-analyzer-spec.md` - Verify new spec exists
- `test -f specs/archive/readme-specification-archived.md` - Verify old spec is archived
- `cat specs/issue-3-adw-5fda6731-comprehensive-earnings-analyzer-spec.md | wc -l` - Verify new spec is comprehensive (should be 500+ lines)
- `grep -r "Natural Language SQL Interface" README.md` - Verify no outdated references (should be empty)
- `grep -r "CSV.*JSON.*upload" README.md | grep -v "ADW"` - Verify no CSV/JSON upload references outside ADW section (should be empty)

## Notes

### Critical Observations

1. **Documentation-Code Mismatch**: The root README and the existing specification in `specs/readme-specification.md` describe an entirely different application (Natural Language SQL Interface with SQL query generation) than what's actually implemented (Multi-Agent Earnings Analyzer with LangGraph).

2. **Actual Application**: The real application in `app/client/` is a sophisticated multi-agent system using:
   - LangGraph for workflow orchestration
   - Multiple specialized agents (Coordinator, Data Extractor, Sentiment Analyzer, Summary Generator)
   - Anthropic Claude API for LLM capabilities
   - FastAPI for REST API
   - Docker containerization

3. **Specification Quality**: The new specification must be:
   - Accurate to the actual codebase
   - Comprehensive enough for implementation and maintenance
   - Production-ready with security, monitoring, and scaling considerations
   - Well-structured with clear sections and acceptance criteria

4. **Preserving ADW Documentation**: The ADW (AI Developer Workflow) system documentation in the README is correct and should be preserved as-is during the update.

### Documentation Standards

Follow these standards when creating the specification:
- Use markdown formatting consistent with existing specs
- Include code examples where helpful
- Provide clear acceptance criteria for each feature
- Document both happy path and error scenarios
- Include performance benchmarks and testing strategies
- Reference actual file paths and code locations
- Use diagrams (ASCII art) where helpful for architecture
- Keep language clear, technical, and implementation-focused
