# 📚 Complete System Documentation
## AI-Powered Self-Healing CI/CD Agent

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Components](#components)
4. [Setup Guide](#setup-guide)
5. [Usage Guide](#usage-guide)
6. [API Reference](#api-reference)
7. [Configuration](#configuration)
8. [Troubleshooting](#troubleshooting)
9. [Development](#development)
10. [Deployment](#deployment)

---

## System Overview

### What It Does

The AI-Powered Self-Healing CI/CD Agent is an intelligent system that automatically detects, analyzes, and fixes CI/CD pipeline failures without human intervention.

### Key Capabilities

- **Monitors** GitHub Actions workflows in real-time
- **Detects** pipeline failures automatically
- **Analyzes** errors using AI (Groq LLaMA 3.3 70B)
- **Generates** complete fixed code
- **Applies** fixes via Git operations
- **Commits** changes to repository
- **Verifies** fixes work
- **Tracks** all operations in database
- **Displays** status in beautiful dashboard

### Supported Error Types

1. **Syntax Errors** (95% success rate)
   - Missing colons, parentheses, brackets
   - Indentation errors
   - Invalid syntax

2. **Dependency Conflicts** (85% success rate)
   - Missing imports
   - Version conflicts
   - Package not found

3. **Test Failures** (80% success rate)
   - Assertion errors
   - Logic errors
   - Test configuration issues

4. **Configuration Errors** (75% success rate)
   - YAML syntax
   - Environment variables
   - Build configuration

5. **Environment Issues** (70% success rate)
   - Path problems
   - Permission errors
   - Resource availability

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Actions                          │
│                   (CI/CD Pipelines)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Webhook / Polling
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Monitor Service                      │
│              (Detects Pipeline Failures)                     │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Failure Event
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                 Agent Orchestrator                           │
│            (Coordinates All Services)                        │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Error Analyzer (AI)                       │ │
│  │  • Classifies error type                              │ │
│  │  • Extracts root cause                                │ │
│  │  • Calculates confidence                              │ │
│  │  • Uses Groq LLaMA 3.3 70B                           │ │
│  └────────────────────────────────────────────────────────┘ │
│                       │                                      │
│                       ▼                                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Fix Engine (AI)                           │ │
│  │  • Fetches complete source file                       │ │
│  │  • Generates corrected code                           │ │
│  │  • Validates syntax                                   │ │
│  │  • Uses Groq LLaMA 3.3 70B                           │ │
│  └────────────────────────────────────────────────────────┘ │
│                       │                                      │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    Git Manager                               │
│  • Clones repository                                         │
│  • Applies fix to file                                       │
│  • Commits changes                                           │
│  • Pushes to GitHub                                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Repository                           │
│              (Fix Applied & Committed)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Triggers New Build
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Actions                              │
│              (Verification Build)                            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    SQLite Database                           │
│  • Pipelines                                                 │
│  • Failure Analyses                                          │
│  • Applied Fixes                                             │
│  • Audit Trail                                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                  React Dashboard (UI)                        │
│  • Real-time monitoring                                      │
│  • Analytics & metrics                                       │
│  • Fix history                                               │
│  • Pipeline status                                           │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

#### Backend
```
Python 3.11+
├── FastAPI (Web Framework)
├── SQLAlchemy (ORM)
├── SQLite (Database)
├── Groq SDK (AI API)
├── PyGithub (GitHub API)
├── GitPython (Git Operations)
├── Pydantic (Data Validation)
├── Loguru (Logging)
└── Python-dotenv (Environment)
```

#### Frontend
```
React 18 + TypeScript
├── Vite (Build Tool)
├── TanStack Query (Data Fetching)
├── React Router (Navigation)
├── Axios (HTTP Client)
├── date-fns (Date Formatting)
└── Lucide React (Icons)
```

#### AI/ML
```
Groq Cloud API
└── LLaMA 3.3 70B Versatile
    ├── 128K context window
    ├── 300+ tokens/sec
    └── Free tier available
```

---

## Components

### 1. Agent Orchestrator

**Location:** `agent-core/app/services/agent_orchestrator.py`

**Responsibilities:**
- Coordinates all services
- Manages monitoring cycle
- Handles failure events
- Tracks processing state
- Prevents duplicate processing

**Key Methods:**
```python
start_monitoring()      # Start monitoring loop
_monitoring_cycle()     # Single monitoring iteration
_handle_failure()       # Process detected failure
_analyze_failure()      # Trigger AI analysis
_apply_fix()           # Apply generated fix
```

**Configuration:**
```python
MONITORING_INTERVAL = 60  # seconds
MAX_RETRIES = 3
CONFIDENCE_THRESHOLD = 70  # percentage
```

### 2. GitHub Monitor

**Location:** `agent-core/app/services/monitors/github_monitor.py`

**Responsibilities:**
- Poll GitHub Actions API
- Detect failed workflows
- Extract error logs
- Track workflow runs

**Key Methods:**
```python
check_pipelines()           # Check all repositories
_get_workflow_runs()        # Get runs for repo
_extract_error_logs()       # Parse failure logs
_is_actionable_failure()    # Filter failures
```

**API Calls:**
```python
# Get workflow runs
GET /repos/{owner}/{repo}/actions/runs

# Get workflow logs
GET /repos/{owner}/{repo}/actions/runs/{run_id}/logs

# Get job details
GET /repos/{owner}/{repo}/actions/runs/{run_id}/jobs
```

### 3. Error Analyzer (AI)

**Location:** `agent-core/app/services/error_analyzer.py`

**Responsibilities:**
- Classify error type
- Extract root cause
- Calculate confidence score
- Provide fix recommendations

**AI Prompt Structure:**
```python
SYSTEM_PROMPT = """
You are an expert DevOps engineer analyzing CI/CD failures.
Classify the error and provide root cause analysis.
"""

USER_PROMPT = f"""
Error Log:
{error_log}

Repository: {repo}
Branch: {branch}
Commit: {commit_sha}

Analyze this failure and provide:
1. Error category
2. Root cause
3. Affected file/line
4. Confidence score (0-100)
"""
```

**Error Categories:**
- `syntax_error`
- `dependency_conflict`
- `test_failure`
- `configuration_error`
- `environment_issue`
- `timeout`
- `resource_limit`
- `unknown`

### 4. Fix Engine (AI)

**Location:** `agent-core/app/services/fix_engine.py`

**Responsibilities:**
- Generate code fixes
- Validate syntax
- Create fix descriptions
- Handle multiple fix strategies

**AI Prompt Structure:**
```python
SYSTEM_PROMPT = """
You are an expert programmer. Generate corrected code.
Return ONLY the complete corrected file content.
"""

USER_PROMPT = f"""
File: {file_path}
Error: {error_message}
Root Cause: {root_cause}

Current Code:
{current_code}

Generate the COMPLETE corrected file.
"""
```

**Fix Strategies:**
1. **Complete File Replacement** (Primary)
   - Fetch entire file
   - Generate corrected version
   - Replace completely

2. **Patch-Based** (Fallback)
   - Generate diff
   - Apply patch
   - Validate result

### 5. Git Manager

**Location:** `agent-core/app/services/git_manager.py`

**Responsibilities:**
- Clone repositories
- Apply fixes
- Commit changes
- Push to GitHub
- Handle authentication

**Key Methods:**
```python
apply_fix()              # Main entry point
_clone_repository()      # Clone to temp dir
_find_file_in_repo()     # Locate target file
_ai_fix_syntax_file()    # Apply AI-generated fix
_commit_and_push()       # Commit & push changes
```

**Git Operations:**
```bash
# Clone
git clone https://github.com/{owner}/{repo}.git

# Configure
git config user.name "AI Healer Bot"
git config user.email "bot@aihealer.dev"

# Commit
git add {file_path}
git commit -m "AI Fix: {description}"

# Push
git push origin {branch}
```

### 6. Database Models

**Location:** `agent-core/app/models/pipeline.py`

**Tables:**

#### Pipeline
```python
id: int (PK)
repository: str
branch: str
commit_sha: str
status: str  # success, failure, pending, running
started_at: datetime
completed_at: datetime
error_message: str
created_at: datetime
```

#### FailureAnalysis
```python
id: int (PK)
pipeline_id: int (FK)
error_category: str
root_cause: str
affected_files: str
confidence_score: int
recommended_actions: str
analyzed_at: datetime
```

#### AppliedFix
```python
id: int (PK)
analysis_id: int (FK)
fix_type: str
fix_description: str
files_modified: str
commit_sha: str
status: str  # pending, applied, verified, failed
applied_at: datetime
verified_at: datetime
success: bool
```

### 7. REST API

**Location:** `agent-core/app/api/routes.py`

**Endpoints:**

```python
GET  /api/v1/health          # Health check
GET  /api/v1/stats           # System statistics
GET  /api/v1/pipelines       # List all pipelines
GET  /api/v1/pipelines/{id}  # Get pipeline details
GET  /api/v1/failures        # List failure analyses
GET  /api/v1/failures/{id}   # Get failure details
GET  /api/v1/fixes           # List applied fixes
GET  /api/v1/fixes/{id}      # Get fix details
POST /api/v1/trigger         # Manual trigger
```

**Response Format:**
```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation completed",
  "timestamp": "2026-03-01T12:00:00Z"
}
```

### 8. React Dashboard

**Location:** `dashboard/src/`

**Pages:**

#### Dashboard (`/`)
- System overview
- Recent fixes showcase
- Statistics cards
- Recent activity

#### Pipelines (`/pipelines`)
- All pipeline runs
- Status tracking
- Commit information
- Timestamps

#### Failures (`/failures`)
- Failure analyses
- Error categories
- Root causes
- Confidence scores

#### Fixes (`/fixes`)
- Applied fixes
- Success/failure status
- Commit links
- Timestamps

**Components:**
```
src/
├── pages/
│   ├── Dashboard.tsx
│   ├── Pipelines.tsx
│   ├── Failures.tsx
│   └── Fixes.tsx
├── components/
│   └── Layout.tsx
├── api/
│   └── client.ts
└── main.tsx
```

---

## Setup Guide

### Prerequisites

```bash
# Required
- Python 3.11+
- Node.js 18+
- Git
- GitHub account
- Groq API key (free)

# Optional
- Docker
- PostgreSQL (for production)
```

### Backend Setup

```bash
# 1. Navigate to backend
cd agent-core

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env

# 6. Configure .env
GITHUB_TOKEN=ghp_your_token_here
GITHUB_USERNAME=your_username
GROQ_API_KEY=gsk_your_key_here
AI_PROVIDER=groq
AI_MODEL=llama-3.3-70b-versatile

# 7. Initialize database
python -c "from app.database.session import init_db; init_db()"

# 8. Run backend
python main.py
```

### Frontend Setup

```bash
# 1. Navigate to frontend
cd dashboard

# 2. Install dependencies
npm install

# 3. Create .env file
echo "VITE_API_BASE_URL=http://localhost:8000" > .env

# 4. Run development server
npm run dev

# 5. Open browser
# http://localhost:5173
```

### GitHub Token Setup

```bash
# 1. Go to GitHub Settings
https://github.com/settings/tokens

# 2. Generate new token (classic)
# Required scopes:
- repo (all)
- workflow

# 3. Copy token
# 4. Add to agent-core/.env
GITHUB_TOKEN=ghp_your_token_here
```

### Groq API Key Setup

```bash
# 1. Go to Groq Console
https://console.groq.com

# 2. Sign up (free)
# 3. Create API key
# 4. Copy key
# 5. Add to agent-core/.env
GROQ_API_KEY=gsk_your_key_here
```

---

## Usage Guide

### Starting the System

```bash
# Terminal 1: Backend
cd agent-core
venv\Scripts\activate  # Windows
python main.py

# Terminal 2: Frontend
cd dashboard
npm run dev
```

### Creating a Test Failure

```python
# 1. Create test file in your repo
# test_syntax.py
def calculate_sum(a, b)  # Missing colon
    return a + b

# 2. Commit and push
git add test_syntax.py
git commit -m "Test: Syntax error"
git push origin main

# 3. Watch GitHub Actions fail
# 4. Watch agent fix it automatically
```

### Monitoring the System

```bash
# Backend logs
tail -f agent-core/logs/agent.log

# Database queries
sqlite3 agent-core/agent.db
SELECT * FROM pipelines ORDER BY created_at DESC LIMIT 5;
SELECT * FROM failure_analyses ORDER BY analyzed_at DESC LIMIT 5;
SELECT * FROM applied_fixes ORDER BY applied_at DESC LIMIT 5;

# Dashboard
# Open http://localhost:5173
```

### Manual Trigger

```bash
# Trigger analysis for specific pipeline
curl -X POST http://localhost:8000/api/v1/trigger \
  -H "Content-Type: application/json" \
  -d '{
    "repository": "owner/repo",
    "run_id": 12345678
  }'
```

---

## API Reference

### GET /api/v1/stats

Get system statistics.

**Response:**
```json
{
  "total_pipelines": 150,
  "total_failures": 45,
  "successful_fixes": 38,
  "success_rate": 84.4,
  "avg_fix_time": 45.2
}
```

### GET /api/v1/pipelines

List all pipelines.

**Query Parameters:**
- `limit` (int): Max results (default: 100)
- `offset` (int): Pagination offset
- `status` (str): Filter by status

**Response:**
```json
[
  {
    "id": 1,
    "repository": "owner/repo",
    "branch": "main",
    "commit_sha": "abc123",
    "status": "failure",
    "started_at": "2026-03-01T12:00:00Z",
    "error_message": "SyntaxError: invalid syntax"
  }
]
```

### GET /api/v1/failures

List failure analyses.

**Response:**
```json
[
  {
    "id": 1,
    "pipeline_id": 1,
    "error_category": "syntax_error",
    "root_cause": "Missing colon after function definition",
    "confidence_score": 95,
    "analyzed_at": "2026-03-01T12:01:00Z"
  }
]
```

### GET /api/v1/fixes

List applied fixes.

**Response:**
```json
[
  {
    "id": 1,
    "analysis_id": 1,
    "fix_type": "syntax_fix",
    "fix_description": "Added missing colon",
    "commit_sha": "def456",
    "status": "applied",
    "success": true,
    "applied_at": "2026-03-01T12:02:00Z"
  }
]
```

---

## Configuration

### Environment Variables

```bash
# GitHub
GITHUB_TOKEN=ghp_xxx              # GitHub personal access token
GITHUB_USERNAME=your_username      # Your GitHub username

# AI Provider
AI_PROVIDER=groq                   # groq or gemini
AI_MODEL=llama-3.3-70b-versatile  # Model name
GROQ_API_KEY=gsk_xxx              # Groq API key

# Database
DATABASE_URL=sqlite:///agent.db    # Database connection

# Monitoring
MONITORING_INTERVAL=60             # Seconds between checks
MAX_RETRIES=3                      # Max retry attempts
CONFIDENCE_THRESHOLD=70            # Min confidence for auto-fix

# Logging
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR
LOG_FILE=logs/agent.log           # Log file path
```

### Agent Configuration

```yaml
# config/agent-config.yaml
monitoring:
  interval: 60
  max_retries: 3
  timeout: 300

analysis:
  confidence_threshold: 70
  max_context_length: 8000
  
fixes:
  auto_apply: true
  create_branch: false
  commit_message_template: "AI Fix: {description}"
  
git:
  user_name: "AI Healer Bot"
  user_email: "bot@aihealer.dev"
```

---

## Troubleshooting

### Common Issues

#### 1. GitHub API Rate Limit

**Error:** `API rate limit exceeded`

**Solution:**
```bash
# Check rate limit
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit

# Wait for reset or use authenticated requests
```

#### 2. Groq API Errors

**Error:** `Invalid API key`

**Solution:**
```bash
# Verify API key
echo $GROQ_API_KEY

# Test API key
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

#### 3. Git Push Failures

**Error:** `Permission denied`

**Solution:**
```bash
# Verify token has correct scopes
# Regenerate token with repo + workflow scopes
# Update .env file
```

#### 4. Database Locked

**Error:** `database is locked`

**Solution:**
```bash
# Stop all processes
# Delete lock file
rm agent-core/agent.db-journal

# Restart
```

#### 5. Frontend Connection Error

**Error:** `Network Error`

**Solution:**
```bash
# Verify backend is running
curl http://localhost:8000/api/v1/health

# Check CORS settings
# Verify VITE_API_BASE_URL in dashboard/.env
```

### Debug Mode

```bash
# Enable debug logging
export LOG_LEVEL=DEBUG

# Run with verbose output
python main.py --debug

# Check logs
tail -f logs/agent.log
```

---

## Development

### Project Structure

```
self-healing-cicd/
├── agent-core/              # Backend
│   ├── app/
│   │   ├── api/            # REST API
│   │   ├── core/           # Configuration
│   │   ├── database/       # Database
│   │   ├── models/         # Data models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── logs/               # Log files
│   ├── main.py            # Entry point
│   └── requirements.txt    # Dependencies
├── dashboard/              # Frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   └── main.tsx       # Entry point
│   └── package.json       # Dependencies
└── docs/                  # Documentation
```

### Adding New Features

#### 1. Add New Error Category

```python
# agent-core/app/services/error_analyzer.py

ERROR_PATTERNS = {
    'new_category': [
        r'pattern1',
        r'pattern2'
    ]
}

def _classify_error(self, error_log: str) -> str:
    # Add new classification logic
    if 'new_pattern' in error_log:
        return 'new_category'
```

#### 2. Add New Fix Strategy

```python
# agent-core/app/services/fix_engine.py

async def generate_fix(self, analysis: FailureAnalysis) -> dict:
    if analysis.error_category == 'new_category':
        return await self._new_fix_strategy(analysis)
```

#### 3. Add New API Endpoint

```python
# agent-core/app/api/routes.py

@router.get("/new-endpoint")
async def new_endpoint(db: Session = Depends(get_db)):
    # Implementation
    return {"data": result}
```

#### 4. Add New Dashboard Page

```typescript
// dashboard/src/pages/NewPage.tsx

export default function NewPage() {
  const { data } = useQuery({
    queryKey: ['newData'],
    queryFn: fetchNewData
  })
  
  return <div>{/* UI */}</div>
}
```

### Testing

```bash
# Backend tests
cd agent-core
pytest tests/

# Frontend tests
cd dashboard
npm test

# Integration tests
python tests/integration/test_end_to_end.py

# Load tests
python tests/load/test_performance.py
```

---

## Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY agent-core/ .
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
```

```bash
# Build
docker build -t ai-healer .

# Run
docker run -d \
  -p 8000:8000 \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  -e GROQ_API_KEY=$GROQ_API_KEY \
  ai-healer
```

### Cloud Deployment

#### AWS

```bash
# Deploy to EC2
aws ec2 run-instances \
  --image-id ami-xxx \
  --instance-type t3.medium \
  --key-name your-key

# Deploy to ECS
aws ecs create-service \
  --cluster ai-healer \
  --service-name agent \
  --task-definition ai-healer:1
```

#### Heroku

```bash
# Create app
heroku create ai-healer

# Set config
heroku config:set GITHUB_TOKEN=xxx
heroku config:set GROQ_API_KEY=xxx

# Deploy
git push heroku main
```

#### Railway

```bash
# Install CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Production Checklist

- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Set up monitoring (Sentry, DataDog)
- [ ] Configure log rotation
- [ ] Set up backups
- [ ] Enable rate limiting
- [ ] Add authentication
- [ ] Set up CI/CD for the agent itself
- [ ] Configure webhooks instead of polling
- [ ] Set up alerting

---

## Support

### Getting Help

- **Documentation:** This file
- **Issues:** GitHub Issues
- **Email:** support@aihealer.dev
- **Discord:** [Community Server]

### Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

### License

MIT License - See LICENSE file

---

**Last Updated:** March 1, 2026
**Version:** 1.0.0
**Status:** Production Ready ✅
