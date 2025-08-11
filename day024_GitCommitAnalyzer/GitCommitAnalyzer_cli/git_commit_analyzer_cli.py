# git_commit_analyzer_cli.py

### === Import ===
import subprocess

### === Functions ===
def get_git_log():
    git_log = subprocess.run(
        ["git", "status"],
        capture_output=True,
        text=True
    )
    return git_log

print("output: \n", get_git_log().stdout)
print("+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=")
print("Error: \n", get_git_log().stderr)