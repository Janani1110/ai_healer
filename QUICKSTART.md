# ⚡ Quick Start Guide
## Get Running in 5 Minutes

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- Git
- GitHub account
- [Groq API key](https://console.groq.com) (free)

---

## Step 1: Clone & Setup (2 minutes)

```bash
# Clone repository
git clone https://github.com/Atshayaa10/self-healing-cicd.git
cd self-healing-cicd

# Backend setup
cd agent-core
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
```

**Required values in `.env`:**

```env
# GitHub
GITHUB_TOKEN=ghp_your_token_here
GITHUB_USERNAME=your_username

# Groq AI
GROQ_API_KEY=gsk_your_key_here
AI_MODEL=llama-3.3-70b-versatile
AI_PROVIDER=groq
```

### Get GitHub Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (all) + `workflow`
4. Copy token to `.env`

### Get Groq API Key
1. Go to https://console.groq.com
2. Sign up (free)
3. Create API key
4. Copy key to `.env`

---

## Step 3: Start Backend (30 seconds)

```bash
# Make sure you're in agent-core/ with venv activated
python main.py
```

**You should see:**
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Starting AI-Powered Self-Healing CI/CD Agent
```

---

## Step 4: Start Frontend (1 minute)

**Open a new terminal:**

```bash
cd dashboard

# Install dependencies
npm install

# Start development server
npm run dev
```

**You should see:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

---

## Step 5: Open Dashboard (10 seconds)

Open your browser to: **http://localhost:5173**

You should see the beautiful dashboard! 🎉

---

## Test It Out

### Create a Test Failure

1. **Create a file with syntax error in your GitHub repo:**

```python
# test_syntax.py
def calculate_sum(a, b)  # Missing colon
    return a + b
```

2. **Commit and push:**

```bash
git add test_syntax.py
git commit -m "Test: Syntax error"
git push origin main
```

3. **Watch the magic:**
   - GitHub Actions will fail
   - Agent detects failure (within 60 seconds)
   - AI analyzes the error
   - Fix is generated and committed
   - New build passes ✅

4. **Check the dashboard:**
   - See the failure analysis
   - See the applied fix
   - See the success!

---

## Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check .env file exists
ls .env
```

### Frontend won't start

```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### No failures detected

```bash
# Check GitHub token
echo $GITHUB_TOKEN  # Should show your token

# Check backend logs
# Look for "Found X failed pipelines"

# Verify repository has GitHub Actions
# Go to your repo → Actions tab
```

### AI not working

```bash
# Check Groq API key
echo $GROQ_API_KEY  # Should show your key

# Test API key
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

---

## What's Next?

### Learn More
- **Full Documentation:** [COMPLETE_SYSTEM_DOCUMENTATION.md](COMPLETE_SYSTEM_DOCUMENTATION.md)
- **Setup Guide:** [COMPLETE_SETUP_GUIDE.md](COMPLETE_SETUP_GUIDE.md)
- **Presentation:** [HACKATHON_PRESENTATION.md](HACKATHON_PRESENTATION.md)

### Customize
- Adjust monitoring interval in `agent-core/app/services/agent_orchestrator.py`
- Modify AI prompts in `agent-core/app/services/error_analyzer.py`
- Customize UI colors in `dashboard/src/pages/`

### Deploy
- See `docs/deployment.md` for production deployment
- Use PostgreSQL instead of SQLite
- Set up webhooks instead of polling
- Enable HTTPS

---

## Quick Commands Reference

```bash
# Start backend
cd agent-core && venv\Scripts\activate && python main.py

# Start frontend
cd dashboard && npm run dev

# Check database
sqlite3 agent-core/agent.db
SELECT * FROM pipelines ORDER BY created_at DESC LIMIT 5;

# View logs
tail -f agent-core/logs/agent.log

# Run tests
cd agent-core && pytest tests/
```

---

## Support

- **Issues:** https://github.com/Atshayaa10/self-healing-cicd/issues
- **Documentation:** [COMPLETE_SYSTEM_DOCUMENTATION.md](COMPLETE_SYSTEM_DOCUMENTATION.md)
- **Email:** support@aihealer.dev

---

**That's it! You're ready to go! 🚀**

The system will now automatically monitor your GitHub Actions and fix failures as they occur. Watch the dashboard for real-time updates!
