import scrapy


class Trf5CnpjSpider(scrapy.Spider):
    name = "trf5_cnpj"
    start_urls = []

    def get_cnpj(self):
        cnpj = "00.000.000/0001-91"
        return cnpj

    def parse(self, response):
        yield scrapy.FormRequest.from_response(response, formid={"tipo_xmlcpf"},
                                               formdata={"filtroCPF2": self.get_cnpj},
                                               clickdata={"id":"submitConsulta"},
                                               callback=self.extract_link_process,
        )

    def extract_link_process(self, response):
        self.log('visitei a página de login: {}'.format(response.url))
        process_link = response.xpath('//body[@class="ff"]//div//div//div//table//tbody//tr//td//table//tbody//td//a//text()').getall()
        self.log(process_link)

        yield process_link

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

