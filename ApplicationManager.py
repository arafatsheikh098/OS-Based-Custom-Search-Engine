import os
import subprocess
import platform
import win32com.client  # Required for shortcut resolution on Windows

class ApplicationManager:
    def __init__(self):
        self.os_name = platform.system()
        self.username = os.environ.get("USERNAME", "Default")

    def get_applications(self):
        apps = []
        if self.os_name == "Darwin":  # macOS
            app_dirs = ["/Applications", "/System/Applications"]
        elif self.os_name == "Windows":
            app_dirs = [
    r"C:/ProgramData/Microsoft/Windows/Start Menu/Programs",
    r"C:/Program Files",
    r"C:/Program Files (x86)",
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
    r"C:/Users/Public/Desktop",
    os.path.expanduser("~/AppData/Local"),
    os.path.expanduser("~/AppData/Roaming/Microsoft/Windows/Start Menu/Programs"),
    r"C:/Cisco",  # Common custom installation folder
]
        else:
            app_dirs = ["/usr/share/applications"]

        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                try:
                    for app in os.listdir(app_dir):
                        app_path = os.path.join(app_dir, app)
                        if self.os_name == "Windows" and (app.endswith(".exe") or app.endswith(".lnk")):
                            apps.append(app_path)
                        elif self.os_name == "Darwin" and app.endswith(".app"):
                            apps.append(app_path)
                        elif self.os_name != "Windows" and app.endswith(".desktop"):
                            apps.append(app_path)
                except Exception:
                    continue  # Inaccessible directories
        return apps

    def open_application_by_name(self, app_name):
        """Search for and open an application by name."""
        apps = self.get_applications()
        # Try exact match first
        for app in apps:
            if os.path.basename(app).lower() == app_name.lower():
                return self.open_application(app)
        # Fallback to partial match
        for app in apps:
            if app_name.lower() in os.path.basename(app).lower():
                return self.open_application(app)
        return "Application not found."

    def open_application(self, app_path):
        """Opens an application, handling .lnk files separately."""
        try:
            if self.os_name == "Darwin":
                subprocess.run(["open", app_path])
            elif self.os_name == "Windows":
                if app_path.endswith(".lnk"):
                    target = self.resolve_shortcut(app_path)
                    if target:
                        subprocess.run([target], shell=True)
                        return f"Opening {os.path.basename(target)}"
                    else:
                        return "Failed to resolve shortcut."
                else:
                    subprocess.run([app_path], shell=True)
            else:
                subprocess.run(["xdg-open", app_path])
            return f"Opening {os.path.basename(app_path)}"
        except Exception as e:
            return f"Error opening application: {e}"

    def resolve_shortcut(self, shortcut_path):
        """Resolve .lnk file to get the real target."""
        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortcut(shortcut_path)
            target = shortcut.TargetPath
            return target if os.path.exists(target) else None
        except Exception:
            return None

if __name__ == "__main__":
    app_manager = ApplicationManager()
    result = app_manager.open_application_by_name("Google Chrome")  # Try "IntelliJ" or "idea64"
    print(result)
