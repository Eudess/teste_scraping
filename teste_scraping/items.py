import scrapy


class ProcessTrf5(scrapy.Item):
    numero_processo = scrapy.Field()
    numero_legado = scrapy.Field()
    data_autuacao = scrapy.Field()
    envolvidos = scrapy.Field()
    movimentacoes = scrapy.Field()
