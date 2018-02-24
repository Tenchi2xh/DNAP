#!/usr/bin/env python3

import os
import json
import shutil
from tempfile import mkdtemp
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

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


def scrape(verbose=False):
    temp_path = mkdtemp()

    settings = {
        "LOG_LEVEL": "WARN",
        "USER_AGENT": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "FEED_FORMAT": "json",
        "FEED_URI": os.path.join(temp_path, "%(name)s")
    }

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
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    print("Scraping...")
    # Using a runner instead of a process here
    # Because of http://twistedmatrix.com/trac/wiki/FrequentlyAskedQuestions#Igetexceptions.ValueError:signalonlyworksinmainthreadwhenItrytorunmyTwistedprogramWhatswrong
    # (And we can't give that argument with Process which doesn't give us control over the reactor)
    reactor.run(installSignalHandlers=0)

    releases = []
    for file in os.listdir(temp_path):
        with open(os.path.join(temp_path, file), "r") as f:
            raw_json = f.read() or "[]"
            releases.extend(json.loads(raw_json))
    shutil.rmtree(temp_path)

    print("Found %d releases." % len(releases))
#    print(json.dumps(releases, indent=4))
#    return

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

        return new_releases

    else:
        if verbose:
            print("No new release found!")
        return []


if __name__ == "__main__":
    scrape(verbose=True)
