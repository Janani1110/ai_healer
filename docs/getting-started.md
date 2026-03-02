# Getting Started

## Quick Start Guide

### 1. Installation

#### Using Setup Script (Recommended)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```powershell
.\setup.ps1
```

#### Manual Installation

**Backend:**
```bash
cd agent-core
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Dashboard:**
```bash
cd dashboard
npm install
```

### 2. Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your credentials:
   ```env
   # Required: At least one CI/CD platform
   GITHUB_TOKEN=ghp_your_token_here
   
   # Required: AI provider
   OPENAI_API_KEY=sk-your_key_here
   
   # Optional: Additional platforms
   GITLAB_TOKEN=glpat_your_token_here
   JENKINS_URL=http://jenkins.example.com
   JENKINS_USER=admin
   JENKINS_TOKEN=your_token
   ```

3. Customize agent behavior in `config/agent-config.yaml`

### 3. Running the Agent

#### Development Mode

**Terminal 1 - Backend:**
```bash
cd agent-core
python main.py
```

**Terminal 2 - Dashboard:**
```bash
cd dashboard
npm run dev
```

Access the dashboard at: http://localhost:3000

#### Production Mode (Docker)

```bash
docker-compose up -d
```

Access the dashboard at: http://localhost:3000

### 4. Verify Setup

1. Check the agent logs:
   ```bash
   tail -f agent-core/agent.log
   ```

2. Visit the dashboard and check the stats page

3. Trigger a test pipeline failure to see the agent in action

## First Steps

### Monitor Your First Pipeline

1. The agent automatically monitors all repositories you have access to
2. When a pipeline fails, check the dashboard's "Failures" page
3. View the analysis and generated fix in the "Fixes" page

### Understanding the Dashboard

- **Dashboard**: Overview with key metrics
- **Pipelines**: All monitored pipeline runs
- **Failures**: Detailed error analyses
- **Fixes**: Applied fixes and their success status

### Customizing Behavior

Edit `config/agent-config.yaml` to:
- Change polling interval
- Filter specific branches
- Enable/disable auto-fix
- Configure commit strategy
- Set up notifications

## Troubleshooting

### Agent not detecting pipelines
- Verify your CI/CD platform token has correct permissions
- Check the logs for authentication errors
- Ensure repositories are accessible with the token

### Fixes not being applied
- Check `AUTO_FIX_ENABLED=true` in `.env`
- Verify `AUTO_COMMIT_ENABLED=true` for automatic commits
- Review agent logs for errors

### Dashboard not loading data
- Ensure the backend is running on port 8000
- Check browser console for API errors
- Verify CORS settings if running on different domains

## Next Steps

- Read the [Architecture](architecture.md) documentation
- Set up additional [Integrations](integrations.md)
- Review the [API Reference](api.md)
- Customize fix strategies in the code
