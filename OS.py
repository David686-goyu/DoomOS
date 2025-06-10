import os
import time

# Simple in-memory file system
file_system = {"/": {}}
current_path = ["/"]

def get_path():
    return "/".join(current_path).replace("//", "/")

def get_folder():
    folder = file_system["/"]
    for part in current_path[1:]:
        folder = folder[part]
    return folder

def list_dir():
    folder = get_folder()
    if not folder:
        print("Directory is empty.")
    else:
        for name in folder:
            print(name)

def make_folder(name):
    folder = get_folder()
    if name in folder:
        print("Folder already exists.")
    else:
        folder[name] = {}

def change_dir(name):
    global current_path
    if name == "..":
        if len(current_path) > 1:
            current_path.pop()
    elif name in get_folder() and isinstance(get_folder()[name], dict):
        current_path.append(name)
    else:
        print("Directory not found.")

def create_file(name):
    folder = get_folder()
    if name in folder:
        print("File already exists.")
    else:
        content = input("Enter file content: ")
        folder[name] = content

def read_file(name):
    folder = get_folder()
    if name in folder and isinstance(folder[name], str):
        print(f"\n--- {name} ---\n{folder[name]}\n")
    else:
        print("File not found.")

def show_help():
    print("""
Available commands:
  ls             - List files and folders
  cd <folder>    - Change directory
  cd ..          - Go up a directory
  mkdir <name>   - Create a folder
  touch <name>   - Create a file
  read <name>    - Read a file
  doom           - Run DOOM (launch or mini demo)
  help           - Show this help
  exit           - Shut down PyLinuxOS
""")

def boot():
    print("Booting DoomOS...")
    time.sleep(1)
    print("Starting services...")
    time.sleep(1)
    print("Welcome to DoomOS Terminal\nType 'help' to begin.\n")

def run_doom():
    # Try to find and launch a real DOOM executable
    doom_paths = [
        "/usr/games/gzdoom",  # Linux common
        "/usr/local/bin/gzdoom",
        "C:\\Program Files\\GZDoom\\gzdoom.exe",  # Windows example
        "./gzdoom.exe"
    ]

    for path in doom_paths:
        if os.path.exists(path):
            print(f"Launching DOOM from {path} ...")
            os.system(f'"{path}"')
            return

    # Fallback: simple text-based DOOM demo
    print("\nDOOM executable not found. Running mini DOOM demo...\n")
    mini_doom_demo()

def mini_doom_demo():
    print("""
Welcome to Mini DOOM Demo!
You're in a dark room. A monster appears!

Commands:
  shoot  - Shoot the monster
  run    - Run away
  help   - Show commands
  exit   - Exit DOOM demo
""")

    monster_alive = True
    while True:
        cmd = input("DOOM > ").strip().lower()
        if cmd == "shoot":
            if monster_alive:
                print("You shoot the monster. It dies. You win!")
                monster_alive = False
            else:
                print("No monsters left to shoot.")
        elif cmd == "run":
            print("You run away safely. Game over.")
            break
        elif cmd == "help":
            print("shoot, run, help, exit")
        elif cmd == "exit":
            print("Exiting DOOM demo...")
            break
        else:
            print("Unknown command.")

def main():
    boot()
    while True:
        cmd = input(f"{get_path()} $ ").strip().split()
        if not cmd:
            continue
        action = cmd[0]

        if action == "help":
            show_help()
        elif action == "ls":
            list_dir()
        elif action == "cd":
            if len(cmd) > 1:
                change_dir(cmd[1])
            else:
                print("Usage: cd <folder>")
        elif action == "mkdir":
            if len(cmd) > 1:
                make_folder(cmd[1])
            else:
                print("Usage: mkdir <folder>")
        elif action == "touch":
            if len(cmd) > 1:
                create_file(cmd[1])
            else:
                print("Usage: touch <filename>")
        elif action == "read":
            if len(cmd) > 1:
                read_file(cmd[1])
            else:
                print("Usage: read <filename>")
        elif action == "doom":
            run_doom()
        elif action == "exit":
            print("Shutting down DoomOS...")
            break
        else:
            print("Command not found. Type 'help'.")

if __name__ == "__main__":
    main()
