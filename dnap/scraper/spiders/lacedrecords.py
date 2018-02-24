import scrapy
import time


class lacedrecords(scrapy.Spider):
    name = __name__
    start_urls = ["https://www.lacedrecords.co/collections/vinyl"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css(".product-list-item"):
            yield {
                "title": div.css(".product-list-item-title a::text").extract_first(),
                "price": " ".join(filter(None, (s.strip() for s in div.css(".product-list-item-price *::text").extract()))),
                "source": "lacedrecords",
                "link": response.urljoin(div.css("a::attr(href)").extract_first()),
                "picture": response.urljoin(div.css("img::attr(src)").extract_first()),
                "first_seen": scrape_time,
                "release_date": ""
            }
