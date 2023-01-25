from scrapy.spiders import CrawlSpider, Spider, Rule
from scrapy.linkextractors import LinkExtractor
#from scrapy.spiders import CrawlSpider
#from scrapy.http import TextResponse, HtmlResponse
from crapNB import items
import re
import time

def calc_rank(cpu_hhz:str, ram_gb: str, ssd_gb:str, price_rub:str) -> float:
    '''
    вычисляем рейтинга привлекательности покупки.
    cpu_hhz int // частота процессора, МГЦ
    ram_gb int // объем ОЗУ, Гб
    ssd_gb int // объем SSD, Гб
    price_rub int // Цена, руб
    '''
    #назначу веса, чтобы рейтинг в районе 1 получался
    cpu_hhz_weigth = 1/5000        #вес для частоты процессора
    ram_gb_weigth = 1/32            #вес для объема ОЗУ
    ssd_gb_weigth = 1/3000          #вес для объема SSD
    price_rub_weigth = 1/200000     #вес для цены
    return int(cpu_hhz) * cpu_hhz_weigth + int(ram_gb) * ram_gb_weigth + int(ssd_gb) * ssd_gb_weigth + int(price_rub) * price_rub_weigth

#class ComputersSpider3(CrawlSpider):
class ComputersSpider3(Spider):
    '''
    паук для сайта https://novosibirsk.holodilnik.ru
    '''
    name = 'holod'
    allowed_domains = ['holodilnik.ru']

    start_urls = ["https://novosibirsk.holodilnik.ru/digital_tech/notebook/?page=" + str(i) for i in range(2, 15)]
    #start_urls = ["https://novosibirsk.holodilnik.ru/digital_tech/notebook/?page=5"]
    default_headers = {}

    def scrap_computers(self, response):
        '''
        выбираем данные со страницы о ноутбуке
        '''
#        new_resp = TextResponse(response.url, encoding='utf-8', body=response.text, )
        comp_href = response.url
        comp_name = response.xpath("//nav[@class='breadcrumb-wrapper']").xpath(".//span[@itemprop='name']/text()")[4].get()
        for card in response.xpath("//div[@class='params-list__item']"):    #разбираем список характеристик на странице
            param_type = card.xpath(".//div[@class='params-list__item-name']/text()").get()
            param_value = card.xpath(".//div[@class='params-list__item-value']/span/text()").get()
            if 'Частота процессора' in param_type:
                comp_CPU = param_value.split('-')[0]    #берём нижнее значение в случае частоты вида 2300-4700
            if 'Размер оперативной памяти' in param_type:
                comp_RAM = param_value
            if 'Объем жесткого диска' in param_type:
                comp_SSD = param_value.split('+')[0]       #берём нижнее значение в случае типа 1000+256
            price = response.xpath("//div[@class='region_block product-new-price-dc-view']/div[@class='product-price-block']").xpath(".//div[@class='product-price__current']/text()").get()
            price_lst = price.split()   #избавляемся от значка "рубль"
            price = price_lst[0] + price_lst[1]
        if "" in [comp_href, comp_name, comp_CPU, comp_RAM, comp_SSD, price]:  # если для какого-то поля не получили значение, не будем заносить запись в БД
            item = None
        else:
            comp_rank = calc_rank(comp_CPU, comp_RAM, comp_SSD, price)
            item = items.ComputerItem(url=comp_href, name=comp_name, cpu=comp_CPU, ram=comp_RAM, ssd=comp_SSD, price=price, rank=comp_rank)
        return item

    def parse(self, response):
#        print("parse next page:",response.url, len(response.xpath("//div[@class='product-name']/a/@href").getall()))
        for comp_page in response.xpath("//div[@class='product-name']/a/@href").getall():
            yield response.follow(comp_page, callback=self.scrap_computers)
