import ast
import os


def analyze_file(file_path):
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

    return {
        "file": os.path.basename(file_path),
        "functions": functions,
        "classes": classes,
    }


if __name__ == "__main__":
    file_path = input("Enter Python file path: ")

    result = analyze_file(file_path)

    print("\nCode Analysis Result")
    print("--------------------")
    print(f"File: {result['file']}")

    print("\nFunctions:")
    for function in result["functions"]:
        print(f"  - {function}")

    print("\nClasses:")
    for class_name in result["classes"]:
        print(f"  - {class_name}")