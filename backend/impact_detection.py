import ast


def get_function_dependencies(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    dependencies = {}

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

            function_name = node.name
            dependencies[function_name] = []

            for child in ast.walk(node):

                if isinstance(child, ast.Call):
                    if isinstance(child.func, ast.Name):

                        called_function = child.func.id

                        if called_function not in dependencies[function_name]:
                            dependencies[function_name].append(called_function)

    return dependencies


def find_impact(dependencies, changed_function):

    affected_functions = []

    for function, calls in dependencies.items():

        if changed_function in calls:
            affected_functions.append(function)

    return affected_functions


if __name__ == "__main__":

    file_path = input("Enter Python file path: ")
    changed_function = input("Enter changed function name: ")

    dependencies = get_function_dependencies(file_path)

    affected_functions = find_impact(
        dependencies,
        changed_function
    )

    print("\n===================================")
    print("        IMPACT ANALYSIS")
    print("===================================")

    print(f"\nChanged Function:")
    print(f"  {changed_function}()")

    print("\nPotentially Affected Functions:")

    if affected_functions:

        for function in affected_functions:
            print(f"  HIGH → {function}()")

        print("\nReason:")
        print(
            f"  The affected functions directly call "
            f"{changed_function}()."
        )

    else:
        print("  No direct dependencies found.")