import ast
import os
from git import Repo


def get_changed_files(repo_path):
    repo = Repo(repo_path)

    changed_files = []

    # Modified files
    for item in repo.index.diff(None):
        changed_files.append(item.a_path)

    # New files
    for file in repo.untracked_files:
        changed_files.append(file)

    return changed_files


def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    functions = []
    classes = []
    dependencies = {}

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)
            dependencies[node.name] = []

            for child in ast.walk(node):
                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):
                        called_function = child.func.id

                        if called_function not in dependencies[node.name]:
                            dependencies[node.name].append(called_function)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

    return functions, classes, dependencies


def analyze_repository(repo_path):

    changed_files = get_changed_files(repo_path)

    print("\n===================================")
    print("     AI CHANGE IMPACT ANALYZER")
    print("===================================")

    if not changed_files:
        print("\nNo changes detected.")
        return

    for file in changed_files:

        print(f"\nFile: {file}")

        if not file.endswith(".py"):
            print("  Skipped (not a Python file)")
            continue

        full_path = os.path.join(repo_path, file)

        functions, classes, dependencies = analyze_file(full_path)

        print("\n  Functions:")

        for function in functions:
            print(f"    - {function}()")

        print("\n  Classes:")

        if classes:
            for class_name in classes:
                print(f"    - {class_name}")
        else:
            print("    - None")

        print("\n  Dependencies:")

        for function, calls in dependencies.items():

            if calls:
                print(f"    {function}()")
                for call in calls:
                    print(f"      -> calls {call}()")
            else:
                print(f"    {function}() -> None")


if __name__ == "__main__":

    repo_path = input("Enter Git repository path: ")

    analyze_repository(repo_path)