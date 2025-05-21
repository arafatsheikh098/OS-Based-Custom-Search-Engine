# import tkinter as tk
# from tkinter import ttk
# import threading
# from FileFinder import FileFinder
# import os  # Added for better path handling
# from ApplicationManager import ApplicationManager  # Import the ApplicationManager

# class SearchApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("OS Search Engine")
#         self.create_widgets()
#         self.file_finder = FileFinder()
#         self.app_manager = ApplicationManager()  # Create an instance of ApplicationManager

#     def create_widgets(self):
#         # Search Bar
#         ttk.Label(self.root, text="Search Query:").grid(row=0, column=0, padx=5, pady=5)
#         self.query_entry = ttk.Entry(self.root, width=50)
#         self.query_entry.grid(row=0, column=1, padx=5, pady=5)

#         # Search Buttons
#         ttk.Button(self.root, text="Search Files", command=self.start_search_thread).grid(row=0, column=2, padx=5, pady=5)
#         ttk.Button(self.root, text="Search Applications", command=self.start_application_search_thread).grid(row=0, column=3, padx=5, pady=5)

#         # Results Panel
#         self.results_tree = ttk.Treeview(self.root, columns=("Name", "Path"), show="headings")
#         self.results_tree.heading("Name", text="File Name")
#         self.results_tree.heading("Path", text="File Path")
#         self.results_tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

#         # Open Button
#         ttk.Button(self.root, text="Open Selected", command=self.open_selected).grid(row=2, column=1, pady=5)

#     def start_search_thread(self):
#         # Start a new thread to perform the file search
#         threading.Thread(target=self.perform_search, daemon=True).start()

#     def perform_search(self):
#         query = self.query_entry.get().strip()
#         if not query:
#             return

#         # Call FileFinder to search for files
#         self.file_finder.find_file(query, self.display_results)

#     def start_application_search_thread(self):
#         # Start a new thread to perform the application search
#         threading.Thread(target=self.perform_application_search, daemon=True).start()

#     def perform_application_search(self):
#         query = self.query_entry.get().strip()
#         # Use the ApplicationManager to get applications
#         results = self.app_manager.get_applications()
#         filtered_results = [app for app in results if query.lower() in os.path.basename(app).lower()]
#         self.display_results(filtered_results)

#     def display_results(self, results):
#         # Clear previous results
#         self.results_tree.delete(*self.results_tree.get_children())

#         # Display new results
#         if results:
#             for path in results:
#                 name = os.path.basename(path)  # Use os.path.basename for cross-platform compatibility
#                 self.results_tree.insert("", "end", values=(name, path))
#         else:
#             self.results_tree.insert("", "end", values=("No Results Found", ""))

#     def open_selected(self):
#         selected_item = self.results_tree.selection()
#         if selected_item:
#             path = self.results_tree.item(selected_item, "values")[1]
#             # Check if it's an application or file
#             if path.endswith(".exe") or path.endswith(".lnk"):  # If it's a Windows application
#                 result = self.app_manager.open_application(path)
#             else:
#                 result = self.file_finder.open_file(path)
#             print(result)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SearchApp(root)
#     root.mainloop()



# import tkinter as tk
# from tkinter import ttk
# import threading
# from FileFinder import FileFinder
# import os
# from ApplicationManager import ApplicationManager
# import time

# class SearchApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("OS Search Engine")
#         self.create_widgets()
#         self.file_finder = FileFinder()
#         self.app_manager = ApplicationManager()
#         self.last_search_time = 0
#         self.search_delay = 0.3  # Delay in seconds between keystrokes before searching
#         self.exact_match_mode = False
#         self.current_search_thread = None

#     def create_widgets(self):
#         ttk.Label(self.root, text="Search Query:").grid(row=0, column=0, padx=5, pady=5)
#         self.query_entry = ttk.Entry(self.root, width=50)
#         self.query_entry.grid(row=0, column=1, padx=5, pady=5)
#         self.query_entry.bind("<KeyRelease>", self.on_query_change)
#         self.query_entry.bind("<Return>", self.on_enter_press)
#         self.query_entry.bind("<Escape>", lambda e: self.query_entry.delete(0, tk.END))

#         ttk.Button(self.root, text="Search Files", command=self.start_search_thread).grid(row=0, column=2, padx=5, pady=5)
#         ttk.Button(self.root, text="Search Applications", command=self.start_application_search_thread).grid(row=0, column=3, padx=5, pady=5)

