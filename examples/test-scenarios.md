# Test Scenarios for Self-Healing Agent

This document provides test scenarios to verify the agent's functionality.

## Scenario 1: Dependency Conflict

### Setup
Create a Python project with conflicting dependencies:

**requirements.txt:**
```
requests==2.28.0
urllib3==2.0.0  # Conflicts with requests
```

**Expected Behavior:**
1. Agent detects dependency conflict
2. Classifies as `dependency_conflict`
3. Generates fix to update urllib3 version
4. Commits fix
5. Re-runs pipeline

### Verification
- Check dashboard "Failures" page for analysis
- Verify fix in "Fixes" page
- Confirm pipeline re-run succeeded

## Scenario 2: Test Failure

### Setup
Create a failing test:

**test_example.py:**
```python
def test_addition():
    assert 1 + 1 == 3  # Intentionally wrong
```

**Expected Behavior:**
1. Agent detects test failure
2. Classifies as `test_failure`
3. Analyzes assertion error
4. Suggests fix (may require manual review)

### Verification
- Check error analysis in dashboard
- Review suggested fix
- Verify confidence score

## Scenario 3: Syntax Error

### Setup
Create a file with syntax error:

**broken.py:**
```python
def hello()
    print("Missing colon")
```

**Expected Behavior:**
1. Agent detects syntax error
2. Classifies as `syntax_error`
3. Generates fix to add missing colon
4. Auto-formats code
5. Commits and re-runs

### Verification
- Verify syntax fix applied
- Check commit message
- Confirm pipeline success

## Scenario 4: Configuration Error

### Setup
Create invalid YAML config:

**.github/workflows/ci.yml:**
```yaml
name: CI
on: push
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test
        run: pytest
        # Missing required fields
```

**Expected Behavior:**
1. Agent detects configuration error
2. Classifies as `configuration_error`
3. Adds missing configuration
4. Validates YAML syntax

## Scenario 5: Environment Issue

### Setup
Reference undefined environment variable:

**script.sh:**
```bash
echo $UNDEFINED_VAR
```

**Expected Behavior:**
1. Agent detects environment issue
2. Classifies as `environment_issue`
3. Suggests adding to .env or CI config
4. Creates fix with placeholder value

## Testing Checklist

### Basic Functionality
- [ ] Agent starts without errors
- [ ] Monitors connect to CI/CD platforms
- [ ] Dashboard loads and displays data
- [ ] API endpoints respond correctly

### Error Detection
- [ ] Detects GitHub Actions failures
- [ ] Detects GitLab CI failures
- [ ] Detects Jenkins failures
- [ ] Correctly classifies error types

### Fix Generation
- [ ] Generates fixes for dependency conflicts
- [ ] Generates fixes for syntax errors
- [ ] Generates fixes for config errors
- [ ] AI analysis provides useful insights

### Fix Application
- [ ] Commits fixes to repository
- [ ] Uses correct commit message format
- [ ] Re-triggers pipeline after fix
- [ ] Tracks fix success/failure

### Dashboard
- [ ] Shows accurate statistics
- [ ] Displays recent pipelines
- [ ] Shows failure analyses
- [ ] Lists applied fixes
- [ ] Updates in real-time

## Performance Testing

### Load Test
1. Monitor 10+ repositories simultaneously
2. Verify agent handles multiple failures
3. Check response time remains acceptable
4. Monitor memory and CPU usage

### Stress Test
1. Trigger multiple failures rapidly
2. Verify agent queues fixes appropriately
3. Check no fixes are lost
4. Verify database integrity

## Integration Testing

### GitHub Actions
```bash
# Create test repository
# Add workflow with intentional failure
# Verify agent detects and fixes
```

### GitLab CI
```bash
# Create test project
# Add .gitlab-ci.yml with failure
# Verify agent detects and fixes
```

## Manual Testing Steps

1. **Setup Test Environment**
   ```bash
   # Use test repositories, not production
   export GITHUB_TOKEN=test_token
   export OPENAI_API_KEY=test_key
   ```

2. **Trigger Test Failure**
   - Push commit with known issue
   - Wait for pipeline to fail

3. **Monitor Agent**
   ```bash
   tail -f agent-core/agent.log
   ```

4. **Verify Fix**
   - Check dashboard for analysis
   - Verify fix was committed
   - Confirm pipeline re-ran
   - Check success status

5. **Review Logs**
   - Check for any errors
   - Verify all steps completed
   - Review AI analysis quality

## Automated Test Suite

Create automated tests:

**test_agent.py:**
```python
import pytest
from app.services.error_analyzer import ErrorAnalyzer

def test_dependency_conflict_detection():
    analyzer = ErrorAnalyzer()
    logs = "ModuleNotFoundError: No module named 'requests'"
    result = analyzer._classify_error(logs)
    assert result == ErrorCategory.DEPENDENCY_CONFLICT

def test_syntax_error_detection():
    analyzer = ErrorAnalyzer()
    logs = "SyntaxError: invalid syntax"
    result = analyzer._classify_error(logs)
    assert result == ErrorCategory.SYNTAX_ERROR
```

## Success Criteria

Agent is working correctly if:
- ✅ Detects failures within polling interval
- ✅ Correctly classifies 80%+ of errors
- ✅ Generates applicable fixes for common issues
- ✅ Successfully applies fixes without breaking code
- ✅ Re-triggers pipelines after fixes
- ✅ Dashboard accurately reflects agent activity
- ✅ No data loss or corruption
- ✅ Handles errors gracefully

## Troubleshooting Tests

If tests fail:
1. Check agent logs for errors
2. Verify API credentials are valid
3. Ensure network connectivity
4. Check database is accessible
5. Verify AI API has credits
6. Review configuration settings
