import requests
from bs4 import BeautifulSoup
from json import load, dump


"""
    Calculation formula:
        The average value is the arithmetic mean, which is calculated by adding a set of 
        numbers and then dividing the resulting sum by their number.
        
    At the development stage, the project will contain many temporary solutions, 
    which will soon be replaced by improved versions.        
"""

class GetBaisData:
    def __init__(self) -> None:
        pass

    def response(self, url='https://www.drom.ru/'):
        """
            A method that takes an html page and returns the result in text format
        """

        res = requests.get(url)

        # with open('test.html', 'w') as file:
        #     file.write(res.text)

        return res.text

    def parsignRootPage(self):
        """
            Takes links and the name of the brand of the car for further parsing
        """
        
        soup = BeautifulSoup(self.response(url='https://drom.ru'), 'lxml')

        marki = soup.find('div', class_='css-1f36sr9 e1m0rp604').find_all('a')
        
        clad = []
        for i in marki:
            if i.text == "Прочие авто":
                break
            elif i.text == "Поиск объявлений":
                continue
            clad.append(
                {
                    i.text:i.get('href')
                }
            )
        
        return clad

    def getListAutoModel(self, model, urlMod):
        """
            This function will give out the names of the models,
            they are needed to automatically substitute their names in the url
        
            return object with urls on model auto
        """
        
        soup = BeautifulSoup(self.response(urlMod), 'lxml')

        modelUrl = soup.find('a', class_='css-aux21u e1px31z30')['href']

        soup = BeautifulSoup(self.response(url=modelUrl), 'lxml')

        name = []
        for lisstName in soup.find_all('div', class_='esy1m7g6'):
            modelName = lisstName.find('div', class_='e3f4v4l2').text.split(' ')[1]
            
            din = False
            for item in modelName:
                if item == " ":
                    din = True
                    break

            if din is True:
                modelName = modelName.replace(' ', ' ')

            name.append(
                {
                    'url':f"https://auto.drom.ru/{model.lower()}/{modelName.replace(',', '').lower().split(' ')[0]}"
                }
            )

        # with open(f'{model}.json', 'w') as model:
        #     dump(name, model, indent=2, ensure_ascii=False)

        return name
        ###############################################################
        
    def getPriсeName(self):
        """
            Collects Make and Model of Auto and their Aftermarket Price
        """
        with open('test.html') as file:
            src = file.read()
        
        # self.response("")

        soup = BeautifulSoup(src, 'lxml')

        c = 0
        carts = soup.find_all('a', class_='css-xb5nz8 e1huvdhj1')
        for i in carts:
            c+=1
            price = int(i.find('span', {"data-ftid":"bull_price"}).text.replace(' ', ''))

            print(price)

    def getYearsIssue(self, controlURL: str):
        """
            A function that iterates over generations and returns lists of end links
        """
        
        bas = []
        for generation in range(1, 3 + 1):
            statusGeneration = requests.get(controlURL + f"/generation{generation}/restyling0/").status_code
            if statusGeneration != 200:
                break
            for restyling in range(3):
                green = controlURL + f"/generation{generation}/restyling{restyling}/"
                fullUrl = requests.get(green).status_code
                if fullUrl != 200:
                    break
                bas.append(green)

        print(bas)

if __name__ == '__main__':
    star = GetBaisData()

    count = 0    
    for i in star.parsignRootPage():
        count += 1
        for urlYear in star.getListAutoModel(*i.keys(), *i.values()):
            star.getYearsIssue("https://auto.drom.ru/audi/a1")

        if count == 1:
            break

    # star.getYearsIssue("https://auto.drom.ru/audi/a1")