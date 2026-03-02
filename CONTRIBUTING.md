# Contributing to Self-Healing CI/CD Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. Fork the repository
2. Clone your fork
3. Run the setup script
4. Create a new branch for your feature

```bash
git checkout -b feature/your-feature-name
```

## Project Structure

```
.
├── agent-core/          # Python backend
│   ├── app/
│   │   ├── api/        # FastAPI routes
│   │   ├── core/       # Configuration
│   │   ├── database/   # Database setup
│   │   ├── models/     # SQLAlchemy models
│   │   ├── schemas/    # Pydantic schemas
│   │   └── services/   # Business logic
│   └── main.py         # Entry point
├── dashboard/          # React frontend
│   └── src/
│       ├── api/        # API client
│       ├── components/ # React components
│       └── pages/      # Page components
├── config/             # Configuration files
└── docs/              # Documentation
```

## Adding New Features

### Adding a New CI/CD Platform Monitor

1. Create a new monitor in `agent-core/app/services/monitors/`
2. Inherit from `BaseMonitor`
3. Implement required methods:
   - `check_pipelines()`
   - `get_pipeline_logs()`
   - `trigger_pipeline()`
4. Register in `AgentOrchestrator._init_monitors()`

Example:
```python
from app.services.monitors.base_monitor import BaseMonitor

class CircleCIMonitor(BaseMonitor):
    async def check_pipelines(self):
        # Implementation
        pass
```

### Adding a New Fix Strategy

1. Add method to `FixEngine` in `agent-core/app/services/fix_engine.py`
2. Update error category routing in `generate_fix()`
3. Add corresponding error category to `ErrorCategory` enum

### Adding Dashboard Pages

1. Create new page component in `dashboard/src/pages/`
2. Add route in `dashboard/src/App.tsx`
3. Add navigation link in `dashboard/src/components/Layout.tsx`

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Maximum line length: 120 characters
- Use meaningful variable names

### TypeScript/React
- Use functional components with hooks
- Follow React best practices
- Use TypeScript for type safety

## Testing

### Backend Tests
```bash
cd agent-core
pytest tests/ -v
```

### Frontend Tests
```bash
cd dashboard
npm test
```

## Commit Messages

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Example:
```
feat: add CircleCI monitor support
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update README.md if adding new features
5. Submit PR with clear description

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions about the codebase

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
