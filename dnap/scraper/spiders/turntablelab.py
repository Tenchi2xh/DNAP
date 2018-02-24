import scrapy
import time


class turntablelab(scrapy.Spider):
    name = __name__
    start_urls = ["https://www.turntablelab.com/collections/vinyl-cds-date"]
    page_limit = 2  # pages are sorted by newest

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css(".product-block"):
            yield {
                "title": div.css(".collection-title::text").extract_first().strip(),
                "price": " ".join(filter(None, (s.strip() for s in div.css(".price *::text").extract()))),
                "source": "turntablelab",
                "link": response.urljoin(div.css("a::attr(href)").extract_first()),
                "picture": response.urljoin(div.css("img::attr(src)").extract_first()),
                "first_seen": scrape_time,
                "release_date": ""
            }
        next_page = response.css("a.next::attr(href)").extract_first()
        if next_page and self.page_limit > 0:
            self.page_limit -= 1
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
