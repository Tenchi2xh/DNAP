import sys
from functools import wraps


def notify(title, subtitle, message, icon=None):
    print(title, subtitle, message, icon)


if sys.platform == "darwin":
    from .macos import notify
    notify = notify
elif sys.platform == "win32":
    from .windows import notify
    notify = notify
elif sys.platform.startswith("linux"):
    import notify2
    from .linux import notify
    notify2.init("DNAP")
    notify = notify


def logged(func):
    @wraps(func)
    def with_logging(title, subtitle, message, icon=None):
        log.info("Sending notification with title '%s'" % title)
        func(title, subtitle, message, icon)
    return with_logging


notify = logged(notify)
