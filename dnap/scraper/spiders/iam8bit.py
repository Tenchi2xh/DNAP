import scrapy
import time


class iam8bit(scrapy.Spider):
    name = __name__
    start_urls = ["https://store.iam8bit.co.uk/collections/vinyl"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css("div.product"):
            yield {
                "title": div.css(".title::text").extract_first(),
                "price": " ".join(filter(None, (s.strip() for s in div.css(".price *::text").extract()))),
                "source": "iam8bit",
                "link": response.urljoin(div.css("a::attr(href)").extract_first()),
                "picture": response.urljoin(div.css("img::attr(src)").extract_first()),
                "first_seen": scrape_time,
                "release_date": ""
            }
        next_page = response.css(".next::attr(href)").extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
