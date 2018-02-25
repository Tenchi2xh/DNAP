from apscheduler.schedulers.background import BackgroundScheduler

from .ui import app
from .util import add_cron
from .scraper.scrape import scrape


def main():
    scheduler = BackgroundScheduler()
    scheduler.start()

    #add_cron(scheduler, scrape_and_notify, {"minute": "*/15"})
    scrape(interval=15 * 60, verbose=True)

    app.start(scheduler)


if __name__ == "__main__":
    main()
