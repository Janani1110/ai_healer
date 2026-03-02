# Start Dashboard Script for Windows

Write-Host "Starting Self-Healing CI/CD Agent Dashboard..." -ForegroundColor Cyan

# Navigate to dashboard
Set-Location dashboard

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

# Start the dashboard
Write-Host ""
Write-Host "Starting dashboard on http://localhost:3000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

npm run dev
