import os
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class AuditReport(BaseModel):
    """Schema for structured code audit output."""
    security_vulnerabilities: list[str] = Field(description="List of security risks and OWASP vulnerabilities.")
    bugs_and_issues: list[str] = Field(description="List of logical bugs or potential errors.")
    refactoring_suggestions: list[str] = Field(description="Actionable recommendations for clean code.")
    score: int = Field(description="Overall code health score from 0 to 100.")

class AutoDevAgents:
    """Agentic Engine for Code Auditing, Refactoring, and Test Generation."""
    def __init__(self, model_name: str = "gpt-4o", api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "mock-key")
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.2,
            api_key=self.api_key
        )

    def audit_code(self, code: str) -> Dict[str, Any]:
        """Agent 1: Security & Quality Auditor."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert Senior Code Auditor. Analyze the provided Python code for bugs, security risks, and optimization opportunities."),
            ("user", "Code to audit:\n```python\n{code}\n```")
        ])
        
        try:
            structured_llm = self.llm.with_structured_output(AuditReport)
            chain = prompt | structured_llm
            result = chain.invoke({"code": code})
            return result.model_dump()
        except Exception as e:
            return {
                "security_vulnerabilities": ["Audit failed due to missing API key or connection error."],
                "bugs_and_issues": [str(e)],
                "refactoring_suggestions": ["Configure OPENAI_API_KEY to run live agent analysis."],
                "score": 0
            }

    def refactor_and_test(self, code: str, audit_report: Dict[str, Any]) -> str:
        """Agent 2: Autonomous Refactoring & Unit Test Generator."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an elite Autonomous Software Engineer. Refactor the code to fix all issues in the audit report, and write clean pytest unit tests."),
            ("user", "Original Code:\n```python\n{code}\n```\n\nAudit Findings:\n{report}\n\nProvide the complete refactored code along with unit tests.")
        ])
        
        try:
            chain = prompt | self.llm
            response = chain.invoke({"code": code, "report": str(audit_report)})
            return response.content
        except Exception as e:
            return f"# Refactoring failed: {str(e)}"
