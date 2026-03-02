from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum

Base = declarative_base()

class PipelineStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    PENDING = "pending"
    RUNNING = "running"

class ErrorCategory(str, enum.Enum):
    DEPENDENCY_CONFLICT = "dependency_conflict"
    TEST_FAILURE = "test_failure"
    SYNTAX_ERROR = "syntax_error"
    CONFIGURATION_ERROR = "configuration_error"
    ENVIRONMENT_ISSUE = "environment_issue"
    TIMEOUT = "timeout"
    RESOURCE_LIMIT = "resource_limit"
    UNKNOWN = "unknown"

class FixStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPLIED = "applied"
    VERIFIED = "verified"
    FAILED = "failed"

class Pipeline(Base):
    __tablename__ = "pipelines"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, nullable=False)  # github, gitlab, jenkins
    repository = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    commit_sha = Column(String, nullable=False)
    pipeline_id = Column(String, nullable=False)
    status = Column(Enum(PipelineStatus), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    logs = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class FailureAnalysis(Base):
    __tablename__ = "failure_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, nullable=False)
    error_category = Column(Enum(ErrorCategory), nullable=False)
    error_message = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=True)
    affected_files = Column(Text, nullable=True)  # JSON array
    confidence_score = Column(Integer, nullable=False)  # 0-100
    analyzed_at = Column(DateTime, default=datetime.utcnow)

class Fix(Base):
    __tablename__ = "fixes"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, nullable=False)
    fix_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    changes = Column(Text, nullable=False)  # JSON with file changes
    commit_sha = Column(String, nullable=True)
    status = Column(Enum(FixStatus), nullable=False)
    success = Column(Boolean, default=False)
    applied_at = Column(DateTime, nullable=True)
    verified_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
