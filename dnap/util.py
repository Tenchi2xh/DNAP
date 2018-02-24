import os
import sys
from apscheduler.triggers.cron import CronTrigger

def add_cron(scheduler, callback, cron, **kwargs):
    scheduler.add_job(callback, trigger=CronTrigger(**cron), **kwargs)


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
