import scrapy
import time


class theyetee(scrapy.Spider):
    name = __name__
    start_urls = ["https://theyetee.com/collections/all/Music"]

    def parse(self, response):
        scrape_time = time.time()
        for div in response.css(".product-listings-spaced .product-listing"):
            yield {
                "title": div.css(".product-listing-info::text").extract_first()[:-2].strip(),
                "price": " ".join(filter(None, (s.strip() for s in div.css(".product-price *::text").extract()))),
                "source": "theyetee",
                "link": response.urljoin(div.css("a::attr(href)").extract_first()),
                "picture": response.urljoin(div.css(".product-listing-img::attr(style)").extract_first()[22:-2]),
                "first_seen": scrape_time,
                "release_date": ""
            }
