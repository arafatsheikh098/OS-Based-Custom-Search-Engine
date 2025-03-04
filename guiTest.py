import tkinter as tk
from tkinter import ttk, messagebox
from search_engine import SearchEngine

class SearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Search Engine")
        self.root.geometry("750x450")  # Adjusted for better spacing
        self.root.resizable(True, True)  # Allow window resizing

        self.create_widgets()

    def create_widgets(self):
        # Styling
        style = ttk.Style()
        style.configure("TButton", padding=5, font=("Arial", 10))
        style.configure("TLabel", font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # Search Bar Frame
        search_frame = ttk.Frame(self.root, padding=10)
        search_frame.pack(fill="x")

        # Search Bar Container (Frame with Border)
        search_container = tk.Frame(search_frame, bg="white", highlightbackground="gray", highlightthickness=1)
        search_container.pack(side="left", padx=5, fill="x", expand=True)

        # Search Icon (🔍)
        search_icon = tk.Label(search_container, text="🔍", font=("Arial", 12), bg="white")
        search_icon.pack(side="left", padx=5, pady=3)

        # Modern Search Entry
        self.query_entry = ttk.Entry(search_container, font=("Arial", 11))
        self.query_entry.pack(side="left", padx=5, expand=True, fill="x", ipady=3)

        # Bind Enter Key to Trigger Search
        self.query_entry.bind("<Return>", self.perform_search)  # Added this line ✅

        # Search Button
        self.search_button = ttk.Button(search_frame, text="Search", command=self.perform_search)
        self.search_button.pack(side="left", padx=5)

        # Hover Effect on Button
        self.search_button.bind("<Enter>", lambda e: self.search_button.config(style="Hover.TButton"))
        self.search_button.bind("<Leave>", lambda e: self.search_button.config(style="TButton"))

        style.configure("Hover.TButton", background="#0078D7", foreground="white", padding=5, font=("Arial", 10, "bold"))

        # Results Frame
        results_frame = ttk.Frame(self.root, padding=10)
        results_frame.pack(fill="both", expand=True)

        # Scrollable Treeview for Results
        columns = ("Name", "Path", "Size", "Modified")
        self.results_tree = ttk.Treeview(results_frame, columns=columns, show="headings")

        # Define column headings
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, anchor="w")

        # Adjust column widths
        self.results_tree.column("Name", width=180)
        self.results_tree.column("Path", width=280)
        self.results_tree.column("Size", width=100, anchor="center")
        self.results_tree.column("Modified", width=120, anchor="center")

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_tree.yview)
        tree_scroll_x = ttk.Scrollbar(results_frame, orient="horizontal", command=self.results_tree.xview)
        self.results_tree.configure(yscroll=tree_scroll_y.set, xscroll=tree_scroll_x.set)

        tree_scroll_y.pack(side="right", fill="y")
        tree_scroll_x.pack(side="bottom", fill="x")
        self.results_tree.pack(fill="both", expand=True)

        # Status Bar
        self.status_label = ttk.Label(self.root, text="Enter a query and click 'Search'", anchor="w", padding=5)
        self.status_label.pack(fill="x")

    def perform_search(self, event=None):  # Added 'event=None' to handle Enter key
        query = self.query_entry.get().strip()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search query!")
            return

        self.status_label.config(text="Searching... Please wait.")
        self.root.update_idletasks()

        search_engine = SearchEngine(root_directory="/")
        results = search_engine.search(query=query)

        # Clear previous results
        for row in self.results_tree.get_children():
            self.results_tree.delete(row)

        # Display new results
        if results:
            for result in results:
                self.results_tree.insert("", "end", values=(result.name, result.path, result.size, result.modified_date))
            self.status_label.config(text=f"Search completed: {len(results)} results found.")
        else:
            self.status_label.config(text="No results found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SearchApp(root)
    root.mainloop()
