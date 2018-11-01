import requests
from bs4 import BeautifulSoup as BS
import os
import json


def IEEEdecode(obj):
    out = IEEEJournal(obj['href'], obj['name'])
    if 'impact' in obj:
        out.score(obj['impact'],obj['eigen'],obj['influence'])
    return out




class IEEEencoder(json.JSONEncoder):
    def default(self, obj):
        odict = {}
        odict['href'] = obj.href
        odict['name'] = obj.name
        if hasattr(obj, 'impact'):
            odict['impact'] = obj.impact
            odict['eigen'] = obj.eigen
            odict['influence'] = obj.influence
        return odict


class IEEEJournal:
    def __init__(self, href, name):
        self.href = href
        self.name = name

    def __str__(self):
        info = str(self.name.encode('utf-8'))
        if self.impact:
            info = info + ' | impact ' + str(self.impact) + ' | eigen ' + str(self.eigen) + ' | influence ' + str(self.influence)
        return info

    def score(self, impact, eigen, influence):
        self.impact = impact
        self.eigen = eigen
        self.influence = influence



journal_pkl = 'IEEEjournal.json'
if os.path.isfile(journal_pkl):
    print('Loading cached IEEE journals...')
    journal_list = json.load(open(journal_pkl, 'r'), object_hook=IEEEdecode)
else:   
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
    raw_input('!!!')
    json.dump(journal_list, open(journal_pkl, 'w'), cls=IEEEencoder)


#impact: #journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-org > span.num
#eigen: #journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-dkblu > span.num
#influence: #journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-blu > span.num
#scope: #journal-page-bdy > div.block.cf.jrn-aims-metrics.no-feat > div.section.sec-style-a.jrnl-aims.compact > div > span > a
#description: #journal-page-bdy > div.block.cf.jrn-aims-metrics.no-feat > div.section.sec-style-a.jrnl-aims.compact > div > div > p:nth-child(2)
#suject: #main > div > div:nth-child(9) > div.col-grd.col-1-grd > div > ul

for j in journal_list:
    r = requests.get(j.href)
    soup = BS(r.text, 'html.parser')
    impact = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-org > span.num')[0]
    eigen = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-dkblu > span.num')[0]
    influence = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-blu > span.num')[0]
    description = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics.no-feat')
    j.score(impact.contents[0], eigen.contents[0], influence.contents[0])
    
    print(j)
    print(description)
    k = raw_input('Next...')
    print(k.decode('ascii'))
    if (k == 27):
        print(' Move on')
        continue
    else:
        scope = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics.no-feat > div.section.sec-style-a.jrnl-aims.compact > div > span > a')[0]
        r = requests.get(scope['href'])


