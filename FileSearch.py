import os
import subprocess
import threading
import platform
import tkinter as tk
from tkinter import ttk

class FileFinder:
    def __init__(self):
        self.search_directories = [
            r"C:/ProgramData/Microsoft/Windows/Start Menu/Programs",
            r"C:/Program Files",
            r"C:/Program Files (x86)",
            r"C:/Users/monju/Downloads",
            r"C:/Users/monju/Documents",
        ]
    def find_file(self, query, callback):
        results = []
        results_lock = threading.Lock()

        def search_directory(directory):
            nonlocal results
            try:
                for dirpath, dirnames, filenames in os.walk(directory, followlinks=True):
                    
                    if not any(dirpath.startswith(d) for d in self.search_directories):
                        continue
                    
                    for filename in filenames:
                        if query.lower() in filename.lower():
                            filepath = os.path.join(dirpath, filename)
                            with results_lock:
                                results.append(filepath)

            except PermissionError:
                print(f"Permission denied: {directory}")
                pass 

        threads = []
        for directory in self.search_directories:
            thread = threading.Thread(target=search_directory, args=(directory,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        callback(results)

    def open_file(self, file_path):
        """Open a file using the default system application."""
        try:
            if os.name == "nt":  # Windows
                os.startfile(file_path)
            elif os.name == "posix":  # macOS or Linux
                subprocess.run(["open", file_path] if platform.system() == "Darwin" else ["xdg-open", file_path])
            return f"Opening {file_path}"
        except Exception as e:
            print(f"Error opening file: {e}")
            return f"Error opening file: {e}"
