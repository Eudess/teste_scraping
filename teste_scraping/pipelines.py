import re
import json
import os

class TesteScrapingPipeline:
    def process_item(self, item, spider):
        if spider.name == "trf5":
            item['numero_legado'] = self.cleaned_numero_legado(item['numero_legado'])
            item['numero_processo'] = self.cleaned_numero_processo(item['numero_processo'], item['numero_legado'])
            item['data_autuacao'] = self.cleaned_data_autuacao(item['data_autuacao'])
            item['envolvidos'] = self.cleaned_envolvidos(self.cleaned_char_envolvidos(item['envolvidos']))
            item['movimentacoes'] = self.cleaned_movimentacoes(self.cleaned_char_movimentacoes((item['movimentacoes'])))

            self.save_file(item)

            return item

    #Função para limpar numero_legado.
    def cleaned_numero_legado(self, numero_legado):
        if numero_legado != None:
            numero_legado = numero_legado.replace("(", "")
            numero_legado = numero_legado.replace(")", "")

        return numero_legado

    #Função para limpar e vericar se o numero_processo é Vazio.
    def cleaned_numero_processo(self,numero_processo, numero_legado):
        if numero_processo == None:
            return numero_legado
        else:
            numero_processo = numero_processo.replace("PROCESSO Nº ", "")
            numero_processo = numero_processo.strip()
            return numero_processo

    #Função para limpar a data.
    def cleaned_data_autuacao(self, date):
        check_date = "0123456789/"
        new_date = ""
        for char in date:
            if char in check_date:
                new_date += char
        return new_date

    #Função para tirar os espaços em branco e os caracteres especiais como: \n \t : \xa0 da lista de envolvidos.
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

    #Função para gerar a lista de dicionário da lista envolvidos.
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

    # Função para tirar os espaços em branco e os caracteres especiais como: \n \t \xa0 da lista de movimentações.
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

    #Função para verificar se a data da lista movimentações está no formato certo.
    def check_date(self, date):
        mMatch = re.compile(r'Em \d{2}/\d{2}/\d{4} \d{2}:\d{2}')
        if re.match(mMatch, date):
            return True
    #Função que remove o que não pertence a lista movimentações e gera a lista de dicionário da lista movimentações.
    def cleaned_movimentacoes(self, movimentacoes_list):
        movimentacoes_list = movimentacoes_list
        check = 0
        while check != 1:
           if not self.check_date(movimentacoes_list[check]):
               movimentacoes_list.remove(movimentacoes_list[check])
           else:
               check = 1

        new_list = []
        date_key = ""
        date_key_index = 0
        count = 0
        while count < len(movimentacoes_list):
            if self.check_date(movimentacoes_list[count]):
                date_key = movimentacoes_list[count]
                new_list.append({date_key: []})
                date_key_index += 1
            elif not self.check_date(movimentacoes_list[count]):
                new_list[date_key_index-1][date_key].append(movimentacoes_list[count])
            count += 1
        return new_list

    #Função para verificar se um caminho específico existe.
    def check_path(self, path):
        if not os.path.exists(path):
            return True

    #Função para salvar o processo raspado num arquivo json.
    def save_file(self, item):
        name = "processo-" + self.cleaned_numero_processo(item['numero_processo'], item['numero_legado'])
        path = os.getcwd()
        final_path = path + "/teste_scraping/processos/"
        if self.check_path(final_path):
            os.mkdir(final_path)
        with open(final_path + name, 'w', encoding='utf-8') as json_file:
            json.dump(dict(item), json_file, ensure_ascii=False, indent=4)

        json_file.close()

