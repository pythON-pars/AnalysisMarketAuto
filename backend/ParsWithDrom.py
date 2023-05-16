import requests
import sqlite3
from bs4 import BeautifulSoup
from PriceArray import getPriсeAuto
from getPrice.mathTask import ArithmeticMean
from json import load, dump

"""
    Calculation formula:
        The average value is the arithmetic mean, which is calculated by adding a set of 
        numbers and then dividing the resulting sum by their number.
        
    At the development stage, the project will contain many temporary solutions, 
    which will soon be replaced by improved versions.
"""

class LinkFormation:
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

        for lisstName in soup.find_all('div', class_='esy1m7g6'):
            modelName = lisstName.find('div', class_='e3f4v4l2').text.split(' ')[1]
            
            din = False
            for item in modelName:
                if item == " ":
                    din = True
                    break

            if din is True:
                modelName = modelName.replace(' ', ' ')

            url = f"https://auto.drom.ru/{model.lower()}/{modelName.replace(',', '').lower().split(' ')[0]}"

            self.getYearsIssue(url, mod=model.lower())

    def getYearsIssue(self, controlURL: str, mod):
        """
            A function that iterates over generations and returns lists of end links
        """
        
        for generation in range(1, 3 + 1):
            statusGeneration = requests.get(controlURL + f"/generation{generation}/restyling0/").status_code
            if statusGeneration != 200:
                break
            for restyling in range(3):
                green = controlURL + f"/generation{generation}/restyling{restyling}/"
                fullUrl = requests.get(green).status_code
                if fullUrl != 200:
                    break
                
                sql.execute(f"INSERT INTO urlib (model, url, generation) VALUES (?, ?, ?)", (mod + ' ' + controlURL.split('/')[-1], green, f"generation{generation} restyling{restyling}"))

                db.commit()
                
                __clark(green)

def __clark(greenLink: str) -> tuple:
    from asyncio import run

    data = run(getPriсeAuto(greenLink))
    return ArithmeticMean().mild(data)

def __getChekSumUrllib(file: str="UrlAuto.db") -> str:
    import hashlib

    checkSum = None
    with open(file, 'rb') as file:
        checkSum = hashlib.md5(file.read()).hexdigest()

    return checkSum

def __databaseCheck() -> bool:

    with open("Q.json") as qJson:
        src = load(qJson)

    if src["md5sum-UrlAuto.db"] == __getChekSumUrllib():
        return True

def get_priceDrom() -> None:
    """
        collects brands, models, generates suitable links up to the 
        generation and restyling of the car and writes all the data to sqlite.

        This module was created only to work with drom.ru
    """
    
    global db, sql

    if __databaseCheck():
        # здесь надо вызвать __clark и он будет возрощать сердную арефметическую и кол-во тачек.
        # По ссылкам будем извлекать модель и марку, а ссылки будем конечно же брать из БД
        return

    # если __clark не вернёт True, то тут то мы начинаем собирать ссылки вплоть до поколения и ристайлинга 
    # А не вернуть true он может только если в таблице какие-то повреждения или изменения - которые могут привести к аномалиям 
    # Это такой, временный сценарий равития событий

    # call the main function that parses drom.ru
    star = LinkFormation()

    # create a database
    db = sqlite3.connect("UrlAuto.db")
    sql = db.cursor()

    # create a table for collecting links
    sql.execute('CREATE TABLE IF NOT EXISTS urlib (model TEXT, url TEXT, generation TEXT)')    
    db.commit()

    # The most important thing to understand is that this is not just parsing, 
    # but the formation of clean links to each generation from car models, 
    # for deep analysis, each of the following functions performs some small task and passes the 
    # etafet until we get integer prices and other important ones auto parameters
    for i in star.parsignRootPage():
        star.getListAutoModel(*i.keys(), *i.values())

    sum = {
        "md5sum-UrlAuto.db" : __getChekSumUrllib()
    }

    with open("Q.json", 'w') as qJson:
        dump(sum, qJson, indent=2, ensure_ascii=False)

    # otherwise, the database with links is simply read and calculations are performed