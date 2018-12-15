import requests
from bs4 import BeautifulSoup
from re import sub
import wikipediaapi as wiki




class Page:
    def __init__(self, url=None, pageid='', wik='', children=[]):
        self.children = children
        self.page_id = pageid
        self.num = 0
        self.url = url
        self.r = requests.get(url)
        self.categories = []
        self.wik = wik
        if wik is '':
            self.wik = wiki.Wikipedia('en')
        page_py = self.wik.page(pageid)
        self.cat = []
        if page_py.exists():
            cat = page_py.categories
            temp = []
            categories = list(cat.keys())
            categories = [w.replace(w, str(w)) for w in categories]
            for i in range(len(categories)):
                categories[i] = remove_prefix(categories[i], 'Category:')


    def getCategories(self):
        return self.categories

    def remove_prefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text

    def addChildren(self):
        html_content = self.r.text
        soup = BeautifulSoup(html_content, 'html.parser')
        for link in [h.get('href') for h in soup.find_all('a')]:
            if str(link).startswith('/wiki/'):
                self.children.append(link)
                self.num += 1
        self.children = list(set(self.children))
        print(self.children)

    def getChildren(self):
        return self.children


class Graph:
    def __init__(self, seed, page_id):
        self.seed = Page(seed, page_id)
        self.temp = []

    def expand(self):
        self.seed.addChildren()
        children = self.seed.getChildren()
        self.temp.append([[self.seed.page_id], [children]])
        for i in range(len(children)):
            children[i] = Page('https://en.wikipedia.org' + children[i], children[i], self.seed.wik)
            children[i].addChildren()
            self.temp.append([children[i], children[i].getChildren()])

    def getTemp0(self):
        return self.temp[0]


grafo = Graph('https://en.wikipedia.org/wiki/Mikhail_Alexandrovich_Gorchakov', 'Mikhail_Alexandrovich_Gorchakov')
grafo.expand()
print(grafo.temp[1])
