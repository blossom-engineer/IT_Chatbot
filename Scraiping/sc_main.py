from abc import ABCMeta
import requests
import xml
import xml.etree.ElementTree as ET

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# options = Options()
# options.add_argument("--headless")

# webdriver_service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(
# 	service=webdriver_service,
# 	options=options
# )

class Scraiping(metaclass=ABCMeta):
    def __init__(self, url: str) -> None:
        raise NotImplementedError

    def content_getter(self) -> None:
        raise NotImplementedError

class Scraiping_RDF(Scraiping):
    def __init__(self, url: str) -> None:
        self.URL = url
        pass

    def content_getter(self) -> None:
        res: requests.Response = requests.get(self.URL)

        # NOTE: 異常系 - ステータスコードが200以外ならエラー
        try:
            res.raise_for_status()
        except requests.HTTPError:
            print('Http Error')
            return

        xml_str = res.content.decode('utf-8')
        root = ET.fromstring(xml_str)

        for item in root.findall('{http://purl.org/rss/1.0/}item'):
            print(item[0].text)
            print(item[1].text)
            print()
        return

if __name__ == '__main__':
    sc_rdf = Scraiping_RDF(
        'https://www.ipa.go.jp/security/alert-rss.rdf'
    )
    sc_rdf.content_getter()
