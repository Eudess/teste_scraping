import scrapy
from selenium import webdriver
import time


class Trf5CnpjSpider(scrapy.Spider):
    name = "trf5_cnpj"
    start_urls = ["http://www5.trf5.jus.br/cp/"]

    def __init__(self):
        self.chrome_driver = webdriver.Chrome()
        self.cnpj = "00.000.000/0001-91"

    def parse(self, response):
        self.chrome_driver.get(response.url)
        self.chrome_driver.find_element_by_id("tipo_xmlcpf").click()
        set_cnpj = self.chrome_driver.find_element_by_id("filtroCPF2")
        set_cnpj.send_keys(self.cnpj)
        self.chrome_driver.find_element_by_id("ordenacao_data").click()
        self.chrome_driver.find_element_by_id("submitConsulta").submit()

        self.chrome_driver.switch_to_window(self.chrome_driver.window_handles[1])
        new_url = self.chrome_driver.current_url
        time.sleep(5)
        self.log(new_url)
        request = scrapy.http.Request(new_url, callback=self.extract_link_process)

        return request

    def extract_link_process(self, response):
        self.log(response.url)
        self.log('visitei a página de login: {}'.format(response.url))
        teste = response.xpath('//body[@class="ff"]//div//text()').getall()
        #process_link = response.xpath('//body[@class="ff"]//div//div//div//text()').getall()
        #self.log(process_link)
        self.log(teste)
        #yield {"teste": process_link}

"""
    def extract_page(self, response):
        self.log('visitei a página de login: {}'.format(response.url))
        numero_processo = response.xpath('//body[@class="ff"]/p[2]/text()').get()
        numero_legado = response.xpath('//body[@class="ff"]/p[3]/text()').get()
        data_autuacao = response.xpath('//table//tr//td//div//text()').get()
        envolvidos = response.xpath('//table[3]//tr//td//text()').getall()
        movimentacoes = response.xpath('//table//tr//td//text()').extract()

        process = ProcessTrf5(numero_processo=numero_processo, numero_legado=numero_legado, data_autuacao=data_autuacao,
                              envolvidos=envolvidos, movimentacoes=movimentacoes)

        yield process
"""

