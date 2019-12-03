# Crawl_Stock_Info
練習使用Selenium進行簡單的網頁爬蟲

## 執行指令
記得需要先安裝Selenium套件才可執行(pip install selenium)
```python
  python stockinfo.py
```

## 說明
程式會依照輸入的股票代號與時間  
計算該股當季結算時的投入資本回報率(RIOC)與收益率(Earnings Yield)  
可用在量化投資上  

本程式在撰寫上是以先達成目的為主  
在架構上使用簡單暴力的寫法  
故尚有許多可改善的地方  

本程式從頭到尾都以下從兩個網站抓取資料  
1.從 公開資訊觀測站 爬取公司歷史財報，並從中取出需要的資料  
https://mops.twse.com.tw/mops/web/t164sb03  

2.從 TWSE臺灣證券交易所 爬取每天的收盤價  
https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY.html or  
https://www.twse.com.tw/zh/page/trading/exchange/STOCK_DAY_AVG.html  

## 後記
本篇值得一提的是用來定位web element的XPath  
```python
  xPath = "//*[contains(text(),'繼續營業單位稅前淨利')]/../following-sibling::*[1]"
```
這段XPath可以切成兩段來看 
```python
  //*[contains(text(),'繼續營業單位稅前淨利')]
  /../following-sibling::*[1]
```
其中，//*[contains(text(),'繼續營業單位稅前淨利')]  
這段代表的意義其實就是 find_element_by_text  

而 /../following-sibling::\*[1]  
這段是先藉由前面的XPath定位到正確的一行  
再藉由 following-sibling::\*[1] 定位到鄰近的partner element上  
