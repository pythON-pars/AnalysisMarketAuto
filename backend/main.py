import requests
from bs4 import BeautifulSoup

"""
    Calculation formula:
        The average value is the arithmetic mean, which is calculated by adding a set of 
        numbers and then dividing the resulting sum by their number.
"""

class GetBaisData:
    def __init__(self) -> None:
        pass

    def response(self, url='https://www.drom.ru/'):
        """
            A method that takes an html page and returns the result in text format
        """
        
        res = requests.get(url)

        with open('test.html', 'w') as file:
            file.write(res.text)

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
            price = i.find('span', {"data-ftid":"bull_price"}).text

if __name__ == '__main__':
    star = GetBaisData()
    # star.response(url="https://auto.drom.ru/hyundai/all/")
    star.getPriсeName()