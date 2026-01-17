import os
import hashlib
import time
from datetime import datetime
import difflib
import shutil

def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None
    return sha256_hash.hexdigest()

def create_baseline(baseline_file, folder):
    with open(baseline_file, "w", encoding="utf-8") as bf:
        for root, dirs, files in os.walk(folder):
            for file in files:
                full_path = os.path.join(root, file)
                if os.path.abspath(full_path) != os.path.abspath(baseline_file):
                    file_hash = calculate_file_hash(full_path)
                    if file_hash:
                        bf.write(f"{full_path}|{file_hash}\n")

def load_baseline(baseline_file):
    baseline_hashes = {}
    if os.path.exists(baseline_file):
        with open(baseline_file, "r", encoding="utf-8") as bf:
            for line in bf:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    path, file_hash = parts
                    baseline_hashes[path] = file_hash
    return baseline_hashes

def save_baseline(baseline_file, baseline_hashes):
    with open(baseline_file, "w", encoding="utf-8") as bf:
        for path, file_hash in baseline_hashes.items():
            bf.write(f"{path}|{file_hash}\n")

def show_text_diff(old_content, new_content, oldfile, newfile):
    diff = difflib.unified_diff(
        old_content, new_content,
        fromfile=oldfile,
        tofile=newfile,
        lineterm=''
    )
    return '\n'.join(diff)

def log_change(message, log_file):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as lf:
        lf.write(f"{timestamp}\n{message}\n\n")
    print(message)

def get_text_file_lines(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    except Exception:
        return []

def monitor_files_forever(folder_path, baseline_file, interval=10, log_file="file_changes.log"):
    if not os.path.exists(baseline_file):
        print("No baseline found: generating baseline...")
        create_baseline(baseline_file, folder_path)
    baseline_hashes = load_baseline(baseline_file)
    print(f"Monitoring '{folder_path}'. Press Ctrl+C to stop.")
    try:
        while True:
            current_hashes = {}
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    full_path = os.path.join(root, file)
                    if os.path.abspath(full_path) != os.path.abspath(baseline_file) and os.path.abspath(full_path) != os.path.abspath(log_file):
                        file_hash = calculate_file_hash(full_path)
                        if file_hash:
                            current_hashes[full_path] = file_hash

            added_files = set(current_hashes.keys()) - set(baseline_hashes.keys())
            deleted_files = set(baseline_hashes.keys()) - set(current_hashes.keys())
            modified_files = {f for f in current_hashes if f in baseline_hashes and current_hashes[f] != baseline_hashes[f]}

            if added_files:
                for f in added_files:
                    log_change(f"ADDED: {f}", log_file)
                    baseline_hashes[f] = current_hashes[f]
            if deleted_files:
                for f in deleted_files:
                    log_change(f"DELETED: {f}", log_file)
                    baseline_hashes.pop(f, None)
            if modified_files:
                for f in modified_files:
                    if f.lower().endswith((".txt", ".log", ".csv", ".py", ".md", ".json")):
                        backup_key = f + ".bak"
                        oldfile_lines = get_text_file_lines(backup_key) if os.path.exists(backup_key) else []
                        difftext = show_text_diff(oldfile_lines, get_text_file_lines(f), "before", "after")
                        log_change(f"MODIFIED: {f}\nChanged lines:\n{difftext if difftext else 'UNABLE TO SHOW DIFF'}", log_file)
                        try:
                            shutil.copy(f, backup_key)
                        except Exception:
                            pass
                    else:
                        log_change(f"MODIFIED: {f} (binary or non-text)", log_file)
                    baseline_hashes[f] = current_hashes[f]
            if added_files or deleted_files or modified_files:
                save_baseline(baseline_file, baseline_hashes)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

if __name__ == "__main__":
    folder_to_monitor = os.getcwd()  # Always use script folder
    baseline_file = os.path.join(folder_to_monitor, "hash_baseline.txt")
    log_file = os.path.join(folder_to_monitor, "file_changes.log")
    monitor_files_forever(folder_to_monitor, baseline_file, interval=10, log_file=log_file)