#         self.results_tree = ttk.Treeview(self.root, columns=("Name", "Path"), show="headings")
#         self.results_tree.heading("Name", text="File Name")
#         self.results_tree.heading("Path", text="File Path")
#         self.results_tree.grid(row=1, column=0, columnspan=4, padx=5, pady=5)
#         self.results_tree.bind("<Double-1>", lambda e: self.open_selected())

#         ttk.Button(self.root, text="Open Selected", command=self.open_selected).grid(row=2, column=1, pady=5)
#     # already shown
#     def start_search_thread(self):
#         if self.current_search_thread and self.current_search_thread.is_alive():
#             return
            
#         self.current_search_thread = threading.Thread(target=self.perform_search, daemon=True)
#         self.current_search_thread.start()
#      #already shown
#     def perform_search(self):
#         query = self.query_entry.get().strip()
#         if not query:
#             self.display_results([])
#             return
        
#         # Use the callback version of find_file
#         self.file_finder.find_file(query, self.display_results)

#     def start_application_search_thread(self):
#         if self.current_search_thread and self.current_search_thread.is_alive():
#             return
            
#         self.current_search_thread = threading.Thread(target=self.perform_application_search, daemon=True)
#         self.current_search_thread.start()

#     def perform_application_search(self):
#         query = self.query_entry.get().strip()
#         results = self.app_manager.get_applications()
#         if self.exact_match_mode:
#             filtered_results = [app for app in results if query.lower() == os.path.basename(app).lower()]
#         else:
#             filtered_results = [app for app in results if query.lower() in os.path.basename(app).lower()]
#         self.display_results(filtered_results)

#     def display_results(self, results):
#         # This will be called by the FileFinder's callback
#         self.root.after(0, self._update_results_tree, results)

#     def _update_results_tree(self, results):
#         self.results_tree.delete(*self.results_tree.get_children())
#         if results:
#             for path in results:
#                 name = os.path.basename(path)
#                 self.results_tree.insert("", "end", values=(name, path))
#             # If in exact match mode and we found results, select the first one
#             if self.exact_match_mode and len(results) > 0:
#                 self.results_tree.selection_set(self.results_tree.get_children()[0])
#         else:
#             self.results_tree.insert("", "end", values=("No Results Found", ""))

#     def open_selected(self):
#         selected_item = self.results_tree.selection()
#         if selected_item:
#             path = self.results_tree.item(selected_item, "values")[1]
#             if path.endswith(".exe") or path.endswith(".lnk"):
#                 result = self.app_manager.open_application(path)
#             else:
#                 result = self.file_finder.open_file(path)
#             print(result)

#     def on_query_change(self, event):
#         """Handle real-time search with debounce."""
#         if event.keysym == "Return":
#             return
            
#         current_time = time.time()
#         if current_time - self.last_search_time < self.search_delay:
#             return
            
#         query = self.query_entry.get().strip()
#         self.last_search_time = current_time
        
#         if query:
#             self.exact_match_mode = False
#             self.start_search_thread()
#         else:
#             self.display_results([])

#     def on_enter_press(self, event):
#         """Perform exact match search when Enter is pressed."""
#         query = self.query_entry.get().strip()
#         if query:
#             self.exact_match_mode = True
#             self.start_search_thread()

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SearchApp(root)
#     root.mainloop()




# import tkinter as tk
# from tkinter import ttk
# import threading
# from FileFinder import FileFinder
# import os
# from ApplicationManager import ApplicationManager
# import time
# import datetime
# from humanize import naturalsize  # For human-readable file sizes

# class SearchApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("OS Search Engine")
#         self.create_widgets()
#         self.file_finder = FileFinder()
#         self.app_manager = ApplicationManager()
#         self.last_search_time = 0
#         self.search_delay = 0.3  # Delay in seconds between keystrokes before searching
#         self.exact_match_mode = False
#         self.current_search_thread = None

#     def create_widgets(self):
#         # Search frame
#         search_frame = ttk.Frame(self.root)
#         search_frame.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        
#         ttk.Label(search_frame, text="Search Query:").pack(side=tk.LEFT, padx=5)
#         self.query_entry = ttk.Entry(search_frame, width=50)
#         self.query_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
#         self.query_entry.bind("<KeyRelease>", self.on_query_change)
#         self.query_entry.bind("<Return>", self.on_enter_press)
#         self.query_entry.bind("<Escape>", lambda e: self.query_entry.delete(0, tk.END))

#         ttk.Button(search_frame, text="Search Files", command=self.start_search_thread).pack(side=tk.LEFT, padx=5)
#         ttk.Button(search_frame, text="Search Apps", command=self.start_application_search_thread).pack(side=tk.LEFT, padx=5)
        
