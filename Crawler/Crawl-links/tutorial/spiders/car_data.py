import scrapy
import json

class CarDataSpider(scrapy.Spider):
    name = "car_data"
    allowed_domains = ["www.cars-data.com"]
    start_urls = ["https://www.cars-data.com/"]
    
    # lấy tất cả các link về các hãng xe
    def parse(self, response):
        links = response.css('section.brands_plus_most div.row div.col-5 a::attr(href)').extract()
        with open('links.json', 'w') as f:
            json.dump(links, f)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_car_links)
    # lấy tất cả các dòng xe trong từng hãng xe
    def parse_car_links(self, response):
        car_links = response.css('section.models div.col-4 a::attr(href)').extract()
        # car_links = response.css('section.models div.col-4').xpath('./a[2]/@href').extract()
        with open('car_links.json', 'a') as f:
            json.dump(car_links, f)
        for car_link in car_links:
            yield response.follow(car_link, callback=self.parse_car_links_child)
    # lấy từng mẫu xe theo từng option
    # respone.css(section.types div.col-8 div.col-6 a::attr(href)).extract()
    def parse_car_links_child(self, response):
        car_links_child = response.css('section.models div.col-4 a::attr(href)').extract()
        with open('car_links_child.json', 'a') as f:
            json.dump(car_links_child, f)
        for car_link_child in car_links_child:
            yield response.follow(car_link_child, callback=self.parse_car)
    # viết ra file json
    # lấy thông tin chi tiết từng xe theo option trên
    # url + /tech
    def parse_car(self, response):
        car = response.css('section.types div.col-8 div.row a::attr(href)').extract()
        with open('car.json', 'a') as f:
            json.dump(car, f)
        



