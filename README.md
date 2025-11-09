# Empire Automation

AI agent automation system for executing "The Empire Builder's Textbook" - a comprehensive business implementation plan for building a $10M+ multi-entity business empire.

## Overview

This project implements a multi-agent system that automates the execution of a 90-day business launch plan, managing three revenue engines (Professional Services, Directory Empire, and Business Acquisitions) through intelligent orchestration and domain-specific agents.

## Architecture

### Core Components

- **Master Orchestrator**: Strategic coordinator managing the 90-day plan execution
- **Domain Agents**: Specialized agents for each business domain
  - Entity Management Agent
  - Credential Acquisition Agent
  - Professional Services Agent
  - Directory Empire Agent
  - Marketing & Lead Generation Agent
  - Financial Operations Agent
  - Client Success Agent

### Key Features

- **Hybrid Critical-Chain Architecture**: Sequential execution for Days 1-30, parallel execution for Days 31-90
- **Dependency-Weighted Risk Prioritization**: Intelligent task prioritization based on financial impact and downstream dependencies
- **Quadratic Growth Modeling**: Financial trajectory tracking with 45-day revenue recognition lag
- **Domain-Constrained Asset Linkage**: Content-aware matching of tasks to reusable assets

## Project Structure

```
empire-automation/
├── empire_automation/
│   ├── agents/              # Base agent classes
│   ├── orchestrator/        # Master orchestrator implementation
│   ├── domain_agents/       # Domain-specific agent implementations
│   ├── utils/               # Utility functions and helpers
│   ├── config/              # Configuration management
│   ├── models/              # Data models and schemas
│   ├── api/                 # FastAPI REST API
│   └── database/            # Database models and migrations
├── tests/                   # Test suite
├── docs/                    # Documentation
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Poetry configuration
└── README.md               # This file
```

## Setup

### Prerequisites

- Python 3.10+
- Poetry (for dependency management)
- Redis (for Celery task queue)
- SQLite (default database, can be configured for PostgreSQL)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd empire-automation
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
# OR using Poetry:
poetry install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

5. Initialize database:
```bash
# Run database migrations (when implemented)
python -m empire_automation.database.init_db
```

## Configuration

Copy `.env.example` to `.env` and configure:

- `ANTHROPIC_API_KEY`: Your Anthropic API key for Claude
- `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET`: Google API credentials
- `SUITEDASH_API_KEY`: SuiteDash CRM API key
- `QUICKBOOKS_API_KEY`: QuickBooks API key
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection URL for Celery

## Usage

### Running the Orchestrator

```bash
python -m empire_automation.orchestrator.main
```

### Running the API Server

```bash
uvicorn empire_automation.api.main:app --reload
```

### Running Celery Worker

```bash
celery -A empire_automation.celery_app worker --loglevel=info
```

### Running Streamlit Dashboard

```bash
streamlit run empire_automation/dashboard/app.py
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black empire_automation/
isort empire_automation/
```

## Key Discoveries Implemented

1. **Hybrid Critical-Chain Architecture**: Sequential foundation phase (Days 1-30) transitions to parallel scaling phase (Days 31-90)
2. **Quadratic Growth Dynamics**: Directory Empire revenue follows quadratic curve with 45-day recognition lag
3. **Human-in-the-Loop Orchestration**: Credential timing, workload concentration, and risk prioritization
4. **Domain-Constrained Asset Linkage**: Content-aware matching with domain-first approach

## License

Proprietary - All rights reserved

## Author

Empire Builder

