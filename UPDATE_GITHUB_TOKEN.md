# Update GitHub Token for Write Access

## Current Issue:
Your GitHub token only has READ access. To actually push fixes, it needs WRITE access.

## Steps to Update Token:

1. **Go to GitHub Settings**:
   - https://github.com/settings/tokens

2. **Find your token** (starts with `github_pat_11BQJTWII...`)
   - Click on it

3. **Update Permissions**:
   Add these permissions:
   - ✅ `repo` (Full control of private repositories)
     - This includes: `repo:status`, `repo_deployment`, `public_repo`, `repo:invite`
   - ✅ `workflow` (Update GitHub Action workflows)
   - ✅ `write:packages` (Upload packages to GitHub Package Registry)

4. **Save the token**

5. **Update `.env` file**:
   Replace the old token with the new one in:
   - `agent-core/.env`

## Alternative: Create New Token

If you can't edit the existing token:

1. Go to: https://github.com/settings/tokens/new
2. Name: `CI Healer - Full Access`
3. Expiration: 90 days (or your preference)
4. Select scopes:
   - ✅ `repo` (all sub-options)
   - ✅ `workflow`
5. Click "Generate token"
6. Copy the new token
7. Update `agent-core/.env`:
   ```
   GITHUB_TOKEN=your_new_token_here
   ```

## After Updating:

Restart the backend:
```powershell
cd C:\Users\atsha\self-healing-cicd\agent-core
python main.py
```

The system will now be able to:
1. Clone repositories ✅
2. Fix syntax errors ✅
3. Commit changes ✅
4. Push to GitHub ✅
5. Trigger re-runs ✅

This completes the full auto-healing cycle!
