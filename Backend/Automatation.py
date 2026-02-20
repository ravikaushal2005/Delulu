class Automation:
    def __init__(self):
        pass

    def open_website(self, url):
        import webbrowser
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        return f"Website {url} opened."

    def create_file(self, path, content=""):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{path}' created."

    def read_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def append_file(self, path, content):
        with open(path, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        return f"Appended content to '{path}'."

    def shutdown_system(self, confirm=False):
        import os, platform
        if not confirm:
            return "Shutdown needs confirmation."
        if platform.system() == "Windows":
            os.system("shutdown /s /t 0")
        else:
            os.system("shutdown now")
        return "Shutdown command executed."

    def restart_system(self, confirm=False):
        import os, platform
        if not confirm:
            return "Restart needs confirmation."
        if platform.system() == "Windows":
            os.system("shutdown /r /t 0")
        else:
            os.system("reboot")
        return "Restart command executed."

    def set_timer(self, seconds, callback=None, message="Time's up!"):
        import threading, time
        def timer_thread():
            time.sleep(seconds)
            if callback:
                callback(message)
            else:
                print(message)
        threading.Thread(target=timer_thread, daemon=True).start()
        return f"Timer set for {seconds} seconds."
