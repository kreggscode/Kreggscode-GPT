"""
File Manager for Kreggscode GPT
Handles automatic file creation and management with cross-platform support
"""

import os
import re
import stat
from pathlib import Path
from typing import Optional, Tuple, List


class FileManager:
    """Manages file creation and organization"""
    
    def __init__(self, output_dir: str = "generated"):
        """
        Initialize File Manager
        
        Args:
            output_dir: Directory to save generated files (default: 'generated')
        """
        self.output_dir = Path(output_dir)
        # Create directory with proper permissions (cross-platform)
        try:
            self.output_dir.mkdir(exist_ok=True, parents=True)
            # Set permissions on Unix-like systems (ignored on Windows)
            if os.name != 'nt':
                os.chmod(self.output_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IROTH | stat.S_IXOTH)
        except PermissionError:
            # Fallback to user's home directory if permission denied
            import tempfile
            self.output_dir = Path(tempfile.gettempdir()) / "kreggscode_gpt" / output_dir
            self.output_dir.mkdir(exist_ok=True, parents=True)
        
        # File extension mappings
        self.extension_map = {
            'python': '.py',
            'javascript': '.js',
            'typescript': '.ts',
            'html': '.html',
            'css': '.css',
            'java': '.java',
            'cpp': '.cpp',
            'c': '.c',
            'rust': '.rs',
            'go': '.go',
            'ruby': '.rb',
            'php': '.php',
            'swift': '.swift',
            'kotlin': '.kt',
            'sql': '.sql',
            'json': '.json',
            'xml': '.xml',
            'yaml': '.yaml',
            'markdown': '.md',
            'text': '.txt',
            'shell': '.sh',
            'bash': '.sh',
            'powershell': '.ps1',
            'batch': '.bat'
        }
    
    def detect_file_request(self, text: str) -> bool:
        """
        Detect if the user is requesting file creation
        
        Args:
            text: User's input text
            
        Returns:
            True if file creation is requested
        """
        keywords = [
            'create file', 'make file', 'generate file',
            'create a file', 'make a file', 'save to file',
            'write file', 'create code', 'generate code',
            'save as', 'export to', 'write to file'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    def extract_code_blocks(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Extract code blocks from markdown-formatted text
        
        Args:
            text: Text containing code blocks
            
        Returns:
            List of tuples (language, code, filename_hint)
        """
        # Pattern to match markdown code blocks with optional language
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        
        results = []
        for lang, code in matches:
            lang = lang.lower() if lang else 'text'
            # Try to extract filename from comments
            filename_hint = self._extract_filename_from_code(code, lang)
            results.append((lang, code.strip(), filename_hint))
        
        return results
    
    def _extract_filename_from_code(self, code: str, lang: str) -> Optional[str]:
        """
        Try to extract filename from code comments
        
        Args:
            code: The code content
            lang: Programming language
            
        Returns:
            Filename if found, None otherwise
        """
        # Look for filename in first few lines
        lines = code.split('\n')[:5]
        
        for line in lines:
            # Check for common filename patterns in comments
            if 'filename:' in line.lower() or 'file:' in line.lower():
                # Extract the filename
                match = re.search(r'(?:filename|file):\s*([^\s]+)', line, re.IGNORECASE)
                if match:
                    return match.group(1)
        
        return None
    
    def save_file(self, content: str, filename: Optional[str] = None, 
                  language: Optional[str] = None) -> str:
        """
        Save content to a file
        
        Args:
            content: File content
            filename: Optional filename
            language: Optional language/file type
            
        Returns:
            Path to saved file
        """
        # Determine file extension
        if filename:
            # Use provided filename
            filepath = self.output_dir / filename
        else:
            # Generate filename
            extension = self._get_extension(language)
            counter = 1
            while True:
                filename = f"generated_{counter}{extension}"
                filepath = self.output_dir / filename
                if not filepath.exists():
                    break
                counter += 1
        
        # Ensure parent directory exists with proper permissions
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            # Fallback to temp directory
            import tempfile
            filepath = Path(tempfile.gettempdir()) / "kreggscode_gpt" / filepath.name
            filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file with proper encoding
        try:
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            
            # Make shell scripts executable on Unix-like systems
            if filepath.suffix in ['.sh', '.bash'] and os.name != 'nt':
                os.chmod(filepath, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        except Exception as e:
            raise IOError(f"Failed to write file {filepath}: {str(e)}")
        
        return str(filepath)
    
    def _get_extension(self, language: Optional[str]) -> str:
        """
        Get file extension for a language
        
        Args:
            language: Programming language or file type
            
        Returns:
            File extension with dot
        """
        if not language:
            return '.txt'
        
        language = language.lower()
        return self.extension_map.get(language, '.txt')
    
    def process_ai_response(self, response: str, user_request: str) -> List[str]:
        """
        Process AI response and save any code blocks as files
        
        Args:
            response: AI's response text
            user_request: Original user request
            
        Returns:
            List of saved file paths
        """
        saved_files = []
        
        # Extract code blocks - ALWAYS save if code blocks are present
        code_blocks = self.extract_code_blocks(response)
        
        if not code_blocks:
            # No code blocks found - don't save anything
            return saved_files
        
        # Save each code block automatically
        for lang, code, filename_hint in code_blocks:
            filename = filename_hint or self._extract_filename_from_request(user_request)
            filepath = self.save_file(code, filename, lang)
            saved_files.append(filepath)
        
        return saved_files
    
    def _extract_filename_from_request(self, request: str) -> Optional[str]:
        """
        Try to extract filename from user request
        
        Args:
            request: User's request text
            
        Returns:
            Filename if found, None otherwise
        """
        # Look for quoted filenames
        match = re.search(r'["\']([^"\']+\.\w+)["\']', request)
        if match:
            return match.group(1)
        
        # Look for common patterns like "called X" or "named X"
        match = re.search(r'(?:called|named)\s+([^\s]+\.\w+)', request, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None
    
    def list_generated_files(self) -> List[str]:
        """
        List all generated files
        
        Returns:
            List of file paths
        """
        if not self.output_dir.exists():
            return []
        
        files = []
        for item in self.output_dir.rglob('*'):
            if item.is_file():
                files.append(str(item))
        
        return sorted(files)
    
    def clear_generated_files(self) -> int:
        """
        Clear all generated files
        
        Returns:
            Number of files deleted
        """
        count = 0
        if self.output_dir.exists():
            for item in self.output_dir.rglob('*'):
                if item.is_file():
                    item.unlink()
                    count += 1
        
        return count
