#!/usr/bin/env python3

import os
import sys
import json
import shutil
import random
import pathlib
from tempfile import mkdtemp
from threading import Thread
from twisted.internet import reactor
from twisted.internet import task
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

from ..util import get_picture
from ..notifications import notify
from .. import cache_path, cache_releases_path, cache_result_path

from . import spiders
from .spiders import iam8bit
from .spiders import minorityrecords
from .spiders import theyetee
from .spiders import shiptoshore
from .spiders import datadiscs
from .spiders import lacedrecords
from .spiders import thinkgeek
from .spiders import turntablelab
from .spiders import fangamer
from .spiders import blackscreen
from .spiders import mondo

all_labels = list(filter(lambda n: not n.startswith("__"), dir(spiders)))


def scrape(interval, verbose=False):
    print("Initiating scrape")

    # Scrapy uses twisted's reactor, which can only be started once per process
    thread = Thread(target=run_scrapes, args=(interval,), kwargs={"verbose": verbose})
    thread.setDaemon(True)
    thread.start()


def process_results(temp_path, verbose):
    releases = []
    for file in os.listdir(temp_path):
        with open(os.path.join(temp_path, file), "r") as f:
            raw_json = f.read() or "[]"
            releases.extend(json.loads(raw_json))
    shutil.rmtree(temp_path)

    print("Found %d releases." % len(releases))

    for label in all_labels:
        if not any(release["source"] == label for release in releases):
            print("WARNING: Label '%s' has no releases, the spider is probably out of date." % label)

    if not os.path.isdir(cache_path):
        os.mkdir(cache_path)

    if not os.path.isfile(cache_releases_path):
        with open(cache_releases_path, "w") as f:
            f.write("[]")

    with open(cache_releases_path, "r") as f:
        persisted = json.loads(f.read() or "[]")

    existing_titles = [(release["source"], release["title"]) for release in persisted]
    new_releases = []

    for release in releases:
        if (release["source"], release["title"]) not in existing_titles:
            new_releases.append(release)

    with open(cache_result_path, "w") as f:
        f.write(json.dumps({
            "new_releases": len(new_releases)
        }))

    if new_releases:
        n = len(new_releases)
        if verbose:
            print("Found %d new release%s:" % (n, "s" if n > 1 else ""))
            for i, release in enumerate(new_releases):
                print("%3d. %s – %s (%s)" % (i, release["source"], release["title"], release["price"]))
                print("     %s" % release["link"])

        persisted.extend(new_releases)
        persisted = sorted(persisted, key=lambda release: -release["first_seen"])

        with open(cache_releases_path, "w") as f:
            f.write(json.dumps(persisted))

        latest = random.choice(new_releases)
        title = "%d new release%s" % (n, "s" if n > 1 else "")
        subtitle = latest["title"]
        message= "%s%s" % (latest["price"] + " on " if latest["price"] else "From ", latest["source"])
        picture = get_picture(latest)
        notify(title, subtitle, message, picture)

    else:
        notify("No new releases", "Program is still working though", "😊")
        if verbose:
            print("No new release found!")


def run_scrapes(interval, verbose=False, limit=-1):
    temp_path = mkdtemp()
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s", "LOG_LEVEL": "WARN"})

    settings = {
        "LOG_LEVEL": "WARN",
        "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "FEED_FORMAT": "json",
        "FEED_URI": os.path.join(pathlib.Path(temp_path).as_uri(), "%(name)s")
    }

    # Using a runner instead of a process here
    # Because of http://twistedmatrix.com/trac/wiki/FrequentlyAskedQuestions#Igetexceptions.ValueError:signalonlyworksinmainthreadwhenItrytorunmyTwistedprogramWhatswrong
    # (And we can't give that argument with Process which doesn't give us control over the reactor)

    def run_crawl():
        runner = CrawlerRunner(settings)
        runner.crawl(iam8bit)
        runner.crawl(minorityrecords)
        runner.crawl(theyetee)
        runner.crawl(shiptoshore)
        runner.crawl(datadiscs)
        runner.crawl(lacedrecords)
        runner.crawl(thinkgeek)
        runner.crawl(turntablelab)
        runner.crawl(fangamer)
        runner.crawl(blackscreen)
        runner.crawl(mondo)
        print("Scraping...")
        notify("Scraping...", "", "(it may crash?)")

        nonlocal limit
        limit -= 1

        d = runner.join()
        if limit == 0:
            def process_and_stop(unused):
                process_results(temp_path, verbose)
                reactor.stop()
            d.addBoth(process_and_stop)
        else:
            d.addBoth(lambda _: process_results(temp_path, verbose))

    loop = task.LoopingCall(run_crawl)
    loop.start(interval)
    reactor.run(installSignalHandlers=0)


if __name__ == "__main__":
    run_scrapes(100, verbose=True, limit=1)
