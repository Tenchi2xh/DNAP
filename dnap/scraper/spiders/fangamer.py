import scrapy
import time


class fangamer(scrapy.Spider):
    name = __name__
    start_urls = ["https://www.fangamer.com/collections/music"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css(".item-view"):
            yield {
                "title": div.css(".title::text").extract_first(),
                "price": " ".join(filter(None, (s.strip() for s in div.css(".price::text").extract()))),
                "source": "fangamer",
                "link": response.urljoin(div.css("a::attr(href)").extract_first()),
                "picture": response.urljoin(div.css("img::attr(src)").extract_first()),
                "first_seen": scrape_time,
                "release_date": ""
            }
