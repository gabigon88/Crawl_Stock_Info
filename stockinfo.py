import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class StockInfo(object):
    def __init__(self, code, year, season):
        """
        get specific stock information!
        Parameters:
        code - a stock code.
        year - The year of Financial report.
        season - The season of Financial report.
        """
        self.code = code
        self.year = year
        self.season = season
        # 使用headless browser抓取資料
        self.fireFoxOptions = webdriver.FirefoxOptions()
        self.fireFoxOptions.headless = True
        url = 'https://mops.twse.com.tw/server-java/t164sb01?step=1&REPORT_ID=C&CO_ID=' + str(code) \
            + '&SYEAR=' + str(year) + '&SSEASON=' + str(season)
        self.driver = webdriver.Firefox(options=self.fireFoxOptions)
        self.driver.get(url)

    def getEBIT(self):
        # EBIT: 稅前淨利
        xPath = "//*[contains(text(),'繼續營業單位稅前淨利')]/../following-sibling::*[1]"
        EBIT = self.driver.find_element_by_xpath(xPath)
        return int(EBIT.text.replace(',', ''))

    def getTotalAssets(self):
        # Total Assets: 總資產
        xPath = "//*[contains(text(),'資產總計')]/../following-sibling::*[1]"
        assets = self.driver.find_element_by_xpath(xPath)
        return int(assets.text.replace(',', ''))

    def getCurrentLiabilities(self):
        # Current Liabilities: 流動負債
        xPath = "//*[contains(text(),'流動負債合計')]/../following-sibling::*[1]"
        liabilities = self.driver.find_element_by_xpath(xPath)
        return int(liabilities.text.replace(',', ''))

    def getROIC(self):
        # ROIC = EBIT/IC
        # IC = 總資產 — 流動負債
        # ROIC: 資本回報率
        # EBIT: 稅前淨利
        # IC: Invested Capital (投入資本)
        ROIC = self.getEBIT() / (self.getTotalAssets() - self.getCurrentLiabilities())
        return ROIC
    
    def getHistoryPrice(self):
        # 依照給的季份設定日期
        date = str(self.year)
        if self.season == 1:
            date = date + '0331'
        elif self.season ==2:
            date = date + '0630'
        elif self.season ==3:
            date = date + '0930'
        else:
            date = date + '1231'
        
        # 依給的參數設定網址
        url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=' + date \
            + '&stockNo=' + str(self.code)
        tempDriver = webdriver.Firefox(options=self.fireFoxOptions)
        tempDriver.get(url)
        
        # 從撈取的數據分解出要的資料，每季報表的結算一定是當月的最後一天，所以直接取倒數第一筆資料
        jsonData = tempDriver.find_element_by_xpath('/html/body').text
        text = json.loads(jsonData)
        tempDriver.quit()
        return float(text['data'][-1][6])

    def getMarketCapitalization(self):
        # 市值 = 公司股票發行總股數 × 股價
        # Market Capitalization: 公司市值
        xPath = "//*[contains(text(),'普通股股本')]/../following-sibling::*[1]"
        capitalStock = self.driver.find_element_by_xpath(xPath)
        return int(capitalStock.text.replace(',', '')) * self.getHistoryPrice()

    def getTotalLiabilities(self):
        # Total Liabilities: 總負債
        xPath = "//*[contains(text(),'負債總計')]/../following-sibling::*[1]"
        liabilities = self.driver.find_element_by_xpath(xPath)
        return int(liabilities.text.replace(',', ''))

    def getCurrentCash(self):
        # Current Cash: 當前現金
        xPath = "//*[contains(text(),'現金及約當現金')]/../following-sibling::*[1]"
        cash = self.driver.find_element_by_xpath(xPath)
        return int(cash.text.replace(',', ''))

    def getEV(self):
        # EV = 公司市值 + 總負債 — 現金
        # EV: 企業價值
        EV = self.getMarketCapitalization() + self.getTotalLiabilities() - self.getCurrentCash()
        return EV

    def getEarningsYield(self):
        # Earnings Yield = EBIT / EV
        # EBIT: 稅前淨利
        # EV: 企業價值
        EarningsYield = self.getEBIT() / self.getEV()
        return EarningsYield

    def quit(self):
        self.driver.quit()

if __name__ == '__main__':
    stocks = [2412, 3045, 4904]
    for stockCode in stocks:
        stock = StockInfo(stockCode, 2019, 2)
        print('stock {} season {}'.format(stock.code, stock.season))
        print('ROIC is {}'.format(stock.getROIC()))
        print('Earnings Yield is {}'.format(stock.getEarningsYield()))
        stock.quit()