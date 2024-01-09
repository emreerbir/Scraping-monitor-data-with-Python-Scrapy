import scrapy


class HbsonSpider(scrapy.Spider):
    name = "hepsiburada"
    allowed_domains = ["www.hepsiburada.com"]
    start_urls = [
        "https://www.hepsiburada.com/oyuncu-monitorleri-c-1988?sayfa=1",
        "https://www.hepsiburada.com/oyuncu-monitorleri-c-1988?sayfa=2",
        "https://www.hepsiburada.com/oyuncu-monitorleri-c-1988?sayfa=3",
        "https://www.hepsiburada.com/oyuncu-monitorleri-c-1988?sayfa=4",
        "https://www.hepsiburada.com/oyuncu-monitorleri-c-1988?sayfa=5",
        "https://www.hepsiburada.com/oyuncu-monitorleri-c-1988?sayfa=6",
        ]

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        cards = response.xpath('//li[@class="productListContent-zAP0Y5msy8OHn5z7T_K_"]').extract()


        for card in cards:
            product_selector = scrapy.Selector(text=card)
            
            titleMonitor = product_selector.xpath('//h3[@data-test-id="product-card-name"]/span/text()').extract()
            if not titleMonitor:
                titleMonitor = " "
            content = product_selector.xpath('//h3[@data-test-id="product-card-name"]/text()').extract()
            if not content:
                content = " "
            price = product_selector.xpath('//div[@data-test-id="price-current-price"]/text()').extract()
            if not price:
                price = " "
            pageLink = product_selector.xpath('//li[@class="productListContent-zAP0Y5msy8OHn5z7T_K_"]/div/a/@href').extract()
            if not pageLink:
                pageLink = " "

            reviewCount = product_selector.xpath('//div[@data-test-id="review"]/div[2]/text()').extract()
            if not reviewCount:
                reviewCount = "0"


            base_url = 'https://www.hepsiburada.com'

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
