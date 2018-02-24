from apscheduler.schedulers.background import BackgroundScheduler

from .ui import app
from .util import add_cron, scrape_and_notify


def main():
    scheduler = BackgroundScheduler()
    scheduler.start()

    add_cron(scheduler, scrape_and_notify, {"minute": "*/15"})

    app.start(scheduler)


if __name__ == "__main__":
    main()
