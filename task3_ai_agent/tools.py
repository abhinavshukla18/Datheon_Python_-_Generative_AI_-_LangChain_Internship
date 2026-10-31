import ast
import operator
import os

from ddgs import DDGS
from langchain_core.tools import tool

OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        left = _eval(node.left)
        right = _eval(node.right)
        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("Exponent too large")
        return OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.operand))
    raise ValueError("Unsupported expression")


@tool
def web_search(query: str) -> str:
    """Search the web for current information. Input is a search query."""
    try:
        results = DDGS().text(query, max_results=4)
    except Exception as e:
        return f"Search failed: {e}"
    if not results:
        return "No results found."
    return "\n\n".join(f"{r['title']}\n{r['body']}\n{r['href']}" for r in results)


@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression such as '(25 * 4) + 10 / 2'. Supports + - * / ** %."""
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except Exception as e:
        return f"Calculation error: {e}"


@tool
def read_file(file_name: str) -> str:
    """Read a local text file from the 'files' folder. Input is the file name, for example 'notes.txt'."""
    safe_path = os.path.join("files", os.path.basename(file_name))
    if not os.path.isfile(safe_path):
        return f"File not found: {file_name}"
    with open(safe_path, encoding="utf-8") as f:
        return f.read()[:5000]