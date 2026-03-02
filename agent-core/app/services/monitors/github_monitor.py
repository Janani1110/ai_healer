from typing import List, Dict, Any
from github import Github
from loguru import logger
from app.services.monitors.base_monitor import BaseMonitor
from app.core.config import settings

class GithubMonitor(BaseMonitor):
    """Monitor for GitHub Actions"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if settings.GITHUB_TOKEN:
            self.client = Github(settings.GITHUB_TOKEN)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        return self.client is not None
    
    async def check_pipelines(self) -> List[Dict[str, Any]]:
        """Check GitHub Actions workflow runs"""
        if not self.is_configured():
            return []
        
        failures = []
        
        try:
            # Get repositories the token has access to
            repos = list(self.client.get_user().get_repos())
            
            if not repos:
                logger.info("No repositories found for this GitHub token")
                return []
            
            for repo in repos[:20]:  # Check first 20 repos to avoid rate limits
                try:
                    # Get recent workflow runs
                    workflows = repo.get_workflow_runs()
                    
                    for run in list(workflows)[:10]:  # Check last 10 runs
                        if run.status == "completed" and run.conclusion == "failure":
                            failures.append({
                                'pipeline_id': str(run.id),
                                'repository': repo.full_name,
                                'branch': run.head_branch,
                                'commit_sha': run.head_sha,
                                'status': 'failure',
                                'started_at': run.created_at,
                                'completed_at': run.updated_at,
                                'platform': 'github'
                            })
                except Exception as e:
                    logger.debug(f"Error checking workflows for {repo.full_name}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error checking GitHub pipelines: {e}")
        
        if failures:
            logger.info(f"Found {len(failures)} failed pipelines")
        
        return failures
    
    async def get_pipeline_logs(self, pipeline_id: str) -> str:
        """Get logs for a GitHub Actions run"""
        if not self.is_configured():
            return ""
        
        try:
            # Get all repos and find the workflow run
            repos = list(self.client.get_user().get_repos())
            
            for repo in repos:
                try:
                    run = repo.get_workflow_run(int(pipeline_id))
                    
                    # Get jobs for this run
                    jobs = run.jobs()
                    log_content = []
                    
                    for job in jobs:
                        log_content.append(f"Job: {job.name}")
                        log_content.append(f"Status: {job.conclusion}")
                        
                        # Get steps
                        for step in job.steps:
                            if step.conclusion == "failure":
                                log_content.append(f"\nFailed Step: {step.name}")
                                log_content.append(f"Conclusion: {step.conclusion}")
                    
                    # Try to get the actual log URL content
                    try:
                        import requests
                        log_url = run.logs_url
                        headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
                        response = requests.get(log_url, headers=headers, allow_redirects=True)
                        if response.status_code == 200:
                            # Logs are in zip format, extract text
                            import zipfile
                            import io
                            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                                for filename in z.namelist():
                                    with z.open(filename) as f:
                                        log_content.append(f.read().decode('utf-8', errors='ignore'))
                    except Exception as log_err:
                        logger.debug(f"Could not fetch detailed logs: {log_err}")
                    
                    return "\n".join(log_content) if log_content else f"Logs for run {pipeline_id}"
                    
                except Exception as e:
                    continue
            
            return f"Logs for run {pipeline_id}"
            
        except Exception as e:
            logger.error(f"Error fetching logs: {e}")
            return f"Logs for run {pipeline_id}"
    
    async def trigger_pipeline(self, repository: str, branch: str) -> str:
        """Trigger a GitHub Actions workflow"""
        if not self.is_configured():
            return ""
        
        try:
            repo = self.client.get_repo(repository)
            workflows = repo.get_workflows()
            
            if workflows.totalCount > 0:
                workflow = workflows[0]
                workflow.create_dispatch(branch)
                return f"Triggered workflow for {repository}:{branch}"
        except Exception as e:
            logger.error(f"Error triggering pipeline: {e}")
        
        return ""
