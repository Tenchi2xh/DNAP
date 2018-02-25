import sys

def notify(title, subtitle, message, icon=None):
    print(title, subtitle, message, icon)

if sys.platform == "darwin":
    from .macos import notify
    notify = notify
elif sys.platform == "win32":
    from .windows import notify
    notify = notify
