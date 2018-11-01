import requests
from bs4 import BeautifulSoup as BS
import os

class IEEEJournal:
    def __init__(self, href, name):
        self.href = href
        self.name = name

    def __str__(self):
        info = self.name.encode('utf-8')
        if self.impact:
            info = info + ' impact ' + str(self.impact)
        return info

    def score(self, impact, eigen, influence):
        self.impact = impact
        self.eigen = eigen
        self.influence = influence


journal_list = []
r = requests.get('https://www.ieee.org/publications/periodicals.html')
soup = BS(r.text, 'html.parser')

##page-container > div > div:nth-child(3) > div.col-sm-9.col-xs-12 > div.section-header-container > div.rte.text.parbase > ul
div = soup.select('#page-container > div > .row > div.col-sm-9.col-xs-12 > div.section-header-container > div.rte.text.parbase > ul')
for ul in div:
    for li in ul.children:
        link = li.contents[0]['href']
        name = li.contents[0].contents[0].encode('utf-8')
        journal_list.append(IEEEJournal(li.contents[0]['href'], li.contents[0].contents[0]))

#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-org > span.num
#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-dkblu > span.num
#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-blu > span.num
for j in journal_list:
    r = requests.get(j.href)
    soup = BS(r.text, 'html.parser')
    impact = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-org > span.num')[0]
    eigen = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-dkblu > span.num')[0]
    influence = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-blu > span.num')[0]
    j.score(impact.contents[0], eigen.contents[0], influence.contents[0])
    print(j)
    key = input('Next... ')
    print('@')