#!/bin/bash

echo "🤖 Setting up AI-Powered Self-Healing CI/CD Agent..."

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi

echo "✅ Prerequisites met"

# Setup backend
echo ""
echo "📦 Setting up backend..."
cd agent-core

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt

cd ..

# Setup frontend
echo ""
echo "📦 Setting up dashboard..."
cd dashboard
npm install
cd ..

# Setup environment
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your credentials"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your CI/CD platform credentials"
echo "2. Start the agent: cd agent-core && python main.py"
echo "3. Start the dashboard: cd dashboard && npm run dev"
echo ""
echo "Or use Docker: docker-compose up"
