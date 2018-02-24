import scrapy
import time


class datadiscs(scrapy.Spider):
    name = __name__
    start_urls = ["https://data-discs.com/collections/all"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css(".product"):
            yield {
                "title": div.css(".title::text").extract_first(),
                "price": " ".join(div.css(".price::text").extract_first().strip().split()),
                "source": "datadiscs",
                "link": response.urljoin(div.css("a::attr(href)").extract_first()),
                "picture": response.urljoin(div.css("img::attr(src)").extract_first()),
                "first_seen": scrape_time,
                "release_date": ""
            }
