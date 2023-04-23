import requests
from bs4 import BeautifulSoup
from getPrice.mathTask import ArithmeticMean
from json import dump, load

"""
    Calculation formula:
        The average value is the arithmetic mean, which is calculated by adding a set of 
        numbers and then dividing the resulting sum by their number.
        
    At the development stage, the project will contain many temporary solutions, 
    which will soon be replaced by improved versions.        
"""

class GetBaisData:
    def __init__(self) -> None:
        self.arithmetic = ArithmeticMean()

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

        modelUrl = soup.find('a', class_='css-aux21u e1px31z30')
        if modelUrl is None:
            return None, None
        
        soup = BeautifulSoup(self.response(url=modelUrl['href']), 'lxml')

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

        return name, model.lower()
        ###############################################################
        
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

        return bas

    def getPriсeName(self, url):
        """
            Collects Make and Model of Auto and their Aftermarket Price
        """
        
        soup = BeautifulSoup(self.response(url), 'lxml')

        c = 0
        carts = soup.find_all('a', class_='css-xb5nz8 e1huvdhj1')
        priceList = []
        for i in carts:
            c+=1
            price = int(i.find('span', {"data-ftid":"bull_price"}).text.replace(' ', ''))
            priceList.append(price)

        s = self.arithmetic.mild(priceList)
        print(s)

if __name__ == '__main__':
    star = GetBaisData()

    count = 0
    sprintData = []
    for i in star.parsignRootPage():
        print(i)
        objectNon, model = star.getListAutoModel(*i.keys(), *i.values())

        sprintData.append(
            {
                model: objectNon                   
            }
        )
        
            # for i in star.getYearsIssue(urlYear['url']):
            #     print(i)
            #     star.getPriсeName(i)
            #     count += 1

        if count == 1:
            break

    with open(f'backend/ModelStore/AllUrlsModel.json', 'w') as model:
        dump(sprintData, model, indent=2, ensure_ascii=False)
