# HashTrack 🛡️

**HashTrack** is a lightweight, Python-based **File Integrity Monitor (FIM)**. It monitors a specific directory for changes in real-time, logging file creations, deletions, and modifications using SHA-256 hashing.

For text-based files, HashTrack goes beyond simple alerts by generating a **Unified Diff**, showing you exactly which lines were added or removed.

## 🚀 Features

* **Integrity Verification:** Uses **SHA-256** hashing to detect even single-byte changes.
* **Smart Baselining:** Automatically creates a "snapshot" of the folder state upon first run.
* **Visual Diffs:** Shows exactly *what* changed in text files (Python, logs, txt, json, etc.).
* **Automatic Backups:** Creates `.bak` copies of files before they are modified, preserving the previous version.
* **Zero Dependencies:** Built entirely with Python's standard library. No `pip install` required.
* **Portable:** Can be compiled into a single `.exe` file for easy deployment.

## 🛠️ Installation & Usage

### Option 1: Running from Source
Ensure you have Python installed.

1.  Clone the repository:
    ```bash
    git clone [https://github.com/YOUR_USERNAME/HashTrack.git](https://github.com/YOUR_USERNAME/HashTrack.git)
    cd HashTrack
    ```
2.  Run the script:
    ```bash
    python file_monitor.py
    ```

### Option 2: Running the Executable
If you have the compiled `.exe` file:
1.  Place `file_monitor.exe` inside the folder you want to monitor.
2.  Double-click to run.
3.  Keep the window open to maintain monitoring.

## 📋 How It Works

1.  **Baseline Creation:** On startup, the script scans the directory and calculates a unique hash for every file. This is saved in `hash_baseline.txt`.
2.  **Continuous Polling:** Every 10 seconds, it rescans the directory and compares the current state to the baseline.
3.  **Logging:**
    * **Added:** New files are detected and hashed.
    * **Deleted:** Missing files are flagged.
    * **Modified:** If a hash mismatch occurs, the script compares the file content to the previous version and generates a diff report.
4.  **Output:** All events are saved to `file_changes.log`.

## 📂 Project Structure

* `file_monitor.py`: The main source code.
* `hash_baseline.txt`: (Generated) Stores the SHA-256 signatures of your files. **Do not edit manually.**
* `file_changes.log`: (Generated) A readable log history of all detected changes.

## 📦 Building the Executable

To convert this script into a standalone `.exe`:

1.  Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```
2.  Build the project:
    ```bash
    pyinstaller --onefile file_monitor.py
    ```
3.  Find your executable in the `dist/` folder.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open-source and available for educational purposes.