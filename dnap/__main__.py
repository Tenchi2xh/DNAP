from apscheduler.schedulers.background import BackgroundScheduler

from .ui import app

def main():
    scheduler = BackgroundScheduler()
    scheduler.start()

    app.start(scheduler)


if __name__ == "__main__":
    main()
