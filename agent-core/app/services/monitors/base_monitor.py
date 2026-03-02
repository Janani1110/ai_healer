from abc import ABC, abstractmethod
from typing import List, Dict, Any
from loguru import logger

class BaseMonitor(ABC):
    """Base class for CI/CD platform monitors"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.platform_name = self.__class__.__name__.replace("Monitor", "").lower()
    
    @abstractmethod
    async def check_pipelines(self) -> List[Dict[str, Any]]:
        """Check for pipeline status updates"""
        pass
    
    @abstractmethod
    async def get_pipeline_logs(self, pipeline_id: str) -> str:
        """Retrieve logs for a specific pipeline"""
        pass
    
    @abstractmethod
    async def trigger_pipeline(self, repository: str, branch: str) -> str:
        """Trigger a pipeline run"""
        pass
    
    def is_configured(self) -> bool:
        """Check if monitor is properly configured"""
        return True
    
    async def handle_failure(self, pipeline_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a pipeline failure"""
        logger.info(f"Handling failure for {self.platform_name}: {pipeline_data.get('pipeline_id')}")
        
        logs = await self.get_pipeline_logs(pipeline_data['pipeline_id'])
        
        return {
            **pipeline_data,
            'logs': logs,
            'platform': self.platform_name
        }
