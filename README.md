# 🤖 AutoDev-Agent: Autonomous AI Code Auditor & Refactoring Engine

An enterprise-grade, agentic AI platform built with **Python**, **LangGraph**, and **Streamlit** that automatically audits Python codebases, extracts AST architecture, executes code in a secure sandbox, and performs autonomous refactoring and unit test generation.

---

## 🌟 Key Features

- 🌳 **AST Code Parsing (`core/ast_parser.py`)**: Uses Python's Abstract Syntax Trees (AST) to map code architecture, extracting classes, functions, and imports.
- 🛡️ **Autonomous Security & Quality Auditor (`core/agents.py`)**: Leverages LLMs to detect logical bugs, OWASP security vulnerabilities, and code code health scores.
- ⚡ **Isolated Code Execution Sandbox (`core/sandbox.py`)**: Runs target code safely inside an isolated execution environment, capturing stdout and stderr.
- 🛠️ **Autonomous Refactoring Engine**: Self-corrects bad code, applies clean architecture patterns, and automatically generates comprehensive PyTest unit tests.
- 💻 **Interactive Web UI (`ui/app.py`)**: Built with Streamlit for seamless user interaction, configuration, and real-time visualization.

---

## 🏗️ System Architecture

```text
+-----------------------+
|  User Code Input (UI) |
+-----------+-----------+
            |
            v
+-----------------------+      +-----------------------+
| AST Structural Parser | ---> | Isolated Sandbox Exec |
+-----------+-----------+      +-----------+-----------+
            |                              |
            +--------------+---------------+
                           |
                           v
            +------------------------------+
            | Multi-Agent LLM Refactoring  |
            +--------------+---------------+
                           |
                           v
            +------------------------------+
            | Audited Code + Unit Tests    |
            +------------------------------+
