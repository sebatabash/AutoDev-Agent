import sys
import subprocess
import tempfile
import os
from typing import Dict, Any

class CodeSandbox:
    """Secure isolation sandbox for running generated Python code and pytest suites."""
    
    def __init__(self, timeout_seconds: int = 10):
        self.timeout = timeout_seconds

    def execute_code(self, code_content: str) -> Dict[str, Any]:
        """Runs Python code string in a temporary isolated environment and returns execution status."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code_content)
            temp_path = temp_file.name

        try:
            result = subprocess.run(
                [sys.executable, temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Execution timed out after {self.timeout} seconds.",
                "exit_code": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "exit_code": -1
            }
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
