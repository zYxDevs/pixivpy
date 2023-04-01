#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from pixivpy3 import AppPixivAPI, ByPassSniApi

sys.dont_write_bytecode = True


# get your refresh_token, and replace _REFRESH_TOKEN
#  https://github.com/upbit/pixivpy/issues/158#issuecomment-778919084
_REFRESH_TOKEN = "0zeYA-PllRYp1tfrsq_w3vHGU1rPy237JMf5oDt73c4"


def main():
    sni = False
    if not sni:
        api = AppPixivAPI()
    else:
        api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
        api.require_appapi_hosts()
    api.auth(refresh_token=_REFRESH_TOKEN)

    # get rankings
    json_result = api.illust_ranking("day", date="2019-01-01")

    directory = "illusts"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # download top3 day rankings to 'illusts' dir
    for idx, illust in enumerate(json_result.illusts[:4]):
        image_url = illust.meta_single_page.get(
            "original_image_url", illust.image_urls.large
        )
        print(f"{illust.title}: {image_url}")

        # try four args in MR#102
        if idx == 0:
            api.download(image_url, path=directory, name=None)
        elif idx == 1:
            url_basename = os.path.basename(image_url)
            extension = os.path.splitext(url_basename)[1]
            name = "illust_id_%d_%s%s" % (illust.id, illust.title, extension)
            api.download(image_url, path=directory, name=name)
        elif idx == 2:
            api.download(image_url, path=directory, fname=f"illust_{illust.id}.jpg")
        else:
            # path will not work due to fname is a handler
            api.download(
                image_url,
                path="/foo/bar",
                fname=open(f"{directory}/illust_{illust.id}.jpg", "wb"),
            )


if __name__ == "__main__":
    main()
