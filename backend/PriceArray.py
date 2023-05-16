from bs4 import BeautifulSoup
import aiohttp
import asyncio

async def getPriсeAuto(url: str) -> list:
    """
        FROM drom.ru

        Collects the price of a car 
        in the secondary market, passes it to a class method that calculates 
        its average cost and returns it at the output.

        Example:
            return_list_price = asyncio.run(getPriсeAuto("https://auto.drom.ru/volvo/850/generation1/restyling1/"))

        All you need to send is a link to a car of a certain make and model, 
        and by generation, then collect the prices in an array and go for 
        calculations, after which the cotreg grows where: 
                1) Arithmetic mean 
                2) Number of cars transferred
    """
    
    # this process is aimed at getting the price and other important parameters
    # that will be displayed on the web but first recorded in SQLite

    # We parse the first page in order to get the number of pages, 
    # albeit not all and all of them are not needed    

    async with aiohttp.ClientSession() as session:
        global priceList
        
        response = await session.get(url)
        soup = BeautifulSoup(await response.text(), 'lxml')
        
        itarablePage = soup.find('div', class_="css-14wh0pm e1lm3vns0")
        if itarablePage is None:
            itarablePage = 2
        else:
            itarablePage = itarablePage.find_all('div', class_='css-19tk3lt e15hqrm30')[-1].text

        tasks = []

        priceList = []
        for page in range(1, int(itarablePage)):
            task = asyncio.create_task(__getListPrice(session=session, pages=page, url=url))
            tasks.append(task)

        await asyncio.gather(*tasks)

        return priceList

async def __getListPrice(session, pages: int, url) -> None:
    # array into which prices are filled

    c = 0
    async with session.get(url + f"page{pages}/") as response:
        response_text = await response.text()

        soup = BeautifulSoup(response_text, 'lxml')
        carts = soup.find_all('a', class_='css-xb5nz8 e1huvdhj1')

        for i in carts:
            c+=1
            price = int(i.find('span', {"data-ftid":"bull_price"}).text.replace(' ', ''))
            priceList.append(price)