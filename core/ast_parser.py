import ast

class CodeASTAnalyzer(ast.NodeVisitor):
    """Parses Python AST to extract structural insights (Classes, Functions, Imports)."""
    def __init__(self):
        self.classes = []
        self.functions = []
        self.imports = []

    def visit_ClassDef(self, node):
        self.classes.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)

def analyze_code_structure(code_content: str) -> dict:
    """Analyze Python code string and return structured architectural components."""
    try:
        tree = ast.parse(code_content)
        analyzer = CodeASTAnalyzer()
        analyzer.visit(tree)
        return {
            "status": "success",
            "classes": analyzer.classes,
            "functions": analyzer.functions,
            "imports": list(set(analyzer.imports))
        }
    except SyntaxError as e:
        return {
            "status": "syntax_error",
            "error": str(e)
        }
