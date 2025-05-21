# import os
# import subprocess
# import platform

# class FileFinder:
#     def __init__(self):
#         self.os_name = platform.system()

#     def find_file(self, query, callback):
#         results = []

#         def is_exact_match(path):
#             if "." in query:
#                 return os.path.basename(path).lower() == query.lower()
#             return query.lower() in os.path.basename(path).lower()

#         # Perform search across specified directories in the get_applications function
#         app_dirs = self.get_applications_directories()

#         for directory in app_dirs:
#             try:
#                 for dirpath, dirnames, filenames in os.walk(directory, followlinks=True):
#                     for filename in filenames:
#                         if is_exact_match(filename):
#                             filepath = os.path.join(dirpath, filename)
#                             results.append(filepath)
#             except PermissionError:
#                 pass  # Skip directories that cannot be accessed

#         # Call the callback function to update the UI with the search results
#         callback(results)

#     def open_file(self, file_path):
#         """Open a file using the default system application."""
#         try:
#             if os.name == "nt":  # Windows
#                 os.startfile(file_path)
#             elif os.name == "posix":  # macOS or Linux
#                 subprocess.run(["open", file_path] if platform.system() == "Darwin" else ["xdg-open", file_path])
#             return f"Opening {file_path}"
#         except Exception as e:
#             return f"Error opening file: {e}"

#     def get_applications_directories(self):
#         app_dirs = []

#         if self.os_name == "Darwin":  # macOS
#             app_dirs = ["/Applications", "/System/Applications"]
#         elif self.os_name == "Windows":
#             app_dirs = [
#                 r"C:/ProgramData/Microsoft/Windows/Start Menu/Programs",
#                 r"C:/Users/USER/Downloads",  # Modify USER to actual user
#                 r"C:/Users/Public/Desktop",  # Corrected Public Desktop path
#                 r"D:/",  # Added D: drive
#                 r"E:/",  # Added E: drive
#             ]
#         elif self.os_name == "Linux":  # Linux
#             app_dirs = [
#                 "/usr/share/applications",
#                 "/usr/local/share/applications",
#                 os.path.expanduser("~/.local/share/applications"),
#             ]

#         return app_dirs

#     def get_applications(self):
#         apps = []
#         app_dirs = self.get_applications_directories()

#         for app_dir in app_dirs:
#             if os.path.exists(app_dir):
#                 for dirpath, dirnames, filenames in os.walk(app_dir):
#                     for filename in filenames:
#                         # Check for application extensions
#                         if self.os_name == "Windows" and filename.lower().endswith(".exe"):
#                             apps.append(os.path.join(dirpath, filename))
#                         elif self.os_name == "Darwin" and filename.lower().endswith(".app"):
#                             apps.append(os.path.join(dirpath, filename))
#                         elif self.os_name == "Linux" and filename.lower().endswith(".desktop"):
#                             apps.append(os.path.join(dirpath, filename))

#         return apps

import subprocess
import os
import platform
import threading

class FileFinder:
    def __init__(self):
        self.os_name = platform.system()
        self.index = {}  # filename.lower(): full_path
        self.lock = threading.Lock()
        self.indexing_complete = False
        threading.Thread(target=self.build_index, daemon=True).start()

    def build_index(self):
        def index_directory(directory):
            try:
                for dirpath, _, filenames in os.walk(directory, followlinks=True):
                    for filename in filenames:
                        full_path = os.path.join(dirpath, filename)
                        with self.lock:
                            self.index[filename.lower()] = full_path
            except PermissionError:
                pass

        directories = self.get_applications_directories()
        threads = []
        for directory in directories:
            if os.path.exists(directory):
                thread = threading.Thread(target=index_directory, args=(directory,))
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

        self.indexing_complete = True

    def find_file(self, query, callback):
        results = []

        def search_index():
            if not query:
                callback([])
                return

            query_lower = query.lower()
            with self.lock:
                for filename, path in self.index.items():
                    if query_lower in filename:
                        results.append(path)

            callback(results)

        threading.Thread(target=search_index, daemon=True).start()

    def open_file(self, file_path):
        """Open a file using the default system application."""
        try:
            if os.name == "nt":  # Windows
                os.startfile(file_path)
            elif os.name == "posix":  # macOS or Linux
                subprocess.run(["open", file_path] if platform.system() == "Darwin" else ["xdg-open", file_path])
            return f"Opening {file_path}"
        except Exception as e:
            return f"Error opening file: {e}"

    def get_applications_directories(self):
        app_dirs = []

        if self.os_name == "Darwin":  # macOS
            app_dirs = ["/Applications", "/System/Applications"]
        elif self.os_name == "Windows":
            app_dirs = [
                
                r"C:/Users/USER/Downloads",  # Modify USER to actual user
                r"C:/Users/Public/Desktop",
                r"D:/",  # Added D: drive
                r"E:/",  # Added E: drive
            ]
        elif self.os_name == "Linux":
            app_dirs = [
                "/usr/share/applications",
                "/usr/local/share/applications",
                os.path.expanduser("~/.local/share/applications"),
            ]

        return app_dirs

    def get_applications(self):
        apps = []
        app_dirs = self.get_applications_directories()

        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                for dirpath, dirnames, filenames in os.walk(app_dir):
                    for filename in filenames:
                        if self.os_name == "Windows" and filename.lower().endswith(".exe"):
                            apps.append(os.path.join(dirpath, filename))
                        elif self.os_name == "Darwin" and filename.lower().endswith(".app"):
                            apps.append(os.path.join(dirpath, filename))
                        elif self.os_name == "Linux" and filename.lower().endswith(".desktop"):
                            apps.append(os.path.join(dirpath, filename))

        return apps
