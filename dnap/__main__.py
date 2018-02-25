from .ui import app
from .scraper.scrape import scrape


def main():
    scrape(interval=15 * 60, verbose=True)
    app.start()


if __name__ == "__main__":
    main()
