import logging

from processor.ZaloraProcessor import LogonProcessor,OrdersProcessor

# 配置日志输出的格式
logInfoLevel = logging.DEBUG
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logInfoLevel)

chromedriverPath = '/Users/trimniu/Downloads/chromedriver-mac-x64/chromedriver'
filePath = '/Users/trimniu/Downloads/'

if __name__ == '__main__':

    logonProcessor = LogonProcessor()
    loggedCookies = logonProcessor.logon(chromedriverPath=chromedriverPath)
    logonProcessor.requestHeaders.updateCookies(newCookies=loggedCookies)
    logonProcessor.requestHeaders.dumpToFile()

    ordersProcessor = OrdersProcessor()
    ordersProcessor.downLoadFile(filePath=filePath)

