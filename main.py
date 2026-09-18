import subprocess
import os

def run_script(script_name):
    print(f"--- Running {script_name} ---")
    result = subprocess.run(["python3", script_name], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in {script_name}:")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        return False
    print(result.stdout)
    return True

def push_to_github():
    print("--- Pushing to GitHub ---")
    if not os.path.exists(".git"):
        print("Git repository not initialized. Skipping push. (Run `git init` and `git remote add` to set this up).")
        return
        
    commands = [
        ["git", "add", "index.html"],
        ["git", "commit", "-m", "Daily Escape Hatch update"],
        ["git", "push", "origin", "main"]
    ]
    
    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 and "nothing to commit" not in result.stdout:
            print(f"Git error: {' '.join(cmd)}")
            print(result.stderr)
            return
    print("Successfully pushed to GitHub.")

if __name__ == "__main__":
    print("Starting Escape Hatch Daily Run...")
    
    if run_script("fetcher.py") and run_script("filter.py") and run_script("builder.py"):
        push_to_github()
        print("Daily run complete. You are caught up.")
    else:
        print("Daily run failed.")
