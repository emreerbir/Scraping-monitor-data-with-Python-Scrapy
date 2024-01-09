import scrapy
from scrapy import Request


class SonSpider(scrapy.Spider):
    name = "trendyol"
    allowed_domains = ["www.trendyol.com"]
    start_urls = [
        "https://www.trendyol.com/monitor-x-c103668?pi=1",
        "https://www.trendyol.com/monitor-x-c103668?pi=2",
        "https://www.trendyol.com/monitor-x-c103668?pi=3",
        "https://www.trendyol.com/monitor-x-c103668?pi=4",
        "https://www.trendyol.com/monitor-x-c103668?pi=5",
        ]

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        cards = response.xpath('//div[@class="p-card-wrppr with-campaign-view add-to-bs-card"]').extract()


        for card in cards:
            product_selector = scrapy.Selector(text=card)
            
            titleMonitor = product_selector.xpath('//span[@class="prdct-desc-cntnr-ttl"]/text()').extract()
            if not titleMonitor:
                titleMonitor = " "

            content = product_selector.xpath('//span[starts-with(@class, "prdct-desc-cntnr-name")]/text()').extract()
            if not content:
                content = " "

            price = product_selector.xpath('//div[@class="prc-box-dscntd"]/text()').extract()
            if not price:
                price = " "

            pageLink = product_selector.xpath('//div[@class="p-card-chldrn-cntnr card-border"]/a/@href').extract()
            if not pageLink:
                pageLink = " "

            reviewCount = product_selector.xpath('//span[@class="ratingCount"]/text()').extract()
            if not reviewCount:
                reviewCount = "0"


            base_url = 'https://www.trendyol.com'

            row_data = zip(titleMonitor,content,price,reviewCount,pageLink)
            for product in row_data:
                scraped_info = {
                    'titleMonitor' : product[0].strip(),
                    'content' : product[1].strip(),
                    'price' : product[2].strip(),
                    'reviewCount' : product[3].strip(),
                    'pageLink' : base_url + product[4].strip(),
                }
                yield scraped_info

            pass
