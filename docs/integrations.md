# Integration Guide

## GitHub Actions

### Setup

1. Create a GitHub Personal Access Token:
   - Go to Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` and `workflow` scopes
   
2. Add to `.env`:
   ```
   GITHUB_TOKEN=ghp_your_token_here
   ```

3. The agent will automatically monitor repositories you have access to

### Permissions Required
- `repo`: Full repository access
- `workflow`: Workflow management

## GitLab CI

### Setup

1. Create a GitLab Personal Access Token:
   - Go to User Settings → Access Tokens
   - Create token with `api` and `read_repository` scopes

2. Add to `.env`:
   ```
   GITLAB_TOKEN=glpat_your_token_here
   ```

### Permissions Required
- `api`: Full API access
- `read_repository`: Repository read access

## Jenkins

### Setup

1. Get Jenkins API token:
   - Go to User → Configure → API Token
   - Generate new token

2. Add to `.env`:
   ```
   JENKINS_URL=http://jenkins.example.com
   JENKINS_USER=your_username
   JENKINS_TOKEN=your_api_token
   ```

### Permissions Required
- Job read access
- Job build trigger access

## AI Provider Setup

### OpenAI

1. Get API key from https://platform.openai.com/api-keys

2. Add to `.env`:
   ```
   OPENAI_API_KEY=sk-your_key_here
   AI_MODEL=gpt-4
   ```

### Anthropic Claude (Alternative)

1. Get API key from https://console.anthropic.com/

2. Add to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your_key_here
   ```

## Configuration

Edit `config/agent-config.yaml` to customize:

- Polling interval
- Branch filters
- Auto-fix behavior
- Commit strategy
- Notification settings

## Testing Integration

Test your integration:

```bash
# Start the agent
cd agent-core
python main.py

# Check logs for connection status
tail -f agent.log
```

The agent will log successful connections to each platform.
