# PowerShell setup script for Windows

Write-Host "🤖 Setting up AI-Powered Self-Healing CI/CD Agent..." -ForegroundColor Cyan

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js is not installed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Prerequisites met" -ForegroundColor Green

# Setup backend
Write-Host ""
Write-Host "📦 Setting up backend..." -ForegroundColor Yellow
Set-Location agent-core

if (-not (Test-Path "venv")) {
    python -m venv venv
}

.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Set-Location ..

# Setup frontend
Write-Host ""
Write-Host "📦 Setting up dashboard..." -ForegroundColor Yellow
Set-Location dashboard
npm install
Set-Location ..

# Setup environment
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "📝 Creating .env file..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "⚠️  Please edit .env with your credentials" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Edit .env with your CI/CD platform credentials"
Write-Host "2. Start the agent: cd agent-core; python main.py"
Write-Host "3. Start the dashboard: cd dashboard; npm run dev"
Write-Host ""
Write-Host "Or use Docker: docker-compose up"
