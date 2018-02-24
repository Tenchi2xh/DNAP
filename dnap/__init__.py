import os
import re
import json
import hashlib
import requests

cache_path = os.path.expanduser("~/.dnap")
cache_releases_path = os.path.join(cache_path, "releases.json")
cache_result_path = os.path.join(cache_path, "result.json")
cache_images_path = os.path.join(cache_path, "images")

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
