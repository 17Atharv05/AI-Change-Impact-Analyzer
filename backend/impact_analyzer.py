import ast
import os
from git import Repo


def get_changed_files(repo_path):
    repo = Repo(repo_path)

    changed_files = []

    for item in repo.index.diff(None):
        changed_files.append(item.a_path)

    for file in repo.untracked_files:
        changed_files.append(file)

    return changed_files


def analyze_python_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    functions = []
    classes = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return functions, classes


if __name__ == "__main__":
    repo_path = input("Enter Git repository path: ")

    changed_files = get_changed_files(repo_path)

    print("\nAI Change Impact Analyzer")
    print("========================")

    for file in changed_files:
        print(f"\nFile: {file}")

        if file.endswith(".py"):
            full_path = os.path.join(repo_path, file)

            functions, classes = analyze_python_file(full_path)

            print("Functions:")
            for function in functions:
                print(f"  - {function}")

            print("Classes:")
            for class_name in classes:
                print(f"  - {class_name}")