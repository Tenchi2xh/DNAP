import scrapy
import time


class mondo(scrapy.Spider):
    name = __name__
    start_urls = ["https://mondotees.com/collections/music"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css("div.product-grid-item"):
            yield {
                "title": div.css(".product-grid-title::text").extract_first(),
                "price": div.css(".product-grid-price::text").extract_first().strip(),
                "source": "mondo",
                "link": response.urljoin(div.css("a::attr(href)").extract_first()),
                "picture": response.urljoin(div.css("img.product-grid-thumb::attr(src)").extract_first()),
                "first_seen": scrape_time,
                "release_date": ""
            }
        next_page = response.css(".icon-arrow-right::attr(href)").extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
