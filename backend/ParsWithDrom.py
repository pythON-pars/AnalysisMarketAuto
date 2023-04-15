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
        
        with open('test.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        marki = soup.find('div', class_='css-1f36sr9 e1m0rp604').find_all('a')
        for i in marki:
            if i.text == "Прочие авто":
                break
            elif i.text == "Поиск объявлений":
                continue
            print(i.text, i.get('href'))

    def getListAutoModel(self, model='Hyundai'):
        """
            This function will give out the names of the models,
            they are needed to automatically substitute their names in the url
        
            return object with urls on model auto
        """
        
        # self.response(url="https://auto.drom.ru/hyundai/all/")
        with open('test.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

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

        with open(f'{model}.json', 'w') as model:
            dump(name, model, indent=2, ensure_ascii=False)

        return name
        ###############################################################
        
    def getPriсeName(self):
        """
            Collects Make and Model of Auto and their Aftermarket Price
        """
        with open('test.html') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        c = 0
        carts = soup.find_all('a', class_='css-xb5nz8 e1huvdhj1')
        for i in carts:
            # print(i.text)
            c+=1
            model = i.find('span').text
            price = int(i.find('span', {"data-ftid":"bull_price"}).text.replace(' ', ''))

            print(price)

    def getYearsIssue(self, generation='generation1/restyling0/'):
        """
            Method that will fetch pages of generations of models of a certain brand, 
            a temporary solution is taken in the default parameter "generation" 
        """

        ##########
        model = "toyota"        
        marka = "mark ||"        
        ##########

        # It is necessary to check the generations, that is, it will be necessary to somehow 
        # find out which is the smallest and which is the largest generation for a particular car model
        with open('test.html') as file:
            src = file.read()

        # soup = BeautifulSoup(self.response(url=self.response(f"https://auto.drom.ru/hyundai/solaris/{generation}")), 'lxml')
        
        soup = BeautifulSoup(src, 'lxml')

        bichVar = []
        for price in soup.find_all('a', class_='css-xb5nz8 e1huvdhj1'):
            intPrice = int(price.find('span', class_='css-46itwz e162wx9x0').text.replace("₽", "").replace(" ", ''))
            bichVar.append(
                {
                    marka: [
                        model,
                        generation,
                        intPrice
                    ]
                }
            )
            
        print(bichVar)

        return bichVar

if __name__ == '__main__':
    star = GetBaisData()
    # star.response(url="https://auto.drom.ru/hyundai/all/")
    star.getYearsIssue()