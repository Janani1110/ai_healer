import asyncio
from typing import Dict, Any
from loguru import logger
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.models.pipeline import Pipeline, FailureAnalysis, Fix, PipelineStatus, FixStatus
from app.services.monitors.github_monitor import GithubMonitor
from app.services.monitors.gitlab_monitor import GitlabMonitor
from app.services.error_analyzer import ErrorAnalyzer
from app.services.fix_engine import FixEngine
from app.services.git_manager import GitManager
from app.core.config import settings
import yaml

class AgentOrchestrator:
    """Main orchestrator for the self-healing agent"""
    
    def __init__(self):
        self.monitors = []
        self.analyzer = ErrorAnalyzer()
        self.fix_engine = FixEngine()
        self.git_manager = GitManager()
        self.running = False
        
        # Load configuration
        self._load_config()
        
        # Initialize monitors
        self._init_monitors()
    
    def _load_config(self):
        """Load agent configuration"""
        try:
            with open('config/agent-config.yaml', 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load config: {e}, using defaults")
            self.config = {'agent': {'polling_interval': 30}}
    
    def _init_monitors(self):
        """Initialize CI/CD platform monitors"""
        github_monitor = GithubMonitor(self.config)
        if github_monitor.is_configured():
            self.monitors.append(github_monitor)
            logger.info("GitHub monitor initialized")
        
        gitlab_monitor = GitlabMonitor(self.config)
        if gitlab_monitor.is_configured():
            self.monitors.append(gitlab_monitor)
            logger.info("GitLab monitor initialized")
        
        if not self.monitors:
            logger.warning("No monitors configured. Please set CI/CD platform credentials.")
    
    async def start_monitoring(self):
        """Start continuous monitoring loop"""
        self.running = True
        logger.info("Starting pipeline monitoring...")
        
        while self.running:
            try:
                await self._monitoring_cycle()
            except Exception as e:
                logger.error(f"Error in monitoring cycle: {e}")
            
            # Wait before next cycle
            interval = self.config.get('agent', {}).get('polling_interval', 30)
            await asyncio.sleep(interval)
    
    async def _monitoring_cycle(self):
        """Single monitoring cycle"""
        logger.debug("Running monitoring cycle...")
        
        for monitor in self.monitors:
            try:
                # Check for pipeline failures
                failures = await monitor.check_pipelines()
                
                for failure_data in failures:
                    await self._handle_failure(monitor, failure_data)
            
            except Exception as e:
                logger.error(f"Error checking {monitor.platform_name}: {e}")
    
    async def _handle_failure(self, monitor, failure_data: Dict[str, Any]):
        """Handle a detected pipeline failure"""
        logger.info(f"Handling failure: {failure_data['pipeline_id']}")
        
        db = SessionLocal()
        
        try:
            # Check if already processed
            existing = db.query(Pipeline).filter(
                Pipeline.pipeline_id == failure_data['pipeline_id']
            ).first()
            
            if existing:
                logger.debug(f"Pipeline {failure_data['pipeline_id']} already processed")
                return
            
            # Save pipeline record
            pipeline = Pipeline(
                platform=failure_data['platform'],
                repository=failure_data['repository'],
                branch=failure_data['branch'],
                commit_sha=failure_data['commit_sha'],
                pipeline_id=failure_data['pipeline_id'],
                status=PipelineStatus.FAILURE,
                started_at=failure_data['started_at'],
                completed_at=failure_data.get('completed_at')
            )
            db.add(pipeline)
            db.commit()
            db.refresh(pipeline)
            
            # Get logs and analyze
            logs = await monitor.get_pipeline_logs(failure_data['pipeline_id'])
            pipeline.logs = logs
            db.commit()
            
            # Analyze error
            analysis_result = await self.analyzer.analyze_failure(logs, failure_data)
            
            # Save analysis
            analysis = FailureAnalysis(
                pipeline_id=pipeline.id,
                error_category=analysis_result['error_category'],
                error_message=analysis_result['error_message'],
                root_cause=analysis_result['root_cause'],
                affected_files=str(analysis_result['affected_files']),
                confidence_score=analysis_result['confidence_score']
            )
            db.add(analysis)
            db.commit()
            db.refresh(analysis)
            
            # Generate and apply fix if enabled
            if settings.AUTO_FIX_ENABLED:
                await self._apply_fix(db, monitor, pipeline, analysis, failure_data)
        
        finally:
            db.close()
    
    async def _apply_fix(self, db: Session, monitor, pipeline: Pipeline, 
                        analysis: FailureAnalysis, failure_data: Dict[str, Any]):
        """Generate and apply automated fix"""
        logger.info(f"Generating fix for analysis {analysis.id}")
        
        try:
            # Generate fix
            fix_result = await self.fix_engine.generate_fix(
                {
                    'error_category': analysis.error_category,
                    'error_message': analysis.error_message,
                    'root_cause': analysis.root_cause,
                    'affected_files': eval(analysis.affected_files) if analysis.affected_files else []
                },
                failure_data
            )
            
            # Save fix record
            fix = Fix(
                analysis_id=analysis.id,
                fix_type=fix_result['fix_type'],
                description=fix_result['description'],
                changes=str(fix_result['changes']),
                status=FixStatus.PENDING
            )
            db.add(fix)
            db.commit()
            db.refresh(fix)
            
            # Apply fix if auto-applicable and auto-commit enabled
            if fix_result.get('auto_applicable') and settings.AUTO_COMMIT_ENABLED:
                success = await self._commit_fix(monitor, pipeline, fix, fix_result)
                
                fix.success = success
                fix.status = FixStatus.VERIFIED if success else FixStatus.FAILED
                db.commit()
        
        except Exception as e:
            logger.error(f"Error applying fix: {e}")
    
    async def _commit_fix(self, monitor, pipeline: Pipeline, 
                         fix: Fix, fix_result: Dict[str, Any]) -> bool:
        """Commit and push fix to repository"""
        logger.info(f"Committing fix {fix.id} to {pipeline.repository}")
        
        try:
            # Clone the repository
            repo_url = f"https://github.com/{pipeline.repository}.git"
            temp_dir = await self.git_manager.clone_repository(repo_url, pipeline.branch)
            
            if not temp_dir:
                logger.error("Failed to clone repository")
                return False
            
            # Apply the fix changes
            changes = fix_result.get('changes', [])
            if not changes:
                logger.warning("No changes to apply")
                return False
            
            success = await self.git_manager.apply_changes(temp_dir, changes)
            
            if not success:
                logger.error("Failed to apply changes")
                await self.git_manager.cleanup_repository(repo_url)
                return False
            
            # Commit and push
            commit_message = f"[CI Healer] {fix_result['description']}\n\nAuto-fix for pipeline failure #{pipeline.pipeline_id}"
            commit_sha = await self.git_manager.commit_and_push(temp_dir, commit_message)
            
            if commit_sha:
                fix.commit_sha = commit_sha
                fix.status = FixStatus.APPLIED
                logger.info(f"Successfully committed fix: {commit_sha}")
                
                # Trigger pipeline re-run
                await monitor.trigger_pipeline(pipeline.repository, pipeline.branch)
                logger.info(f"Re-triggered pipeline for {pipeline.repository}")
                
                # Cleanup
                await self.git_manager.cleanup_repository(repo_url)
                return True
            else:
                logger.error("Failed to commit changes")
                await self.git_manager.cleanup_repository(repo_url)
                return False
                
        except Exception as e:
            logger.error(f"Error committing fix: {e}")
            return False
            logger.info(f"Re-triggered pipeline for {pipeline.repository}")
            return True
        except Exception as e:
            logger.error(f"Failed to trigger pipeline: {e}")
            return False
    
    def stop_monitoring(self):
        """Stop the monitoring loop"""
        self.running = False
        logger.info("Stopping monitoring...")
