import requests
from bs4 import BeautifulSoup as BS
from bs4 import NavigableString
import os
import json
import pickle


def IEEEdecode(obj):
    out = IEEEJournal(obj['href'], obj['name'])
    if 'impact' in obj:
        out.score(obj['impact'],obj['eigen'],obj['influence'])
    if 'info' in obj:
        out.description(obj['info'])
    if 'subjectList' in obj:
        out.subjects(obj['subjectList'])
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
        if hasattr(obj, 'info'):
            odict['info'] = obj.info
        if hasattr(obj, 'subjectList'):
            odict['subjectList'] = obj.subjectList
        return odict


class IEEEJournal:
    def __init__(self, href, name):
        self.href = href
        self.name = name

    def __str__(self):
        info = '\n' + str(self.name.encode('utf-8', 'xmlcharrefreplace'))
        if self.impact:
            info = info + ' | impact ' + str(self.impact) + ' | eigen ' + str(self.eigen) + ' | influence ' + str(self.influence)
        if self.info:            
            info = info + '\nInfo: ' + self.info.encode('utf-8')
        if self.subjectList:
            info = info + '\nSubjects: '
            for ele in self.subjectList:
                info = info + str(ele) + ' || '
        info = info + '\n'
        return info

    def score(self, impact, eigen, influence):
        self.impact = impact
        self.eigen = eigen
        self.influence = influence

    def description(self, desc):
        self.info = desc

    def subjects(self, subjectList):
        self.subjectList = subjectList



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
#scope: #journal-page-bdy > div.block.cf.jrn-aims-metrics > div.section.sec-style-a.jrnl-aims > div > span > a
#description: #main > div > p:nth-child(4)
#suject: #main > div > div:nth-child(13) > div.col-grd.col-1-grd > div > ul

prefix = 'https://ieeexplore.ieee.org/xpl/'
target = []
if os.path.isfile(journal_pkl):
    for j in journal_list:
        r = requests.get(j.href)
        soup = BS(r.text, 'html.parser')
        impact = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-org > span.num')[0]
        eigen = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-dkblu > span.num')[0]
        influence = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.jrnl-metrics.cf > a.metric.bg-blu > span.num')[0]
        j.score(impact.contents[0], eigen.contents[0], influence.contents[0])

        scope = soup.select('#journal-page-bdy > div.block.cf.jrn-aims-metrics > div.section.sec-style-a.jrnl-aims > div > span > a')[0]
        r = requests.get(prefix+scope['href'])
        soup = BS(r.text.encode('utf-8'), 'html.parser')
        description = soup.select('#main > div.block.blk-style-wht.article-blk > p > p')[0]
        subjects = [i.get_text() for i in soup.select('#main > div > div.col-2-290.cf.jrnl-abt-lists > div.col-grd.col-1-grd > div > ul > li')]
        j.description(description.get_text())
        j.subjects(subjects)

    json.dump(journal_list, open(journal_pkl, 'w'), cls=IEEEencoder)
else:
    journal_list = json.load(open(journal_pkl, 'r'), object_hook=IEEEdecode)


for j in journal_list:
    print(j)
    k = raw_input('Next...')
    if k == 1:
        target.append(j.name)



