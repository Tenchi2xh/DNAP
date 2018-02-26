import os
import re
import sys
import json
import hashlib
import requests

from . import cache_releases_path, cache_result_path, cache_images_path


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_releases():
    # FIXME: Verify that file exists
    log.debug("Fetching releases")
    with open(cache_releases_path, "r") as f:
        releases = json.load(f)
    return releases


def latest_scraped():
    # FIXME: Account for empty list
    releases = get_releases()
    return max(releases, key=lambda r: r["first_seen"])


def last_scrape_result():
    # FIXME: Verify that file exists
    log.debug("Fetching last scrape result")
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
        log.debug("Picture '%s' not cached, fetching" % (release["picture"]))
        # FIXME: have a default image for errors
        r = requests.get(release["picture"])
        with open(image_path, "wb") as f:
            f.write(r.content)

    return image_path
