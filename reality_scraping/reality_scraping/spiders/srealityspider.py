import unicodedata

import scrapy
import json
import time


class SRealityFlatsForSaleSpider(scrapy.Spider):
    name = "sreality-flats_sale"
    #forbidden by robots.txt
    tms = int(round(time.time(), 3) * 1000)
    start_urls = [f"https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1"
                  f"&per_page=500&tms={tms}"]

    def parse(self, response):
        resp = json.loads(response.body)
        estates = resp['_embedded']['estates']
        for estate in estates:
            try:
                title = estate["name"]
                #title = title.replace(u'\xa0', u' ')
                title = unicodedata.normalize("NFKD", title)
            except:
                title = "error loading title for this flat"
            try:
                img_url = estate["_links"]["image_middle2"][0]['href']
            except:
                img_url = ""

            yield {
                "title": title,
                "img_url": img_url
            }
        """
        property_list = response.css("div.dir-property-list")
        for element in property_list:
            yield {
                "title": element.css("span.name.ng-binding::text").get(),
                #"img_url": offer.css("img").attrib['src'],
                #"url": offer.css("a.text-underline").attrib['href']
            }
        """