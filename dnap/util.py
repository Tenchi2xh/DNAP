import os
import re
import sys
import json
import hashlib
import requests
from apscheduler.triggers.cron import CronTrigger

from . import cache_releases_path, cache_result_path, cache_images_path
from .scraper.scrape import scrape
from .notifications import notify


def add_cron(scheduler, callback, cron, **kwargs):
    scheduler.add_job(callback, trigger=CronTrigger(**cron), **kwargs)


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def latest_scraped():
    with open(cache_releases_path, "r") as f:
        releases = json.load(f)
    return max(releases, key=lambda r: r["first_seen"])


def last_scrape_result():
    with open(cache_result_path, "r") as f:
        new_releases = json.load(f)["new_releases"]
    return new_releases


def release_hash(release_dict):
    data = json.dumps(release_dict, sort_keys=True)
    return hashlib.sha1(data.encode("utf-8")).hexdigest()


def get_extension(url):
    extension_pattern = r".*(\.[a-zA-Z]+)(\?.*)?"
    match = re.match(extension_pattern, url)
    if match:
        return match.group(1)
    else:
        return ""


def get_picture(release):
    source_path = os.path.join(cache_images_path, release["source"])
    if not os.path.isdir(source_path):
        os.makedirs(source_path)

    image_path = os.path.join(source_path, "%s%s" % (release_hash(release), get_extension(release["picture"])))
    if not os.path.isfile(image_path):
        r = requests.get(release["picture"])
        with open(image_path, "wb") as f:
            f.write(r.content)

    return image_path


def scrape_and_notify():
    scrape()
    result = last_scrape_result()
    release = latest_scraped()
    if result:
        title = "%d new release%s" % (result, "s" if result > 1 else "")
        subtitle = release["title"]
        message= "%s%s" % (release["price"] + " on " if release["price"] else "From ", release["source"])
        picture = get_picture(release)
        notify(title, subtitle, message, picture)
