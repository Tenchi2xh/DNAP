import scrapy
import time


class shiptoshore(scrapy.Spider):
    name = __name__
    start_urls = ["https://www.shiptoshoremedia.com/store"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css(".product-container"):
            yield {
                "title": div.css("h4::text").extract_first(),
                "price": div.css(".ui.dividing.header::text").extract_first(),
                "source": "shiptoshore",
                "link": response.urljoin(div.css("::attr(href)").extract_first()),
                "picture": response.urljoin(div.css("img::attr(src)").extract_first()),
                "first_seen": scrape_time,
                "release_date": ""
            }
