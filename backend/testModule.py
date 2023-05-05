"""
    This file is only for testing modules or algorithms.
    It does not carry any semantic load.
"""
from getPrice.mathTask import ArithmeticMean

async def getPriсeName():
        """
            Collects Make and Model of Auto and their Aftermarket Price
        """
        
        # this process is aimed at getting the price and other important parameters
        # that will be displayed on the web but first recorded in SQLite
        
        soup = BeautifulSoup(self.response(url), 'lxml')

        c = 0
        carts = soup.find_all('a', class_='css-xb5nz8 e1huvdhj1')
        priceList = []
        for i in carts:
            c+=1
            price = int(i.find('span', {"data-ftid":"bull_price"}).text.replace(' ', ''))
            priceList.append(price)

        s = ArithmeticMean.mild(priceList)
        print(s)
