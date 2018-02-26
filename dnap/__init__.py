import os
import sys
import logging
import builtins


cache_path = os.path.expanduser("~/.dnap")
if not os.path.isdir(cache_path):
    os.mkdir(cache_path)
cache_releases_path = os.path.join(cache_path, "releases.json")
cache_result_path = os.path.join(cache_path, "result.json")
cache_images_path = os.path.join(cache_path, "images")

logger = logging.getLogger("DNAP")
logger.setLevel(logging.DEBUG)

class LoggingFilter(logging.Filter):
    def filter(self, record):
        name = "%s.%s" % (record.module, record.funcName)
        if len(name) > 18:
            name = name[:18] + "…"
        record.fullname = "%s:%d" % (name, record.lineno)
        return True

logger.addFilter(LoggingFilter())

formatter = logging.Formatter(
    "{asctime:15} │ {levelname:^7} │ {fullname:23} │ {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{"
)

if getattr(sys, "frozen", False):
    handler = logging.FileHandler(os.path.join(cache_path, "dnap.log"), encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
else:
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

logging.addLevelName(logging.DEBUG,    "debug")
logging.addLevelName(logging.INFO,     "info")
logging.addLevelName(logging.WARNING,  "warning")
logging.addLevelName(logging.ERROR,    "error")
logging.addLevelName(logging.CRITICAL, "fatal")
logger.addHandler(handler)

builtins.log = logger
