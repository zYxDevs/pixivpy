#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ssl
import sys
from datetime import datetime, timedelta

from pixivpy3 import AppPixivAPI

sys.dont_write_bytecode = True

# disable SSL verify
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

_REQUESTS_KWARGS = {
    "proxies": {
        "https": "http://127.0.0.1:1087",
    },
}

# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "0zeYA-PllRYp1tfrsq_w3vHGU1rPy237JMf5oDt73c4"


def main():
    api = AppPixivAPI(**_REQUESTS_KWARGS)
    api.auth(refresh_token=_REFRESH_TOKEN)

    target_id = 275527
    json_result = api.user_bookmarks_illust(target_id)
    print_illusts(json_result.illusts[:3])

    print(">> next_url: " + json_result.next_url)
    next_qs = api.parse_qs(json_result.next_url)
    if next_qs is not None:
        json_result = api.user_bookmarks_illust(**next_qs)
        print_illusts(json_result.illusts[:3])


def print_illusts(illusts):
    for illust in illusts:
        print("[ID={illust.id}] {illust.title}".format(illust=illust))
        print("    {illust.image_urls.large}".format(illust=illust))


if __name__ == "__main__":
    main()
