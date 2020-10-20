import scrapy
from teste_scraping.items import ProcessTrf5


class Trf5Spider(scrapy.Spider):
    name = "trf5"
    start_urls = ["http://www5.trf5.jus.br/cp/"]


    def get_process_list(self):
        process_list = ["0015648-78.1999.4.05.0000", "0012656-90.2012.4.05.0000", "0043753-74.2013.4.05.0000",
                    "0002098-07.2011.4.05.8500", "0460674-33.2019.4.05.0000", "0000560-67.2017.4.05.0000"]
        return process_list

    def parse(self, response):
        for process in self.get_process_list():
            yield scrapy.FormRequest.from_response(response, formid="tipo_xmlproc",
                                                   formdata={"filtro": process},
                                                   clickdata={"id": "submitConsulta"},
                                                   callback=self.extract_page,
            )

    def extract_page(self, response):
        numero_processo = response.xpath('//body[@class="ff"]/p[2]/text()').get()
        numero_legado = response.xpath('//body[@class="ff"]/p[3]/text()').get()
        data_autuacao = response.xpath('//table//tr//td//div//text()').get()
        envolvidos = response.xpath('//table[3]//tr//td//text()').getall()
        movimentacoes = response.xpath('//table//tr//td//text()').extract()

        process = ProcessTrf5(numero_processo=numero_processo, numero_legado=numero_legado, data_autuacao=data_autuacao,
                              envolvidos=envolvidos, movimentacoes=movimentacoes)

        yield process