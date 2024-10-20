from abc import ABCMeta
import requests
import xml
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup as bs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from sc_dataclass import HtmlContent

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

    def content_getter(self):
        raise NotImplementedError

class Scraiping_RDF(Scraiping):
    def __init__(self, url: str) -> None:
        self.URL = url
        pass

    def content_getter(self) -> list[str]:
        res: requests.Response = requests.get(self.URL)

        # NOTE: 異常系 - ステータスコードが200以外ならエラー
        try:
            res.raise_for_status()
        except requests.HTTPError:
            print('Http Error')
            return

        xml_str = res.content.decode('utf-8')
        root = ET.fromstring(xml_str)
        result: list[str] = []

        for item in root.findall('{http://purl.org/rss/1.0/}item'):
            result.append(item[1].text)

        return result


class Scraiping_html(Scraiping):
    def __init__(self, url: str) -> None:
        self.URL = url

    def content_getter(self) -> None:
        html = requests.get(self.URL)
        soup = bs(html.content, 'html.parser')

        # NOTE: main要素のテキストを取得
        content = soup.select('main p.article-txt')

        # NOTE: contentから文字列部分のみ抽出して配列化
        content_txt_list = [ txt.text for txt in content ]
        content_txt_list.pop()

        content_txt = ''.join(content_txt_list)

        # NOTE: ページのタイトルを取得
        title = soup.find('h1').get_text()

        page_content = HtmlContent(page_title=title, content=content_txt)

        return page_content


if __name__ == '__main__':
    sc_rdf = Scraiping_RDF(
        'https://www.ipa.go.jp/security/alert-rss.rdf'
    )
    url_list = sc_rdf.content_getter()

    for url in url_list:
        html = Scraiping_html(url)
        content = html.content_getter()
        print(content)
