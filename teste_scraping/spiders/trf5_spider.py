import scrapy


class Trf5Spider(scrapy.Spider):
    name = "trf5"
    start_urls = ["http://www5.trf5.jus.br/cp/"]

    def parse(self, response):
        yield scrapy.FormRequest.from_response(response, formid="tipo_xmlproc",
                                               formdata={"filtro":"0015648-78.1999.4.05.0000"},
                                               clickdata={"id":"submitConsulta"},
                                               callback=self.extract_page,
        )

    def extract_page(self, response):
        self.log('visitei a página de login: {}'.format(response.url))
        numero_processo = response.xpath('//body[@class="ff"]/p[2]/text()').get()
        numero_legado = response.xpath('//body[@class="ff"]/p[3]/text()').get()
        data_autuacao = response.xpath('//table//tr//td//div//text()').get()
        envolvidos = response.xpath('//table[3]//tr//td//text()').extract()
        movimentacoes = response.xpath('//table//tr//td//text()').extract()
        self.log(numero_processo)
        self.log(numero_legado)
        self.log(data_autuacao)
        self.log(envolvidos)
        self.log(movimentacoes)