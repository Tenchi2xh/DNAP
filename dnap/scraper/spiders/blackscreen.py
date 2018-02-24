import scrapy
import time


class blackscreen(scrapy.Spider):
    name = __name__
    start_urls = ["http://blackscreenrecords.limitedrun.com/"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css("li.product"):
            yield {
                "title": div.css(".overlay span::text").extract_first(),
                "price": "",
                "source": "blackscreen",
                "link": response.urljoin(div.css("a::attr(href)").extract_first()),
                "picture": div.css("img::attr(src)").extract_first(),
                "first_seen": scrape_time,
                "release_date": ""
            }
        next_page = response.css(".next a::attr(href)").extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
