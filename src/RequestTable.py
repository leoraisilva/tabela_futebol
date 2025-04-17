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

