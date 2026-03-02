from typing import Dict, Any, List
from loguru import logger
from app.models.pipeline import ErrorCategory
from app.core.config import settings
import json

class FixEngine:
    """Automated fix generation engine"""
    
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
                logger.info(f"Ollama client initialized for fix generation")
            except ImportError:
                logger.warning("Ollama package not installed")
                self.client = None
        elif self.ai_provider == "groq":
            try:
                from groq import Groq
                self.client = Groq(api_key=settings.GROQ_API_KEY)
                logger.info(f"Groq client initialized for fix generation")
            except ImportError:
                logger.warning("Groq package not installed")
                self.client = None
        elif self.ai_provider == "gemini":
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GOOGLE_API_KEY)
                self.client = genai
                logger.info(f"Gemini client initialized for fix generation")
            except ImportError:
                logger.warning("Google Generative AI package not installed")
                self.client = None
    
    async def generate_fix(self, analysis: Dict[str, Any], 
                          repository_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate automated fix based on error analysis"""
        
        category = analysis['error_category']
        
        # Route to appropriate fix strategy
        if category == ErrorCategory.DEPENDENCY_CONFLICT:
            return await self._fix_dependency_conflict(analysis, repository_context)
        elif category == ErrorCategory.TEST_FAILURE:
            return await self._fix_test_failure(analysis, repository_context)
        elif category == ErrorCategory.SYNTAX_ERROR:
            return await self._fix_syntax_error(analysis, repository_context)
        elif category == ErrorCategory.CONFIGURATION_ERROR:
            return await self._fix_configuration_error(analysis, repository_context)
        elif category == ErrorCategory.ENVIRONMENT_ISSUE:
            return await self._fix_environment_issue(analysis, repository_context)
        else:
            return await self._generic_fix(analysis, repository_context)
    
    async def _fix_dependency_conflict(self, analysis: Dict[str, Any], 
                                      context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix dependency conflicts"""
        
        # Example fix strategies
        changes = []
        
        # Strategy 1: Update package versions
        if 'package.json' in str(analysis.get('affected_files', [])):
            changes.append({
                'file': 'package.json',
                'action': 'update_dependency',
                'description': 'Update conflicting package versions'
            })
        
        # Strategy 2: Update requirements.txt
        if 'requirements.txt' in str(analysis.get('affected_files', [])):
            changes.append({
                'file': 'requirements.txt',
                'action': 'pin_version',
                'description': 'Pin dependency versions to resolve conflict'
            })
        
        # Use AI for specific fix if available
        if self.client:
            ai_fix = await self._ai_generate_fix(analysis, context)
            if ai_fix:
                changes.extend(ai_fix.get('changes', []))
        
        return {
            'fix_type': 'dependency_conflict_resolution',
            'description': 'Resolved dependency version conflicts',
            'changes': changes,
            'auto_applicable': True
        }
    
    async def _fix_test_failure(self, analysis: Dict[str, Any], 
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix test failures"""
        
        changes = []
        
        # Identify test files
        test_files = [f for f in analysis.get('affected_files', []) 
                     if 'test' in f.lower() or 'spec' in f.lower()]
        
        for test_file in test_files:
            changes.append({
                'file': test_file,
                'action': 'update_test',
                'description': 'Update test assertions or mocks'
            })
        
        return {
            'fix_type': 'test_failure_fix',
            'description': 'Fixed failing test cases',
            'changes': changes,
            'auto_applicable': False  # Tests need manual review
        }
    
    async def _fix_syntax_error(self, analysis: Dict[str, Any], 
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix syntax errors - AI will analyze file after cloning repo"""
        
        changes = []
        
        # For syntax errors, we'll use a special action that tells git_manager
        # to fetch the file, send it to AI, and replace it with corrected version
        for file in analysis.get('affected_files', []):
            if file and not file.endswith(('.yml', '.yaml', '.c')):
                changes.append({
                    'file': file,
                    'action': 'ai_fix_syntax',
                    'description': 'Fetch file, analyze with AI, and replace with corrected version',
                    'error_message': analysis.get('error_message', ''),
                    'root_cause': analysis.get('root_cause', '')
                })
        
        return {
            'fix_type': 'syntax_error_fix',
            'description': 'AI-powered syntax error fix',
            'changes': changes,
            'auto_applicable': True
        }
    
    async def _fix_configuration_error(self, analysis: Dict[str, Any], 
                                      context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix configuration errors"""
        
        changes = []
        
        config_files = [f for f in analysis.get('affected_files', [])
                       if any(ext in f for ext in ['.yaml', '.yml', '.json', '.toml', '.ini'])]
        
        for config_file in config_files:
            changes.append({
                'file': config_file,
                'action': 'update_config',
                'description': 'Fix configuration syntax or add missing keys'
            })
        
        return {
            'fix_type': 'configuration_fix',
            'description': 'Fixed configuration errors',
            'changes': changes,
            'auto_applicable': True
        }
    
    async def _fix_environment_issue(self, analysis: Dict[str, Any], 
                                    context: Dict[str, Any]) -> Dict[str, Any]:
        """Fix environment issues"""
        
        changes = [{
            'file': '.env.example',
            'action': 'add_env_var',
            'description': 'Add missing environment variables'
        }]
        
        return {
            'fix_type': 'environment_fix',
            'description': 'Fixed environment configuration',
            'changes': changes,
            'auto_applicable': True
        }
    
    async def _generic_fix(self, analysis: Dict[str, Any], 
                          context: Dict[str, Any]) -> Dict[str, Any]:
        """Generic fix for unknown errors"""
        
        return {
            'fix_type': 'generic_fix',
            'description': 'Attempted generic error resolution',
            'changes': [],
            'auto_applicable': False
        }
    
    async def _ai_fix_syntax_with_full_file(self, analysis: Dict[str, Any], 
                                            context: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to fetch entire file, analyze it, and generate complete corrected code"""
        
        if not self.client:
            return {}
        
        try:
            # Get the affected file
            affected_files = analysis.get('affected_files', [])
            if not affected_files:
                logger.warning("No affected files found in analysis")
                return {}
            
            # Focus on the first affected file (usually the main issue)
            target_file = affected_files[0]
            logger.info(f"Fetching file content from GitHub: {target_file}")
            
            # Fetch file content from GitHub
            file_content = await self._fetch_file_from_github(target_file, context)
            if not file_content:
                logger.error(f"Could not fetch file content for {target_file}")
                return {}
            
            logger.info(f"Successfully fetched {len(file_content)} characters from {target_file}")
            
            # Use AI to analyze and fix the entire file
            prompt = f"""You are a code fixing expert. A CI/CD pipeline failed due to a syntax error in this file.

File: {target_file}
Error Message: {analysis['error_message']}
Root Cause: {analysis.get('root_cause', 'Syntax error detected')}

Here is the COMPLETE file content:

```
{file_content}
```

Your task:
1. Analyze the ENTIRE file carefully
2. Identify ALL syntax errors (missing colons, parentheses, indentation issues, etc.)
3. Generate the COMPLETE CORRECTED file with ALL errors fixed
4. Return ONLY the corrected code, nothing else

IMPORTANT: Return the COMPLETE corrected file content. Do not explain, do not add comments about what you changed. Just return the fixed code."""

            if self.ai_provider == "groq":
                response = self.client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a code fixing expert. Return only the corrected code, no explanations."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.1
                )
                corrected_code = response.choices[0].message.content.strip()
                
            elif self.ai_provider == "openai":
                response = self.client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a code fixing expert. Return only the corrected code, no explanations."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=2000,
                    temperature=0.1
                )
                corrected_code = response.choices[0].message.content.strip()
                
            elif self.ai_provider == "gemini":
                model = self.client.GenerativeModel(settings.AI_MODEL)
                full_prompt = "You are a code fixing expert. Return only the corrected code, no explanations.\n\n" + prompt
                response = model.generate_content(full_prompt)
                corrected_code = response.text.strip()
                
            elif self.ai_provider == "ollama":
                response = self.client.chat(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a code fixing expert. Return only the corrected code, no explanations."},
                        {"role": "user", "content": prompt}
                    ]
                )
                corrected_code = response['message']['content'].strip()
            else:
                return {}
            
            # Clean up the response - remove markdown code blocks if present
            if '```python' in corrected_code:
                corrected_code = corrected_code.split('```python')[1].split('```')[0].strip()
            elif '```' in corrected_code:
                corrected_code = corrected_code.split('```')[1].split('```')[0].strip()
            
            logger.info(f"AI generated corrected code ({len(corrected_code)} characters)")
            
            # Return the fix with complete file content
            return {
                'fix_type': 'syntax_error_fix',
                'description': f'AI-generated complete fix for {target_file}',
                'changes': [{
                    'file': target_file,
                    'action': 'replace_entire_file',
                    'description': f'Replace entire file with AI-corrected version',
                    'code_snippet': corrected_code
                }],
                'auto_applicable': True
            }
        
        except Exception as e:
            logger.error(f"AI full file fix failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return {}
    
    async def _fetch_file_from_github(self, file_path: str, context: Dict[str, Any]) -> str:
        """Fetch file content from GitHub repository"""
        try:
            import requests
            from app.core.config import settings
            
            # Extract repository info from context
            repository = context.get('repository', '')
            branch = context.get('branch', 'main')
            
            if not repository:
                logger.error("No repository information in context")
                return ""
            
            # GitHub API URL for file content
            api_url = f"https://api.github.com/repos/{repository}/contents/{file_path}"
            
            headers = {
                'Accept': 'application/vnd.github.v3.raw',
                'Authorization': f'token {settings.GITHUB_TOKEN}'
            }
            
            params = {'ref': branch}
            
            logger.info(f"Fetching from GitHub: {api_url}?ref={branch}")
            
            response = requests.get(api_url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                return response.text
            else:
                logger.error(f"GitHub API error: {response.status_code} - {response.text}")
                return ""
        
        except Exception as e:
            logger.error(f"Failed to fetch file from GitHub: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return ""
    
    async def _ai_generate_fix(self, analysis: Dict[str, Any], 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to generate specific fix"""
        
        if not self.client:
            return {}
            
        try:
            prompt = f"""Generate a specific fix for this CI/CD failure:

Error Category: {analysis['error_category']}
Error Message: {analysis['error_message']}
Root Cause: {analysis.get('root_cause', 'Unknown')}
Affected Files: {', '.join(analysis.get('affected_files', [])[:5])}

Provide a JSON response with:
{{
  "changes": [
    {{
      "file": "path/to/file",
      "action": "specific_action",
      "description": "what to change",
      "code_snippet": "actual code change if applicable"
    }}
  ]
}}

Keep it practical and executable."""

            if self.ai_provider == "ollama":
                response = self.client.chat(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a CI/CD fix automation expert. Respond only with valid JSON."},
                        {"role": "user", "content": prompt}
                    ]
                )
                content = response['message']['content'].strip()
                
            elif self.ai_provider == "openai":
                response = self.client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a CI/CD fix automation expert. Respond only with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.2
                )
                content = response.choices[0].message.content.strip()
                
            elif self.ai_provider == "groq":
                response = self.client.chat.completions.create(
                    model=settings.AI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are a CI/CD fix automation expert. Respond only with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=500,
                    temperature=0.2
                )
                content = response.choices[0].message.content.strip()
                
            elif self.ai_provider == "gemini":
                model = self.client.GenerativeModel(settings.AI_MODEL)
                full_prompt = "You are a CI/CD fix automation expert. Respond only with valid JSON.\n\n" + prompt
                response = model.generate_content(full_prompt)
                content = response.text.strip()
                
            elif self.ai_provider == "anthropic":
                response = self.client.messages.create(
                    model=settings.AI_MODEL,
                    max_tokens=500,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                content = response.content[0].text.strip()
            else:
                return {}
            
            # Extract JSON from response
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            return json.loads(content)
        
        except Exception as e:
            logger.error(f"AI fix generation failed: {e}")
            return {}
