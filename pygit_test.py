import pygit2

repo_path = r"C:\Users\Yogendra Fegade\python-mini-projects"

repo = pygit2.Repository(repo_path)

commit = repo.head.peel()

print("Latest Commit ID:", commit.id)
print("Message:", commit.message)

#  Check number of parents
parent_count = len(commit.parents)

print("Number of Parents:", parent_count)

if parent_count > 1:
    print("This is a MERGE commit")
else:
    print("This is a NORMAL commit")


#  Get parents
parent1 = commit.parents[0]   # main branch before merge
parent2 = commit.parents[1]   # merged branch (test)

# Get trees (snapshot of files)
tree_old = parent1.tree
tree_new = commit.tree

#  Generate diff
diff = repo.diff(tree_old, tree_new)

print("\nDiff generated successfully!\n")

print("Changed Files:\n")

for patch in diff:
    file_path = patch.delta.new_file.path or patch.delta.old_file.path

    #  Detect change type
    if patch.delta.status == pygit2.GIT_DELTA_ADDED:
        change_type = "A"
    elif patch.delta.status == pygit2.GIT_DELTA_DELETED:
        change_type = "D"
    else:
        change_type = "M"

    print(f"{change_type} {file_path}")

print("\nLine Changes:\n")

for patch in diff:
    file_path = patch.delta.new_file.path or patch.delta.old_file.path
    print(f"\nFile: {file_path}")

    for hunk in patch.hunks:
        old_line_no = hunk.old_start
        new_line_no = hunk.new_start

        for line in hunk.lines:

            content = line.content.strip()

            #  Removed line
            if line.origin == '-':
                if content:
                    print(f"Line {old_line_no} (-): {content}")
                old_line_no += 1

            #  Added line
            elif line.origin == '+':
                if content:
                    print(f"Line {new_line_no} (+): {content}")
                new_line_no += 1

            #  Context line
            else:
                old_line_no += 1
                new_line_no += 1