#вариант рекурсии на parse, беря ссылку на страницу следующая и  проверяя, что она существует
        # for page in response.xpath("//nav/ul/li[@class='page-item page-next']/a/@href"):
        #     yield response.follow(page, callback=self.parse)

    # def parse_paginator(self, response):
    #     '''
    #     ходим по ссылкам на ноутбуки, имеющимся на странице.
    #     '''
    #     print(response.url)
    #     for comp_page in response.xpath("//div[@class='product-name']/a/@href").getall():
    #         yield response.follow(comp_page, callback=self.scrap_computers)
    #
    # def parse_start_url(self, response, **kwargs):
    #     '''
    #     выбираем страницы из навигатора страниц внизу стнаницы
    #     '''
    #     for comp_page in response.xpath("//nav/ul/li[@class='page-item']/a/@href").getall():
    #         yield response.follow(comp_page, callback=self.parse_paginator)



class ComputersSpider1(CrawlSpider):
    '''
    паук для сайта https://www.citilink.ru/catalog/noutbuki
    '''
    name = 'ctlnk'
    allowed_domains = ['citilink.ru']
#    APIKEY ='fafeec85911910dab5c2692382796138'
#    semi_url = f"http://api.scraperapi.com/?api_key=fafeec85911910dab5c2692382796138&url=https://www.citilink.ru/catalog/noutbuki/?p="
    start_urls = ["https://www.citilink.ru/catalog/noutbuki/?p=" + str(i) for i in range(2, 15)]
#    start_urls = ["https://www.citilink.ru/catalog/noutbuki/?p=6"]

#    start_urls = ['http://api.scraperapi.com/?api_key=fafeec85911910dab5c2692382796138&url=https://www.citilink.ru/catalog/noutbuki/?p=' + str(i) for i in range(2, 15)]

    default_headers = {}

        # rules = (
    #     Rule(LinkExtractor(allow=('noutbuki', )), callback='scrap_computers'),
    # )

    def scrap_computers1(self, response):
        '''
        для сайта https://www.citilink.ru/catalog/noutbuki с одной версией наименований классов
        '''
        # link_extractor = LinkExtractor(allow=('noutbuki',), unique=True)
        # links = link_extractor.extract_links(response)
        #time.sleep(3)  # С паузой менее 2 сек может не получить данные
        #comp_SSD = re.findall(r'\d+', '')
        for comp_full_data in response.xpath("//div[@class='ProductCardVerticalLayout ProductCardVertical__layout']"):
            #price_selector = card.xpath(".//td[@class='glt-cell gltc-cart']")
            comp_data = comp_full_data.xpath(".//div[@class='ProductCardVerticalLayout__header']")
            card = comp_data.xpath(".//a[@class=' ProductCardVertical__name  Link js--Link Link_type_default']")
            comp_href = "https://www.citilink.ru" + card.attrib['href']
            comp_data = card.attrib['title'].split(",")
            if 'IPS' in comp_data[1]:    #это поле встречается не во всех записях, поэтому удаляем его
                comp_data.pop(1)
            if 'IPS' in comp_data[2]:    #это поле встречается не во всех записях, поэтому удаляем его
                comp_data.pop(2)
            if len(comp_data) < 5:  # если по ноутбуку недостаточно данных пропускаем его
                continue
            comp_name_lst = comp_data[0].split(" ")
            comp_name = " ".join(comp_name_lst[1:])    #отрезаем слово "ноутбук", оно юникодом написано
            comp_CPU = comp_data[2]
            comp_CPU = re.findall(r'\d\.\d', comp_CPU)
            comp_CPU = ("".join(comp_CPU))
            if comp_CPU:    #если строка не пустая
                comp_CPU = str(int(float(comp_CPU.replace(",", ".")) * 1000))
            comp_RAM = comp_data[3]
            comp_RAM = re.findall(r'\d+', comp_RAM)
            comp_RAM = "".join(comp_RAM)
            comp_SSD = comp_data[4]
            comp_SSD = re.findall(r'\d+', comp_SSD)
            comp_SSD = "".join(comp_SSD)
            if 'ТБ' in comp_data[4]:    #переводим ТБ в ГБ
                comp_SSD = comp_SSD + "000"
            comp_price_data = comp_full_data.xpath(".//div[@class='ProductCardVerticalLayout__footer']")
