import os


def find_symlinks(repo_path):
    symlinks = []
    for root, dirs, files in os.walk(repo_path):
        for name in dirs + files:
            full_path = os.path.join(root, name)
            if os.path.islink(full_path):
                # Get the relative path to the repo
                rel_path = os.path.relpath(full_path, repo_path)
                symlinks.append(rel_path)
    return symlinks


def add_to_gitignore(repo_path, symlinks):
    gitignore_path = os.path.join(repo_path, ".gitignore")
    existing_entries = set()

    # Read existing .gitignore entries
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as gitignore:
            existing_entries = set(line.strip() for line in gitignore.readlines())

    # Add new entries
    with open(gitignore_path, "a") as gitignore:
        for link in symlinks:
            if link not in existing_entries:
                gitignore.write(f"{link}\n")
                print(f"Added to .gitignore: {link}")


def main():
    # Define the path to your repository
    repo_path = os.path.abspath(
        "."
    )  # Change this to your repo path if not running from the repo's root

    symlinks = find_symlinks(repo_path)
    if symlinks:
        add_to_gitignore(repo_path, symlinks)
    else:
        print("No symlinks found in the repository.")


if __name__ == "__main__":
    main()
