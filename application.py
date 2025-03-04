import os
import subprocess
import platform


class ApplicationManager:
    def __init__(self):
        self.os_name = platform.system()

    def get_applications(self):
        apps = []
        if self.os_name == "Darwin":  # macOS
            app_dirs = ["/Applications", "/System/Applications"]
        elif self.os_name == "Windows":
            app_dirs = [r"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs"]
        else:
            app_dirs = ["/usr/share/applications"]

        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                for app in os.listdir(app_dir):
                    if app.endswith(".app") or app.endswith(".lnk") or app.endswith(".desktop"):
                        apps.append(os.path.join(app_dir, app))

        return apps

    def open_application(self, app_name):
        apps = self.get_applications()
        for app in apps:
            if app_name.lower() in os.path.basename(app).lower():
                try:
                    if self.os_name == "Darwin":
                        subprocess.run(["open", app])
                    elif self.os_name == "Windows":
                        subprocess.run(["start", "", app], shell=True)
                    else:
                        subprocess.run(["xdg-open", app])
                    return f"Opening {app}"
                except Exception as e:
                    return f"Error opening {app}: {e}"
        return "Application not found."


    def open_application(self, app_path):
        try:
            if self.os_name == "Darwin":
                subprocess.run(["open", app_path])
            elif self.os_name == "Windows":
                subprocess.run(["start", "", app_path], shell=True)
            else:
                subprocess.run(["xdg-open", app_path])
            return f"Opening {os.path.basename(app_path)}"
        except Exception as e:
            return f"Error opening application: {e}"