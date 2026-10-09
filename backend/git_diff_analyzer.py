from git import Repo
import re


def get_changed_functions(repo_path):
    repo = Repo(repo_path)

    diff = repo.git.diff("-U0")

    changed_functions = []

    current_file = None
    current_function = None

    for line in diff.splitlines():

        # Detect changed file
        if line.startswith("+++ b/"):
            current_file = line[6:]

        # Detect function context
        if line.startswith("@@"):
            match = re.search(r"@@.*@@\s*(.*)", line)

            if match:
                context = match.group(1).strip()

                function_match = re.search(
                    r"(?:def|async def)\s+(\w+)",
                    context
                )

                if function_match:
                    current_function = function_match.group(1)

        # Detect actual code change
        if (line.startswith("+") or line.startswith("-")) \
                and not line.startswith("+++") \
                and not line.startswith("---"):

            if current_file and current_function:

                changed_functions.append(
                    (current_file, current_function)
                )

    return list(set(changed_functions))


if __name__ == "__main__":

    repo_path = input("Enter Git repository path: ")

    changes = get_changed_functions(repo_path)

    print("\n===================================")
    print("       CHANGED FUNCTIONS")
    print("===================================")

    if changes:

        for file, function in changes:
            print(f"\nFile: {file}")
            print(f"Function: {function}()")

    else:
        print("\nNo changed functions detected.")