#         # Results treeview with scrollbar
#         tree_frame = ttk.Frame(self.root)
#         tree_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
#         self.results_tree = ttk.Treeview(tree_frame, columns=("Name", "Path", "Type", "Size", "Modified"), show="headings")
        
#         # Configure columns
#         self.results_tree.heading("Name", text="Name", anchor=tk.W)
#         self.results_tree.heading("Path", text="Path", anchor=tk.W)
#         self.results_tree.heading("Type", text="Type", anchor=tk.W)
#         self.results_tree.heading("Size", text="Size", anchor=tk.W)
#         self.results_tree.heading("Modified", text="Modified", anchor=tk.W)
        
#         self.results_tree.column("Name", width=200, stretch=tk.YES)
#         self.results_tree.column("Path", width=300, stretch=tk.YES)
#         self.results_tree.column("Type", width=100, stretch=tk.NO)
#         self.results_tree.column("Size", width=100, stretch=tk.NO)
#         self.results_tree.column("Modified", width=150, stretch=tk.NO)
        
#         # Add scrollbar
#         tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.results_tree.yview)
#         tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
#         self.results_tree.configure(yscrollcommand=tree_scroll.set)
#         self.results_tree.pack(fill=tk.BOTH, expand=True)
        
#         self.results_tree.bind("<Double-1>", lambda e: self.open_selected())

#         # Bottom buttons
#         button_frame = ttk.Frame(self.root)
#         button_frame.grid(row=2, column=0, columnspan=4, pady=5)
        
#         ttk.Button(button_frame, text="Open Selected", command=self.open_selected).pack(side=tk.LEFT, padx=5)
#         ttk.Button(button_frame, text="Show in Folder", command=self.show_in_folder).pack(side=tk.LEFT, padx=5)
        
#         # Configure grid weights
#         self.root.grid_rowconfigure(1, weight=1)
#         self.root.grid_columnconfigure(0, weight=1)

#     def get_file_info(self, path):
#         """Get detailed file information for display in the treeview."""
#         try:
#             stat = os.stat(path)
#             size = naturalsize(stat.st_size) if os.path.isfile(path) else "--"
            
#             modified_time = datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
#             if os.path.isdir(path):
#                 file_type = "Folder"
#             elif path.endswith(('.exe', '.lnk')):
#                 file_type = "Application"
#             else:
#                 file_type = os.path.splitext(path)[1][1:].upper() + " File"
                
#             return size, modified_time, file_type
            
#         except Exception as e:
#             print(f"Error getting file info: {e}")
#             return "--", "--", "--"

#     def start_search_thread(self):
#         if self.current_search_thread and self.current_search_thread.is_alive():
#             return
            
#         self.current_search_thread = threading.Thread(target=self.perform_search, daemon=True)
#         self.current_search_thread.start()

#     def perform_search(self):
#         query = self.query_entry.get().strip()
#         if not query:
#             self.display_results([])
#             return
        
#         # Use the callback version of find_file
#         self.file_finder.find_file(query, self.display_results)

#     def start_application_search_thread(self):
#         if self.current_search_thread and self.current_search_thread.is_alive():
#             return
            
#         self.current_search_thread = threading.Thread(target=self.perform_application_search, daemon=True)
#         self.current_search_thread.start()

#     def perform_application_search(self):
#         query = self.query_entry.get().strip()
#         results = self.app_manager.get_applications()
#         if self.exact_match_mode:
#             filtered_results = [app for app in results if query.lower() == os.path.basename(app).lower()]
#         else:
#             filtered_results = [app for app in results if query.lower() in os.path.basename(app).lower()]
#         self.display_results(filtered_results)

#     def display_results(self, results):
#         """Display results with additional file information."""
#         processed_results = []
#         for path in results:
#             try:
#                 name = os.path.basename(path)
#                 size, modified, file_type = self.get_file_info(path)
#                 processed_results.append((path, name, file_type, size, modified))
#             except Exception as e:
#                 print(f"Error processing result {path}: {e}")
        
#         self.root.after(0, self._update_results_tree, processed_results)

#     def _update_results_tree(self, results):
#         self.results_tree.delete(*self.results_tree.get_children())
#         if results:
#             for path, name, file_type, size, modified in results:
#                 self.results_tree.insert("", "end", values=(name, path, file_type, size, modified))
#             # If in exact match mode and we found results, select the first one
#             if self.exact_match_mode and len(results) > 0:
#                 self.results_tree.selection_set(self.results_tree.get_children()[0])
#         else:
#             self.results_tree.insert("", "end", values=("No Results Found", "", "", "", ""))

