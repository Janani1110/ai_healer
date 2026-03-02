from typing import Dict, Any, Optional
from loguru import logger
from app.models.pipeline import ErrorCategory
import re
from app.core.config import settings

class ErrorAnalyzer:
    """AI-powered error analysis service"""
    
    def __init__(self):
        self.client = None
        self.ai_provider = settings.AI_PROVIDER.lower()
        
        if self.ai_provider == "openai" and settings.OPENAI_API_KEY:
            from openai import OpenAI
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.ai_provider == "ollama":
            try:
                import ollama
                self.client = ollama
                logger.info(f"Ollama client initialized with model: {settings.AI_MODEL}")
            except ImportError:
                logger.warning("Ollama package not installed. Run: pip install ollama")
                self.client = None
        elif self.ai_provider == "groq":
            try:
                from groq import Groq
                self.client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info(f"Groq client initialized with model: {settings.AI_MODEL}")
            except ImportError:
                logger.warning("Groq package not installed. Run: pip install groq")
                self.client = None
        elif self.ai_provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.client = genai
                logger.info(f"Gemini client initialized with model: {settings.AI_MODEL}")
            except ImportError:
                logger.warning("Google Generative AI package not installed. Run: pip install google-generativeai")
                self.client = None
    
    async def analyze_failure(self, logs: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze pipeline failure and determine root cause"""
        
        # First try pattern-based classification
        category = self._classify_error(logs)
        
        # Extract error details
        error_message = self._extract_error_message(logs)
        affected_files = self._extract_affected_files(logs)
        
        # Use AI for deeper analysis if available
        root_cause = await self._ai_analyze(logs, category) if self.client else None
        
        confidence = self._calculate_confidence(category, error_message, root_cause)
        
        return {
            'error_category': category,
            'error_message': error_message,
            'root_cause': root_cause or f"Detected {category.value} issue",
            'affected_files': affected_files,
            'confidence_score': confidence
        }
    
    def _classify_error(self, logs: str) -> ErrorCategory:
        """Classify error based on log patterns"""
        logs_lower = logs.lower()
        
        # Syntax error patterns - CHECK FIRST (highest priority)
        if any(pattern in logs_lower for pattern in [
            'syntax error', 'syntaxerror', 'parse error', 'unexpected token',
            'invalid syntax', 'compilation failed', 'expected \':\'', 'expected ":"'
        ]):
            return ErrorCategory.SYNTAX_ERROR
        
        # Dependency patterns
        if any(pattern in logs_lower for pattern in [
            'dependency', 'version conflict', 'package not found', 
            'module not found', 'cannot resolve'
        ]):
            return ErrorCategory.DEPENDENCY_CONFLICT
        
        # Test failure patterns
        if any(pattern in logs_lower for pattern in [
            'test failed', 'assertion error', 'expected', 'actual',
            'test suite failed', 'spec failed'
        ]):
            return ErrorCategory.TEST_FAILURE
        
        # Configuration patterns
        if any(pattern in logs_lower for pattern in [
            'config', 'configuration', 'missing key', 'invalid config',
            'yaml error', 'json error'
        ]):
            return ErrorCategory.CONFIGURATION_ERROR
        
        # Environment patterns
        if any(pattern in logs_lower for pattern in [
            'environment variable', 'env not set', 'path not found',
            'permission denied', 'access denied'
        ]):
            return ErrorCategory.ENVIRONMENT_ISSUE
        
        # Timeout patterns
        if any(pattern in logs_lower for pattern in [
            'timeout', 'timed out', 'deadline exceeded'
        ]):
            return ErrorCategory.TIMEOUT
        
        return ErrorCategory.UNKNOWN
    
    def _extract_error_message(self, logs: str) -> str:
        """Extract the main error message from logs"""
        lines = logs.split('\n')
        
        # Look for common error indicators
        error_keywords = ['error:', 'failed:', 'exception:', 'fatal:']
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in error_keywords):
                return line.strip()[:500]  # Limit length
        
        # Return last non-empty line if no error found
        for line in reversed(lines):
            if line.strip():
                return line.strip()[:500]
        
        return "Error message not found"
    
    def _extract_affected_files(self, logs: str) -> list:
        """Extract file paths mentioned in error logs and convert to repo-relative paths"""
        # Improved regex to capture full file paths with various extensions
        file_pattern = r'(?:[\w\-./]+/)?[\w\-]+\.(?:py|js|ts|tsx|jsx|java|go|rb|php|cpp|c|h|yaml|yml|json|xml|txt|md|sh|bat|ps1)'
        matches = re.findall(file_pattern, logs)
        
        # Also try to find files mentioned in common error patterns
        # Pattern: "File 'filename.ext'" or 'File "filename.ext"'
        quoted_pattern = r"[Ff]ile\s+['\"]([^'\"]+\.(?:py|js|ts|tsx|jsx|java|go|rb|php|cpp|c|h|yaml|yml|json|xml))['\"]"
        quoted_matches = re.findall(quoted_pattern, logs)
        
        # Pattern: "in filename.ext"
        in_pattern = r'\bin\s+([\w\-./]+\.(?:py|js|ts|tsx|jsx|java|go|rb|php|cpp|c|h|yaml|yml|json|xml))'
        in_matches = re.findall(in_pattern, logs)
        
        # Pattern: Python syntax errors often show: "  File "/path/to/file.py", line X"
        python_error_pattern = r'File\s+"([^"]+\.py)",\s+line\s+\d+'
        python_error_matches = re.findall(python_error_pattern, logs)
        
        # Combine all matches, prioritizing Python error pattern matches
        all_matches = python_error_matches + quoted_matches + in_matches + matches
        
        # Clean up paths to be relative to repo root
        cleaned_files = []
        seen = set()
        for file_path in all_matches:
            cleaned_path = self._clean_file_path(file_path)
            if cleaned_path and cleaned_path not in seen:
                # Filter out workflow files unless they're the only files found
                if not cleaned_path.startswith('.github/workflows'):
                    cleaned_files.append(cleaned_path)
                    seen.add(cleaned_path)
        
        # If no source files found, include workflow files
        if not cleaned_files:
            for file_path in all_matches:
                cleaned_path = self._clean_file_path(file_path)
                if cleaned_path and cleaned_path not in seen:
                    cleaned_files.append(cleaned_path)
                    seen.add(cleaned_path)
        
        # Remove duplicates and limit
        unique_files = cleaned_files[:10]
        
        return unique_files if unique_files else []
    
    def _clean_file_path(self, file_path: str) -> str:
        """Clean file path to be relative to repository root"""
        # Remove common CI runner absolute paths
        # GitHub Actions: /home/runner/work/repo-name/repo-name/
        # Windows: C:\home\runner\work\repo-name\repo-name\
        
        # Remove Windows drive letters
        if len(file_path) > 2 and file_path[1] == ':':
            file_path = file_path[2:]
        
        # Remove leading slashes/backslashes
        file_path = file_path.lstrip('/\\')
        
        # Common patterns to remove
        patterns_to_remove = [
            r'^home/runner/work/[^/]+/[^/]+/',  # GitHub Actions Linux
            r'^home\\runner\\work\\[^\\]+\\[^\\]+\\',  # GitHub Actions Windows
            r'^runner/work/[^/]+/[^/]+/',  # Alternative GitHub Actions
            r'^github/workspace/',  # Docker GitHub Actions
            r'^workspace/',  # Generic workspace
            r'^[^/]+/[^/]+/\.github/',  # Remove repo-name/repo-name/.github
            r'^[^\\]+\\[^\\]+\\\.github\\',  # Windows version
        ]
        
        for pattern in patterns_to_remove:
            file_path = re.sub(pattern, '', file_path)
        
        # If path still contains repository name twice (common in CI), remove first occurrence
        parts = file_path.split('/')
        if len(parts) > 2 and parts[0] == parts[1]:
            file_path = '/'.join(parts[1:])
        
        # Convert backslashes to forward slashes
        file_path = file_path.replace('\\', '/')
        
        # Remove any remaining leading slashes
        file_path = file_path.lstrip('/')
        
        # Skip if it's a URL or external path
        if 'github.com' in file_path or 'http' in file_path:
            return ''
        
        # Skip if it's still an absolute path
        if file_path.startswith('C:') or file_path.startswith('/home'):
            return ''
        
        return file_path
    
    async def _ai_analyze(self, logs: str, category: ErrorCategory) -> Optional[str]:
        """Use AI to perform deeper analysis"""
        if not self.client:
            return None
            
        try:
            prompt = f"""Analyze this CI/CD pipeline failure log and provide a concise root cause analysis.

Error Category: {category.value}

Logs:
{logs[:2000]}  # Limit log size

Provide:
1. Root cause (1-2 sentences)
2. Specific issue location if identifiable
3. Recommended fix approach

Keep response under 200 words."""

            if self.ai_provider == "ollama":
                response = self.client.chat(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a CI/CD debugging expert."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response['message']['content'].strip()
                
            elif self.ai_provider == "openai":
                response = self.client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a CI/CD debugging expert."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
                
            elif self.ai_provider == "groq":
                response = self.client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a CI/CD debugging expert."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
                
            elif self.ai_provider == "gemini":
                model = self.client.GenerativeModel(settings.AI_MODEL)
                full_prompt = "You are a CI/CD debugging expert.\n\n" + prompt
                response = model.generate_content(full_prompt)
                return response.text.strip()
                
            elif self.ai_provider == "anthropic":
                response = self.client.messages.create(
                    model=settings.AI_MODEL,
                    max_tokens=300,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.content[0].text.strip()
        
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return None
    
    def _calculate_confidence(self, category: ErrorCategory, 
                            error_message: str, root_cause: Optional[str]) -> int:
        """Calculate confidence score for the analysis"""
        confidence = 50  # Base confidence
        
        # Increase confidence if category is not unknown
        if category != ErrorCategory.UNKNOWN:
            confidence += 20
        
        # Increase if we have a clear error message
        if error_message and error_message != "Error message not found":
            confidence += 15
        
        # Increase if AI provided analysis
        if root_cause and len(root_cause) > 50:
            confidence += 15
        
        return min(confidence, 100)
