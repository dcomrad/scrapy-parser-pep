import scrapy
import re

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response, *kwargs):
        lines = response.css('#numerical-index tbody tr')
        for line in lines:
            pep_link = line.css('a.reference::attr(href)').get()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get().strip()
        pep_pattern = r'PEP (?P<number>\d+) – (?P<name>.+)'

        pep_match = re.search(pep_pattern, title, re.I | re.U)
        status = response.css('dt:contains("Status") + dd abbr::text').get()

        data = {
            'number': pep_match.group(1),
            'name': pep_match.group(2),
            'status': status,
        } if pep_match else {}
        yield PepParseItem(data)