#     def open_selected(self):
#         selected_item = self.results_tree.selection()
#         if selected_item:
#             path = self.results_tree.item(selected_item, "values")[1]
#             if path.endswith(".exe") or path.endswith(".lnk"):
#                 result = self.app_manager.open_application(path)
#             else:
#                 result = self.file_finder.open_file(path)
#             print(result)

#     def show_in_folder(self):
#         """Open file explorer with the selected file highlighted."""
#         selected_item = self.results_tree.selection()
#         if selected_item:
#             path = self.results_tree.item(selected_item, "values")[1]
#             try:
#                 if os.path.isfile(path):
#                     # Windows-specific implementation
#                     os.startfile(os.path.dirname(path))
#                 elif os.path.isdir(path):
#                     os.startfile(path)
#             except Exception as e:
#                 print(f"Error showing in folder: {e}")

#     def on_query_change(self, event):
#         """Handle real-time search with debounce."""
#         if event.keysym == "Return":
#             return
            
#         current_time = time.time()
#         if current_time - self.last_search_time < self.search_delay:
#             return
            
#         query = self.query_entry.get().strip()
#         self.last_search_time = current_time
        
#         if query:
#             self.exact_match_mode = False
#             self.start_search_thread()
#         else:
#             self.display_results([])

#     def on_enter_press(self, event):
#         """Perform exact match search when Enter is pressed."""
#         query = self.query_entry.get().strip()
#         if query:
#             self.exact_match_mode = True
#             self.start_search_thread()

# if __name__ == "__main__":
#     root = tk.Tk()
#     # Set a more modern theme if available
#     try:
#         root.tk.call("source", "azure.tcl")
#         root.tk.call("set_theme", "dark")
#     except:
#         pass
        
#     root.geometry("900x600")
#     app = SearchApp(root)
#     root.mainloop()

#     # we need to install additional python package humanize

import tkinter as tk
from tkinter import ttk
import threading
from FileFinder import FileFinder
import os
from ApplicationManager import ApplicationManager
import time
import datetime

