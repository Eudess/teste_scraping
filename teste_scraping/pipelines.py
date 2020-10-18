# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TesteScrapingPipeline:
    def process_item(self, item, spider):
        item['numero_legado'] = item['numero_legado'].replace("(", "")
        item['numero_legado'] = item['numero_legado'].replace(")", "")
        if item['numero_processo'] != None:
            item['numero_processo'] = item['numero_processo'].strip()
        else:
            item['numero_processo'] = item['numero_legado']

        item['data_autuacao'] = self.cleaned_data_autuacao(item['data_autuacao'])
        item['envolvidos'] = self.cleaned_envolvidos(self.cleaned_char_envolvidos(item['envolvidos']))
        item['movimentacoes'] = self.cleaned_char_movimentacoes((item['movimentacoes']))
        #item['movimentacoes'] = self.cleaned_movimentacoes(self.cleaned_list((item['movimentacoes'])))


        return item

    def cleaned_data_autuacao(self, date):
        check_date = "0123456789/"
        new_date = ""
        for char in date:
            if char in check_date:
                new_date += char
        return new_date

    def cleaned_char_envolvidos(self, envolvidos_list):
        new_list = []
        final_list = []
        new_string = ""
        string_check = ":\xa0\n\t"
        for word in envolvidos_list:
            for char in word:
                if char not in string_check:
                    new_string += char
            new_list.append(new_string)
            new_string = ""

        for word in new_list:
            if word != " ":
                final_list.append(word.strip())
        return final_list


    def cleaned_envolvidos(self, envolvidos_list):
        count1 = 0
        count2 = 1
        new_list = []
        check_string1 = "DESEMBARGADOR FEDERAL "
        check_string2 = "DESEMBARGADOR(A) FEDERAL "
        while count2 < len(envolvidos_list):
            if check_string1 in envolvidos_list[count2]:
                envolvidos_list[count2] = envolvidos_list[count2].replace(check_string1, "")
            if check_string2 in envolvidos_list[count2]:
                envolvidos_list[count2] = envolvidos_list[count2].replace(check_string2, "")
            new_list.append({envolvidos_list[count1]: envolvidos_list[count2]})
            count1 += 2
            count2 += 2
        return new_list

    def cleaned_char_movimentacoes(self, movimentacoes_list):
        new_list = []
        final_list = []
        new_string = ""
        string_check = "\xa0\n\t"
        for word in movimentacoes_list:
            for char in word:
                if char not in string_check:
                    new_string += char
            new_list.append(new_string)
            new_string = ""

        for word in new_list:
            if word != "":
                final_list.append(word.strip())
        return final_list

