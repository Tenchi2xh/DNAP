import scrapy
import time


class thinkgeek(scrapy.Spider):
    name = __name__
    start_urls = ["https://www.thinkgeek.com/collectibles/vinyl-records/"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css(".product"):
            yield {
                "title": div.css("::attr(data-name)").extract_first(),
                "price": div.css("::attr(data-price)").extract_first(),
                "source": "thinkgeek",
                "link": response.urljoin(div.css("a::attr(href)").extract_first()),
                "picture": response.urljoin(div.css("img::attr(data-original)").extract_first()),
                "first_seen": scrape_time,
                "release_date": ""
            }
        next_page = response.css(".pagenav-item.pagenav-next a::attr(href)").extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
