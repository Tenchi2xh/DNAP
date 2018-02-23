from apscheduler.schedulers.background import BackgroundScheduler

from .ui import app

if __name__ == "__main__":
        scheduler = BackgroundScheduler()
        scheduler.start()

        app.start(scheduler)
