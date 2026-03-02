import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent-core'))

from github import Github
from app.core.config import settings

client = Github(settings.GITHUB_TOKEN)
repos = list(client.get_user().get_repos())

print(f"Total repositories: {len(repos)}\n")
print("First 15 repositories:")
for i, repo in enumerate(repos[:15], 1):
    print(f"{i}. {repo.full_name}")
    if 'sample_file_ci_cd' in repo.name:
        print(f"   ← FOUND sample_file_ci_cd at position {i}")
