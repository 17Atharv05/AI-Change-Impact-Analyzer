import ast


class DependencyAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.current_function = None
        self.dependencies = {}

    def visit_FunctionDef(self, node):
        previous_function = self.current_function
        self.current_function = node.name
        self.dependencies[node.name] = []

        self.generic_visit(node)

        self.current_function = previous_function

    def visit_Call(self, node):
        if self.current_function and isinstance(node.func, ast.Name):
            called_function = node.func.id

            if called_function not in self.dependencies[self.current_function]:
                self.dependencies[self.current_function].append(called_function)

        self.generic_visit(node)


def analyze_dependencies(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    tree = ast.parse(source_code)

    analyzer = DependencyAnalyzer()
    analyzer.visit(tree)

    return analyzer.dependencies


if __name__ == "__main__":
    file_path = input("Enter Python file path: ")

    dependencies = analyze_dependencies(file_path)

    print("\nFunction Dependencies")
    print("=====================")

    for function, calls in dependencies.items():
        print(f"\n{function}()")

        if calls:
            for call in calls:
                print(f"  -> calls {call}()")
        else:
            print("  -> no function calls")