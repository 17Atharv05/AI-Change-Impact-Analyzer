from git import Repo


def get_changed_files(repo_path):
    repo = Repo(repo_path)

    changed_files = []

    # Modified and deleted tracked files
    for item in repo.index.diff(None):
        changed_files.append(item.a_path)

    # New untracked files
    for file in repo.untracked_files:
        changed_files.append(file)

    return changed_files


if __name__ == "__main__":
    repo_path = input("Enter Git repository path: ")

    files = get_changed_files(repo_path)

    print("\nChanged Files")
    print("-------------")

    if not files:
        print("No changes found.")
    else:
        for file in files:
            print(f"- {file}")