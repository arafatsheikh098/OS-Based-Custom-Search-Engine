import os
import subprocess
import platform


class ApplicationManager:
    def __init__(self):
        self.os_name = platform.system()
        print(self.os_name)

    def get_applications(self):
        apps = []
        if self.os_name == "Darwin":
            app_dirs = ["/Applications", "/System/Applications"]
        elif self.os_name == "Windows":
            app_dirs = ["C:/ProgramData/Microsoft/Windows/Start Menu/Programs"] + ["C:/ProgramData/Microsoft/Windows/Start Menu/Programs"]
        else:
            app_dirs = ["/usr/share/applications"]

        for app_dir in app_dirs:
            if os.path.exists(app_dir):
                for app in os.listdir(app_dir):
                    if app.endswith(".app") or app.endswith(".lnk") or app.endswith(".desktop") or app.endswith(".exe"):
                        apps.append(os.path.join(app_dir, app))

        return apps

    def open_application_by_name(self, app_name):
        """Opens an application by searching for its name."""
        apps = self.get_applications()
        for app in apps:
            if app_name.lower() in os.path.basename(app).lower():
                return self.open_application(app)
        return "Application not found."

    def open_application(self, app_path):
        """Opens an application given its full path."""
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


if __name__ == "__main__":
    manager = ApplicationManager()

    while True:
        app_name = input("Enter the name of the application to open (or type 'exit' to quit): ").strip()
        if app_name.lower() == "exit":
            print("Exiting program.")
            break

        result = manager.open_application_by_name(app_name)
        print(result)
