import requests
from bs4 import BeautifulSoup
import wikipediaapi as wiki



def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

class Page:
    def __init__(self, url=None, pageid='', wik='', children=[]):
        self.children = children #Conterrà i link interni alla pagine wiki
        self.page_id = pageid #Identificatore univoco della pagina
        self.num = 0
        self.url = url #contiene la stringa 'https://en.wikipedia.org/pageid'
        self.r = requests.get(url) #il metodo requests.get() fa il ping alla pagina desiderata
        self.categories = []
        self.wik = wik
        if wik is '':
            self.wik = wiki.Wikipedia('en') #inizializza come Singleton un'istanza della classe Wikipedia
        page_py = self.wik.page(pageid)
        self.cat = []
        if page_py.exists():
            cat = page_py.categories #elenco delle cartegorie cui la pagina identificata con pageid pertiene
            temp = []
            categories = list(cat.keys())
            categories = [w.replace(w, str(w)) for w in categories]
            for i in range(len(categories)):
                categories[i] = remove_prefix(categories[i], 'Category:') #salva le categorie della pagina come stringhe


    def getCategories(self):
        return self.categories

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
        self.seed = Page(seed, page_id) #origine del grado
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

#TODO: metodo plot che crea effettivamente il grafo.

#test
grafo = Graph('https://en.wikipedia.org/wiki/Mikhail_Alexandrovich_Gorchakov', 'Mikhail_Alexandrovich_Gorchakov')
grafo.expand()
print(grafo.temp[1])