#            price = comp_price_data.xpath(".//span[@class='ProductCardVerticalPrice__price-current_current-price js--ProductCardVerticalPrice__price-current_current-price ']")[1].get()
            price = re.findall(r'\d+', comp_price_data.xpath(".//span[@class='ProductCardVerticalPrice__price-current_current-price js--ProductCardVerticalPrice__price-current_current-price ']")[1].xpath(".//text()").get())
            price = "".join(price)
        #    ecname = price_selector.xpath(".//a").attrib.get("ecname")
#            yield {"url": comp_href, "name": comp_name, "cpu": comp_CPU, "ram": comp_RAM, "ssd": comp_SSD, "price": price}
            if "" in [comp_href, comp_name, comp_CPU, comp_RAM, comp_SSD, price]:  # если для какого-то поля не получили значение, не будем заносить запись в БД
                continue
            comp_rank = calc_rank(comp_CPU, comp_RAM, comp_SSD, price)
            item = items.ComputerItem(url=comp_href, name=comp_name, cpu=comp_CPU, ram=comp_RAM, ssd=comp_SSD, price=price, rank=comp_rank)
            #item = items.ComputerItem(url=comp_href, name=comp_name, cpu=comp_CPU, ram=comp_RAM, ssd=comp_SSD, price=price)
            yield item

    def scrap_computers2(self, response):
        '''
        !! логика не актуальная, актуальная в scrap_computers1
        для сайта https://www.citilink.ru/catalog/noutbuki с другой версией наименований классов
        '''
        time.sleep(3)  # С паузой менее 2 сек может не получить данные
        for comp_full_data in response.xpath("//div[@class='app-catalog-sjv9i2 e8bog4b0']"):
            # price_selector = card.xpath(".//td[@class='glt-cell gltc-cart']")
            comp_data = comp_full_data.xpath(".//div[@class='app-catalog-632im3 e1sv2xw70']")
            card = comp_data.xpath(".//a[@class='app-catalog-9gnskf e1259i3g0']")
            comp_href = "https://www.citilink.ru" + card.attrib['href']
            comp_data = card.attrib['title'].split(",")
            comp_name_lst = comp_data[0].split(" ")
            comp_name = " ".join(comp_name_lst[1:])  # отрезаем слово "ноутбук", оно юникодом написано
            comp_CPU = comp_data[3]
            comp_CPU = re.findall(r'\d\.\d', comp_CPU)
            comp_CPU = float("".join(comp_CPU))
            comp_RAM = comp_data[4]
            comp_RAM = re.findall(r'\d+', comp_RAM)
            comp_RAM = int("".join(comp_RAM))
            comp_SSD = comp_data[5]
            comp_SSD = re.findall(r'\d+', comp_SSD)
            comp_SSD = int("".join(comp_SSD))
            comp_price_data = comp_full_data.xpath(".//div[@class='app-catalog-gt3vul eyol3820']")
            #            price = comp_price_data.xpath(".//span[@class='ProductCardVerticalPrice__price-current_current-price js--ProductCardVerticalPrice__price-current_current-price ']")[1].get()
            price = re.findall(r'\d+', comp_price_data.xpath(
                ".//span[@class='app-catalog-0 eb8dq160']")[
                1].xpath(".//text()").get())
            price = int("".join(price))
            #    ecname = price_selector.xpath(".//a").attrib.get("ecname")
            #            yield {"url": comp_href, "name": comp_name, "cpu": comp_CPU, "ram": comp_RAM, "ssd": comp_SSD, "price": price}
            item = items.ComputerItem(url=comp_href, name=comp_name, cpu=comp_CPU, ram=comp_RAM, ssd=comp_SSD,price=price)
            yield item
    # def parse_start_url(self, response, **kwargs):
    #     for i in range(1, 20):
    #         url = self.start_urls[0] + "?p=" + str(i)
    #         print(url)
    #         return response.follow(
    #             url, callback=self.scrap_computers, headers=self.default_headers
    #         )
    def parse_start_url(self, response, **kwargs):
        return self.scrap_computers1(response)
