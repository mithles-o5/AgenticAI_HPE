import os

possible_paths = [
    r"C:\Users\ELCOT\AppData\Roaming\Claude\logs",
    r"C:\Users\ELCOT\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\logs",
    r"C:\Users\ELCOT\AppData\Local\Claude\logs"
]

def find_logs():
    for p in possible_paths:
        expanded = os.path.expandvars(p)
        if os.path.exists(expanded):
            print(f"Found logs directory: {expanded}")
            files = os.listdir(expanded)
            print(f"Log files found: {files}")
            # Print last lines of the most recent log file
            log_files = [os.path.join(expanded, f) for f in files if f.endswith(".log")]
            if log_files:
                newest = max(log_files, key=os.path.getmtime)
                print(f"\nLast 15 lines of newest log file ({os.path.basename(newest)}):")
                with open(newest, "r", encoding="utf-8", errors="ignore") as lf:
                    lines = lf.readlines()
                    for line in lines[-15:]:
                        print(line.strip())
            return
    print("No Claude Desktop log directories found.")

if __name__ == "__main__":
    find_logs()
