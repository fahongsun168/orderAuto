# -*- coding:utf-8 -*-

import logging

# 配置日志输出的格式
from datetime import datetime

from processor.HKTVmallProcessor import LogonProcessor, OrdersProcessor

logInfoLevel = logging.DEBUG
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logInfoLevel)

if __name__ == '__main__':

    ## 登陆HKtvmall官网,获取token，类似ipad模拟登陆
    logonProcessor = LogonProcessor()
    logonProcessor.requestHeaders.updateHeadersByKey("Authorization","Bearer "+logonProcessor.getResponse()['accessToken'])
    logonProcessor.requestHeaders.dumpToFile()

    ## 获取订单数据，组装参数，直接http请求
    nowStr = datetime.now().strftime('%Y-%m-%d')
    dynParams = {"pickUpEnd": nowStr, "pickUpStart": nowStr}

    hktvmallOrdersProcessor = OrdersProcessor()
    orders = hktvmallOrdersProcessor.getResponse(dynamicParams=dynParams)