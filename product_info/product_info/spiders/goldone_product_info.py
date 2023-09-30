import scrapy

class GoldoneProductInfoSpider(scrapy.Spider):
    name = "goldone_product_info"
    allowed_domains = ["www.goldonecomputer.com"]
    start_urls = ["https://www.goldonecomputer.com/"]

    def parse(self, response):
        # Step 1:  scrape all the categories' links in the gold one computer website
        urls = response.xpath("//*[@class='box-content']/ul[@id='nav-one']/li/a/@href").getall()
        for url in urls:
            category_url = response.urljoin(url)
            # print("category url in parse: ", category_url)
            yield response.follow(category_url, self.parse_category)

    def parse_category(self, response):
        # print("category url in parse_category: ", response)

        # Step 2: follow each category link that was just scraped (to view the all product in the category)
        product_urls = response.xpath("//*[@class='caption']/h4/a/@href").getall()

        # Step 3: Scrape all the link of each product (link that we can view the product in detail)
        for product_url in product_urls:
            product_url = response.urljoin(product_url)
            # print("each product_url in parse_category: ", product_url)
            yield scrapy.Request(product_url, callback=self.parse_product)

    def parse_product(self, response):
        # print("each product_url in parse_product: ", response)
        # Step 4: follow each product link (link of product detail)
        # and then scrape some information like code, title, brand, price, review count and image of each product.
        code = response.xpath("//ul[@class='list-unstyled']/li/text()").get()
        title = response.xpath("//*/h3[@class='product-title']/text()").get()
        brand = response.xpath("//ul[@class='list-unstyled']/li/a/text()").extract_first()
        price = response.xpath("//ul[@class='list-unstyled price']/li/h3/text()").get()
        review_count = response.xpath("//div[@class='rating-wrapper']/a[@class='review-count']/text()").get()
        image = response.xpath('//*[@id="tmzoom"]/@src').get()

        product_info = {
            'code': code,
            'title': title,
            'brand': brand,
            'price': price,
            'review_count': review_count,
            'image_url': image
        }
        yield product_info

        # Step 5: save the data that was just scraped in json format.
        # run command>  scrapy crawl goldone_product_info -o goldone_product_info.json