import scrapy
import json
import pandas as pd
from scrapy import Field
import csv
from w3lib.html import remove_tags

# df = pd.read_csv('../Data-science-project/data/crawl/cars.csv')
# car_urls = list(map(lambda x: x.split('\t')[1], df['\tcar'].tolist()))

class MyItem(scrapy.item.Item):
    name = Field()
    price = Field()
    url = Field()
    eLabel = Field()
    length = Field()
    bodyType = Field()
    emissionsCO2 = Field()
    model = Field()
    brand = Field()
    cargoVolume = Field()
    driveWheelConfiguration = Field()
    fuelConsumption = Field()
    engineCapacity = Field()
    vEenginePower = Field()
    modelDate = Field()
    fuelType = Field()
    numberOfAxles = Field()
    numberOfDoors = Field()
    numberOfForwardGears = Field()
    seatingCapacity = Field()
    vehicleTransmission = Field()
    roofLoad = Field()
    accelerationTime = Field()
    fuelCapacity = Field()
    speed = Field()
    payload = Field()
    trailerWeight = Field()
    vEengineType = Field()
    vEfuelType = Field()
    vEengineDisplacement = Field()
    torque = Field()
    weightTotal = Field()
    wheelbase = Field()
    height = Field()
    weight = Field()
    width = Field()
    curbWeight = Field()


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        # urls = car_urls
        urls = [
            'https://www.cars-data.com/en/honda-civic-tourer-1.8-lifestyle-specs/76033',
            'http://www.cars-data.com/en/opel-rekord-2.2i-cd-specs/71211'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
        # keys = data[0].keys()
        # with open('cars_data.csv', 'w', newline='', encoding='utf8') as output_file:
        #     dict_writer = csv.DictWriter(output_file, keys)
        #     dict_writer.writeheader()
        #     dict_writer.writerows(data)

    def parse(self, response):
        item = MyItem()
        data = self.get_car_info(response, item)
        next_link = data['url'] + '/tech'
        yield scrapy.Request(url=next_link, meta={"item": item} , callback=self.parse_more_data)
        # extend_data = request.meta['item']
        # data.update(extend_data)
        # yield data

    def parse_more_data(self, response):
        item = response.meta["item"]
        item['fuelCapacity'] = 'NA'
        table_items = list(map(remove_tags, response.xpath("//tr/td[contains(@class, 'col-6')]").getall()))
        for i in range(0, len(table_items), 2):
            if table_items[i] == 'Fuel Tank Capacity:' and table_items[i+1] != "":
                item['fuelCapacity'] = table_items[i+1]

        yield item

    def get_car_info(self, response, item):
        item['price'] = 'NA'
        item['url'] = 'NA'
        item['eLabel'] = 'NA'
        item['length'] = 'NA'
        item['bodyType'] = 'NA'
        item['emissionsCO2'] = 'NA'
        item['name'] = 'NA'
        item['model'] = 'NA'
        item['brand'] = 'NA'
        item['cargoVolume'] = 'NA'
        item['driveWheelConfiguration'] = 'NA'
        item['fuelConsumption'] = 'NA'
        item['engineCapacity'] = 'NA'
        item['vEenginePower'] = 'NA'
        item['curbWeight'] = 'NA'

        # get url
        item['url'] = response.xpath("//meta[@property='og:url']").attrib['content']
        # get brand and model
        list_name = response.xpath("//li/a/span[@itemprop='name']/text()").getall()
        if len(list_name) >= 3:
            item['brand'] = list_name[1]
            item['model'] = list_name[2]
        # get name
        item['name'] = response.xpath("//meta[@property='og:title']").attrib['content']
        # get data from json file
        table_items = list(map(remove_tags, response.xpath("//tr/td[contains(@class, 'col-6')]").getall()))
        for i in range(0, len(table_items), 2):
            if table_items[i] == 'Price:' and table_items[i+1] != "":
                item['price'] = table_items[i+1]
            if table_items[i] == 'Energy Label:' and table_items[i+1] != "":
                item['eLabel'] = table_items[i+1]
            if table_items[i] == 'Length:' and table_items[i+1] != "":
                item['length'] = table_items[i+1]
            if table_items[i] == 'Body Type:' and table_items[i+1] != "":
                item['bodyType'] = table_items[i+1]
            if table_items[i] == 'Co2 Emissions:' and table_items[i+1] != "":
                item['emissionsCO2'] = table_items[i+1]
            if table_items[i] == 'Cargo Capacity:' and table_items[i+1] != "":
                item['cargoVolume'] = table_items[i+1]
            if table_items[i] == 'Drive Wheel :' and table_items[i+1] != "":
                item['driveWheelConfiguration'] = table_items[i+1]
            if table_items[i] == 'Combined Consumption:' and table_items[i+1] != "":
                item['fuelConsumption'] = table_items[i+1]
            if table_items[i] == 'Engine Capacity:' and table_items[i+1] != "":
                item['engineCapacity'] = table_items[i+1]
            if table_items[i] == 'Total Max. Power (kW):' and table_items[i+1] != "":
                item['vEenginePower'] = table_items[i+1]
            if table_items[i] == 'Curb Weight:' and table_items[i+1] != "":
                item['curbWeight'] = table_items[i+1]

        list_script_app = response.xpath("//script[@type='application/ld+json']/text()").getall()
        js = json.loads(list_script_app[0])
        # name = js.get("name", "NA")
        item['bodyType'] = js.get("bodyType", {}).get("value", "NA") if item['bodyType'] == "NA" else item['bodyType']
        item['emissionsCO2'] = js.get('emissionsCO2', "NA") if item['emissionsCO2'] == "NA" else item['emissionsCO2']
        item['modelDate'] = js.get('productionDate', "NA")
        item['fuelType'] = js.get('fuelType', "NA")
        item['numberOfAxles'] = js.get('numberOfAxles', "NA")
        item['numberOfDoors'] = js.get('numberOfDoors', "NA")
        item['numberOfForwardGears'] = js.get('numberOfForwardGears', "NA")
        item['seatingCapacity'] = js.get('vehicleSeatingCapacity', "NA")
        item['vehicleTransmission'] = js.get('vehicleTransmission', "NA")
        # model = js.get('model', "NA")
        # url = js.get('url', "NA")
        item['cargoVolume'] = js.get('cargoVolume', {}).get("value", "NA") if item['cargoVolume'] == "NA" else item['cargoVolume']
        item['roofLoad'] = js.get('roofLoad', {}).get("value", "NA")
        item['accelerationTime'] = js.get('accelerationTime', {}).get("value", "NA")
        # driveWheelConfiguration = js.get('driveWheelConfiguration', {}).get('name', "NA")
        # fuelCapacity = js.get('fuelCapacity', {}).get("value", "NA")
        item['fuelConsumption'] = js.get('fuelConsumption', {}).get("value", "NA") if item['fuelConsumption'] == 'NA' else item['fuelConsumption']
        item['speed'] = js.get('speed', {}).get("value", "NA")
        item['payload'] = js.get('payload', {}).get("value", "NA")
        item['trailerWeight'] = js.get('trailerWeight', {}).get("value", "NA")
        item['vEengineType'] = js.get('vehicleEngine', {})[0].get('engineType', "NA")
        item['vEfuelType'] = js.get('vehicleEngine', {})[0].get('fuelType', "NA")
        item['vEengineDisplacement'] = js.get('vehicleEngine', {})[0].get('engineDisplacement', {}).get("value", "NA")
        item['vEenginePower'] = js.get('vehicleEngine', {})[0].get('enginePower', {}).get("value", "NA") if item['vEenginePower'] == 'NA' else item['vEenginePower']
        item['torque'] = js.get('vehicleEngine', {})[0].get('torque', {}).get("value", "NA")
        item['weightTotal'] = js.get('weightTotal', {}).get("value", "NA")
        item['wheelbase'] = js.get('wheelbase', {}).get("value", "NA")
        item['height'] = js.get('height', {}).get("value", "NA")
        item['brand'] = js.get('manufacturer', "NA")
        item['weight'] = js.get('weight', {}).get("value", "NA")
        item['width'] = js.get('width', {}).get("value", "NA")

        return dict(url=item['url'], name=item['name'], model=item['model'], brand=item['brand'], price=item['price'], eLabel=item['eLabel'], bodyType=item['bodyType'], length=item['length'], height=item['height'], width=item['width'],
                    weight=item['weight'], weightTotal=item['weightTotal'], emissionsCO2=item['emissionsCO2'], modelDate=item['modelDate'], fuelType=item['fuelType'], numberOfAxles=item['numberOfAxles'],
                    numberOfDoors=item['numberOfDoors'], numberOfForwardGears=item['numberOfForwardGears'], seatingCapacity=item['seatingCapacity'], vehicleTransmission=item['vehicleTransmission'],
                    cargoVolume=item['cargoVolume'], roofLoad=item['roofLoad'], accelerationTime=item['accelerationTime'],
                    driveWheelConfiguration=item['driveWheelConfiguration'],
                    # fuelCapacity=fuelCapacity,
                    fuelConsumption=item['fuelConsumption'], speed=item['speed'], payload=item['payload'], trailerWeight=item['trailerWeight'],
                    vEengineType=item['vEengineType'], vEfuelType=item['vEfuelType'], vEengineDisplacement=item['vEengineDisplacement'], vEenginePower=item['vEenginePower'], torque=item['torque'])
