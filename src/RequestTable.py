import json
import re
import requests
from bs4 import BeautifulSoup


class RequestTable:
    def tabela(self, url):
        raw = requests.get(url)
        html = BeautifulSoup(raw.content, "html.parser")
        content = html.find('script', id='scriptReact').string
        data = re.findall(r'const classificacao\s*=\s*(.*?);', content)
        table = json.loads(data[0])['classificacao']
        return table

    def jogos(self, url):
        raw = requests.get(url)
        html_parser = BeautifulSoup(raw.content, "html.parser")
        content = html_parser.find('script', id='scriptReact').string
        data = re.findall(r'const listaJogos\s*=\s*(.*?)\n', content)
        list = data[0][1:-1]
        local = '{"da'
        lists = list.split(local)
        test = []
        for i in range(1, len(lists)):
            test.append(json.loads(local + lists[i][0:-1]))
        return test