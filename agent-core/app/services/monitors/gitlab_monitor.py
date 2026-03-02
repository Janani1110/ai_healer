from typing import List, Dict, Any
from loguru import logger
from app.services.monitors.base_monitor import BaseMonitor
from app.core.config import settings
import gitlab

class GitlabMonitor(BaseMonitor):
    """Monitor for GitLab CI"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        if settings.GITLAB_TOKEN:
            self.client = gitlab.Gitlab(private_token=settings.GITLAB_TOKEN)
        else:
            self.client = None
    
    def is_configured(self) -> bool:
        return self.client is not None
    
    async def check_pipelines(self) -> List[Dict[str, Any]]:
        """Check GitLab CI pipelines"""
        if not self.is_configured():
            return []
        
        failures = []
        
        try:
            projects = self.client.projects.list(membership=True)
            
            for project in projects[:20]:  # Check first 20 projects
                pipelines = project.pipelines.list(per_page=10)
                
                for pipeline in pipelines:
                    if pipeline.status == "failed":
                        failures.append({
                            'pipeline_id': str(pipeline.id),
                            'repository': project.path_with_namespace,
                            'branch': pipeline.ref,
                            'commit_sha': pipeline.sha,
                            'status': 'failure',
                            'started_at': pipeline.created_at,
                            'completed_at': pipeline.updated_at
                        })
        except Exception as e:
            logger.error(f"Error checking GitLab pipelines: {e}")
        
        return failures
    
    async def get_pipeline_logs(self, pipeline_id: str) -> str:
        """Get logs for a GitLab pipeline"""
        if not self.is_configured():
            return ""
        
        try:
            # Simplified log retrieval
            return f"Logs for pipeline {pipeline_id}"
        except Exception as e:
            logger.error(f"Error fetching logs: {e}")
            return ""
    
    async def trigger_pipeline(self, repository: str, branch: str) -> str:
        """Trigger a GitLab pipeline"""
        if not self.is_configured():
            return ""
        
        try:
            project = self.client.projects.get(repository)
            pipeline = project.pipelines.create({'ref': branch})
            return f"Triggered pipeline {pipeline.id}"
        except Exception as e:
            logger.error(f"Error triggering pipeline: {e}")
        
        return ""
