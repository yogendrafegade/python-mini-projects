import pygit2
import os
from variable import REPO_PATH

# Initialize repository
try:
    repo = pygit2.Repository(REPO_PATH)
except pygit2.GitError:
    print(f"Error: Could not find a valid Git repository at {REPO_PATH}")
    exit()

# Get the latest commit
commit = repo.head.peel()

# --- Analysis Logic ---
parent_count = len(commit.parents)
commit_type = "MERGE commit" if parent_count > 1 else "NORMAL commit"

print(f"--- Git Analysis Tool ---")
print(f"Message: {commit.message.strip()}")
print(f"Type:    {commit_type}")
print("-" * 30)

# Determine the trees to compare
if parent_count > 0:
    # Compare against the first parent (main line of history)
    tree_old = commit.parents[0].tree
    tree_new = commit.tree
    diff = repo.diff(tree_old, tree_new)
else:
    # Handle initial commit (no parents)
    # We compare an empty tree to the current commit tree
    diff = commit.tree.diff_to_tree()

# --- File Level Output ---
print("\nChanged Files:")
for patch in diff:
    status_map = {
        pygit2.GIT_DELTA_ADDED: "A",
        pygit2.GIT_DELTA_DELETED: "D",
        pygit2.GIT_DELTA_MODIFIED: "M",
        pygit2.GIT_DELTA_RENAMED: "R"
    }
    status = status_map.get(patch.delta.status, "?")
    file_path = patch.delta.new_file.path
    print(f"[{status}] {file_path}")

# --- Line Level Output ---
print("\nLine Changes:")
for patch in diff:
    file_path = patch.delta.new_file.path
    print(f"\nFile: {file_path}")

    for hunk in patch.hunks:
        # Pointers for tracking line numbers
        old_ln = hunk.old_start
        new_ln = hunk.new_start

        for line in hunk.lines:
            content = line.content.strip()
            
            # Identify the change type
            if line.origin == '-':
                if content: # Only print non-empty lines
                    print(f"Line {old_ln} (-): {content}")
                old_ln += 1
            
            elif line.origin == '+':
                if content:
                    print(f"Line {new_ln} (+): {content}")
                new_ln += 1
            
            else:
                # This is a context line (no change)
                old_ln += 1
                new_ln += 1