
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import ast
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Change Impact Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "null",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    file_path: str
    changed_function: str


@app.get("/")
def home():
    return {"message": "AI Change Impact Analyzer API is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    path = Path(request.file_path)

    if not path.is_file() or path.suffix != ".py":
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid Python file path."
        )

    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        raise HTTPException(
            status_code=400,
            detail="Could not parse this Python file."
        )

    callers = []

    class CallVisitor(ast.NodeVisitor):
        def __init__(self):
            self.current_function = None

        def visit_FunctionDef(self, node):
            previous = self.current_function
            self.current_function = node.name
            self.generic_visit(node)
            self.current_function = previous

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_Call(self, node):
            if (
                isinstance(node.func, ast.Name)
                and node.func.id == request.changed_function
                and self.current_function
                and self.current_function != request.changed_function
            ):
                if self.current_function not in callers:
                    callers.append(self.current_function)
            self.generic_visit(node)

    CallVisitor().visit(tree)

    return {
        "changed_function": request.changed_function,
        "potentially_affected_functions": callers,
        "impact_level": "HIGH" if callers else "UNKNOWN"
    }