class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Search Engine")
        self.create_widgets()
        self.file_finder = FileFinder()
        self.app_manager = ApplicationManager()
        self.last_search_time = 0
        self.search_delay = 0.3  # Delay in seconds between keystrokes before searching
        self.exact_match_mode = False
        self.current_search_thread = None

    def create_widgets(self):
        # Search frame
        search_frame = ttk.Frame(self.root)
        search_frame.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="ew")
        
        ttk.Label(search_frame, text="Search Query:").pack(side=tk.LEFT, padx=5)
        self.query_entry = ttk.Entry(search_frame, width=50)
        self.query_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.query_entry.bind("<KeyRelease>", self.on_query_change)
        self.query_entry.bind("<Return>", self.on_enter_press)
        self.query_entry.bind("<Escape>", lambda e: self.query_entry.delete(0, tk.END))

        ttk.Button(search_frame, text="Search Files", command=self.start_search_thread).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Search Apps", command=self.start_application_search_thread).pack(side=tk.LEFT, padx=5)
        
        # Results treeview with scrollbar
        tree_frame = ttk.Frame(self.root)
        tree_frame.grid(row=1, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        self.results_tree = ttk.Treeview(tree_frame, columns=("Name", "Path", "Type", "Size", "Modified"), show="headings")
        
        # Configure columns
        self.results_tree.heading("Name", text="Name", anchor=tk.W)
        self.results_tree.heading("Path", text="Path", anchor=tk.W)
        self.results_tree.heading("Type", text="Type", anchor=tk.W)
        self.results_tree.heading("Size", text="Size", anchor=tk.W)
        self.results_tree.heading("Modified", text="Modified", anchor=tk.W)
        
        self.results_tree.column("Name", width=200, stretch=tk.YES)
        self.results_tree.column("Path", width=300, stretch=tk.YES)
        self.results_tree.column("Type", width=100, stretch=tk.NO)
        self.results_tree.column("Size", width=100, stretch=tk.NO)
        self.results_tree.column("Modified", width=150, stretch=tk.NO)
        
        # Add scrollbar
        tree_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.results_tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_tree.configure(yscrollcommand=tree_scroll.set)
        self.results_tree.pack(fill=tk.BOTH, expand=True)
        
        self.results_tree.bind("<Double-1>", lambda e: self.open_selected())

        # Bottom buttons
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=2, column=0, columnspan=4, pady=5)
        
        ttk.Button(button_frame, text="Open Selected", command=self.open_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show in Folder", command=self.show_in_folder).pack(side=tk.LEFT, padx=5)
        
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def format_size(self, size_bytes):
        """Convert file size in bytes to human-readable format without external dependencies."""
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        i = 0
        while size_bytes >= 1024 and i < len(size_name)-1:
            size_bytes /= 1024.0
            i += 1
        return f"{size_bytes:.1f} {size_name[i]}"

    def get_file_info(self, path):
        """Get detailed file information for display in the treeview."""
        try:
            if not os.path.exists(path):
                return "--", "--", "--"
            
            if os.path.isdir(path):
                size = "--"
                file_type = "Folder"
            else:
                size_bytes = os.path.getsize(path)
                size = self.format_size(size_bytes)
                if path.endswith(('.exe', '.lnk')):
                    file_type = "Application"
                else:
                    file_type = os.path.splitext(path)[1][1:].upper() + " File"
            
            modified_time = datetime.datetime.fromtimestamp(
                os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M:%S')
                
            return size, modified_time, file_type
            
        except Exception as e:
            print(f"Error getting file info: {e}")
            return "--", "--", "--"

    def start_search_thread(self):
        if self.current_search_thread and self.current_search_thread.is_alive():
            return
            
        self.current_search_thread = threading.Thread(target=self.perform_search, daemon=True)
        self.current_search_thread.start()

    def perform_search(self):
        query = self.query_entry.get().strip()
        if not query:
            self.display_results([])
            return
        
        # Use the callback version of find_file
        self.file_finder.find_file(query, self.display_results)

    def start_application_search_thread(self):
        if self.current_search_thread and self.current_search_thread.is_alive():
            return
            
        self.current_search_thread = threading.Thread(target=self.perform_application_search, daemon=True)
        self.current_search_thread.start()

    def perform_application_search(self):
        query = self.query_entry.get().strip()
        results = self.app_manager.get_applications()
        if self.exact_match_mode:
            filtered_results = [app for app in results if query.lower() == os.path.basename(app).lower()]
        else:
            filtered_results = [app for app in results if query.lower() in os.path.basename(app).lower()]
        self.display_results(filtered_results)

    def display_results(self, results):
        """Display results with additional file information."""
        processed_results = []
        for path in results:
            try:
                name = os.path.basename(path)
                size, modified, file_type = self.get_file_info(path)
                processed_results.append((path, name, file_type, size, modified))
            except Exception as e:
                print(f"Error processing result {path}: {e}")
        
        self.root.after(0, self._update_results_tree, processed_results)

    def _update_results_tree(self, results):
        self.results_tree.delete(*self.results_tree.get_children())
        if results:
            for path, name, file_type, size, modified in results:
                self.results_tree.insert("", "end", values=(name, path, file_type, size, modified))
            # If in exact match mode and we found results, select the first one
            if self.exact_match_mode and len(results) > 0:
                self.results_tree.selection_set(self.results_tree.get_children()[0])
        else:
            self.results_tree.insert("", "end", values=("No Results Found", "", "", "", ""))

    def open_selected(self):
        selected_item = self.results_tree.selection()
        if selected_item:
            path = self.results_tree.item(selected_item, "values")[1]
            if path.endswith(".exe") or path.endswith(".lnk"):
                result = self.app_manager.open_application(path)
            else:
                result = self.file_finder.open_file(path)
            print(result)

    def show_in_folder(self):
        """Open file explorer with the selected file highlighted."""
        selected_item = self.results_tree.selection()
        if selected_item:
            path = self.results_tree.item(selected_item, "values")[1]
            try:
                if os.path.isfile(path):
                    # Windows-specific implementation
                    os.startfile(os.path.dirname(path))
                elif os.path.isdir(path):
                    os.startfile(path)
            except Exception as e:
                print(f"Error showing in folder: {e}")

    def on_query_change(self, event):
        """Handle real-time search with debounce."""
        if event.keysym == "Return":
            return
            
        current_time = time.time()
        if current_time - self.last_search_time < self.search_delay:
            return
            
        query = self.query_entry.get().strip()
        self.last_search_time = current_time
        
        if query:
            self.exact_match_mode = False
            self.start_search_thread()
        else:
            self.display_results([])

    def on_enter_press(self, event):
        """Perform exact match search when Enter is pressed."""
        query = self.query_entry.get().strip()
        if query:
            self.exact_match_mode = True
            self.start_search_thread()

if __name__ == "__main__":
    root = tk.Tk()
    # Set a more modern theme if available
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except:
        pass
        
    root.geometry("900x600")
    app = SearchApp(root)
    root.mainloop()