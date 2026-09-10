import streamlit as st
import sys
import os

# Add parent directory to path so core modules can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.ast_parser import analyze_code_structure
from core.agents import AutoDevAgents
from core.sandbox import CodeSandbox

st.set_page_config(
    page_title="AutoDev-Agent | Autonomous AI Code Auditor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AutoDev-Agent")
st.caption("Autonomous AI Code Auditor & Refactoring Engine")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
model_choice = st.sidebar.selectbox("Model", ["gpt-4o", "gpt-4o-mini"])

# Sample code for testing
sample_code = '''def calculate_total(prices):
    total = 0
    for p in prices:
        total += p
    return total

# Potential issue: hardcoded secret
db_password = "admin_password123"
'''

st.subheader("1. Input Python Code")
code_input = st.text_area("Paste Python code to analyze:", value=sample_code, height=200)

if st.button("🚀 Analyze & Audit Code", type="primary"):
    if not code_input.strip():
        st.warning("Please provide Python code to analyze.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌳 AST Structural Analysis")
            ast_results = analyze_code_structure(code_input)
            if ast_results["status"] == "success":
                st.json({
                    "Classes": ast_results["classes"],
                    "Functions": ast_results["functions"],
                    "Imports": ast_results["imports"]
                })
            else:
                st.error(f"Syntax Error: {ast_results.get('error')}")

        with col2:
            st.subheader("⚡ Sandbox Code Execution")
            sandbox = CodeSandbox()
            exec_result = sandbox.execute_code(code_input)
            if exec_result["success"]:
                st.success("Execution Successful!")
                st.code(exec_result["stdout"] or "No output printed.")
            else:
                st.error("Execution Error / Failed:")
                st.code(exec_result["stderr"])

        st.markdown("---")
        st.subheader("🔍 AI Agent Audit & Refactoring")
        
        if not api_key:
            st.info("💡 Enter your OpenAI API key in the sidebar for live AI Agent auditing.")
        else:
            agents = AutoDevAgents(model_name=model_choice, api_key=api_key)
            
            with st.spinner("Agent 1: Auditing security and code quality..."):
                audit = agents.audit_code(code_input)
                st.write(f"**Code Health Score:** {audit.get('score', 'N/A')}/100")
                
                st.markdown("##### 🛡️ Security Vulnerabilities")
                for vuln in audit.get("security_vulnerabilities", []):
                    st.write(f"- {vuln}")
                    
                st.markdown("##### 🐛 Bugs & Issues")
                for bug in audit.get("bugs_and_issues", []):
                    st.write(f"- {bug}")

            with st.spinner("Agent 2: Generating refactored code & unit tests..."):
                refactored = agents.refactor_and_test(code_input, audit)
                st.markdown("##### 🛠️ Refactored Code & Unit Tests")
                st.code(refactored, language="python")
