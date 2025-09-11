# -*- coding:utf-8 -*-
import html
import logging

from util.ChromeBrowser import BrowserUtil
from util.ConfigUtil import PropertiesUtil, LoggerUtil
from util.DateUtil import DateUtil

from processor.HKTVmallProcessor import LogonProcessor, ConsignmentProcessor, PrintWaybillsAndInvoiceProcessor

LoggerUtil.loadLogger_defaults()
log = logging.getLogger(__name__)

if __name__ == '__main__':
    configs = PropertiesUtil.read_properties_file_defaults()

    ## 登陆并更新Token
    logonProcessor = LogonProcessor()
    logonProcessor.requestHeaders.updateHeadersByKey("Authorization","Bearer "+logonProcessor.getResponse()['accessToken'])
    logonProcessor.requestHeaders.dumpToFile()

    ## 获取页面订单数据
    consignmentProcessor = ConsignmentProcessor()
    consignmentDynformValues ={
        "startDate": DateUtil.dateFromat_UTC_8T(DateUtil.getNow_startOfDay()),
        "endDate": DateUtil.dateFromat_UTC_8T(DateUtil.getNow_endOfDay())
    }
    consigmentOrders = consignmentProcessor.getResponse(dynamicParams=consignmentDynformValues)

    ## 输出电子面单
    printWaybillsAndInvoiceProcessor = PrintWaybillsAndInvoiceProcessor()
    for consigmentOrderData in consigmentOrders:
        dynformValues = {
            "waybills": consigmentOrderData['waybillNumber'],
            "shipmentIds": consigmentOrderData['consignmentCode'],
            "orderIds": consigmentOrderData['orderId'],
        }
        BrowserUtil.blobToPdf(
            html.unescape(printWaybillsAndInvoiceProcessor.getResponse(dynamicParams=dynformValues)['result']),
            pdfName=configs['hktvlablespath'] + consigmentOrderData['waybillNumber'],
            chromedriverPath=configs['chromedriverpath'], optionsArgument=["--headless"])