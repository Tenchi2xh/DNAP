import scrapy
import time


class minorityrecords(scrapy.Spider):
    name = __name__
    start_urls = ["https://www.minorityrecords.com/en/releases"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css(".views-row"):
            yield {
                "title": div.css(".views-field-title a::text").extract_first(),
                "price": "",
                "source": "minorityrecords",
                "link": response.urljoin(div.css(".views-field-title a::attr(href)").extract_first()),
                "picture": response.urljoin(div.css(".views-field-field-cover img::attr(src)").extract_first()),
                "first_seen": scrape_time,
                "release_date": ""
            }
