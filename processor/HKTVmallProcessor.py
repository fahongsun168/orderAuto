from reqTools.HttpRequestProcessor import NormalHttpRequestProcessor, PageDataHttpRequestProcessor
from reqTools.enum.MethodEnum import MethodEnum


class OrdersProcessor(NormalHttpRequestProcessor):
    """一个基本的http请求处理实现类
    该类重新实现了setCookieFileName,setUrl,setMethod,setFormValues5个抽象方法
    """

    # 设置cookie文件名称
    def setCookieFileName(self):
        return "hktvmall.txt"

    # 设置Url
    def setUrl(self, dynamicParams=None):
        return "https://merchant-order-api.shoalter.com/order/HKTV/pickListDetailCsv"

    # 设置方法
    def setMethod(self):
        return MethodEnum.POST

    # 设置表单信息
    def setStaticFormValues(self):
        # 固定不变的请求参数
        formValues = {
            "deliveryEnd": "",
            "deliveryStart": "",
            "endDate": "",
            "pickUpEnd": "2024-01-27",
            "pickUpStart": "2024-01-27",
            "startDate": "",
            "overseasWaybill": "",
            "deliveryMethod": "STANDARD_DELIVERY",
            "warehouseList": [
                "P012200101"
            ],
            "storeCode": "P0122001",
            "todayVersion": False
        }
        return formValues

class LogonProcessor(OrdersProcessor):

    # 设置Url
    def setUrl(self, dynamicParams=None):
        return "https://merchant-user-api.shoalter.com/user/login/webLogin"

    # 设置方法
    def setMethod(self):
        return MethodEnum.POST

    # 设置表单信息
    def setStaticFormValues(self):
        # 固定不变的请求参数
        formValues = {
            "userCode": "",
            "userPwd": ""
        }
        return formValues

class ConsignmentProcessor(PageDataHttpRequestProcessor):

    # 设置cookie文件名称
    def setCookieFileName(self):
        return "hktvmall.txt"

    # 设置Url
    def setUrl(self, dynamicParams=None):
        return "https://merchant-order-api.shoalter.com/order/TO_SHIP/consignments"

    # 设置方法
    def setMethod(self):
        return MethodEnum.POST


    def getTotal(self, pageJsonObj):
        """
        从当前页请求Json数据对象中解析出分页数据的总条数

        :param pageJsonObj: 当前页请求Json数据对象

        :return: 数据总条数
        """
        return pageJsonObj['pagination']['totalResults']

    def getCurrentPageDatas(self, pageJsonObj):
        """
        从当前页请求Json数据对象中解析出页面数据

        :param pageJsonObj: 当前页请求Json数据对象

        :return: 当前页数据Json对象
        """
        return pageJsonObj['data']


    def setCurrentPageNumberKey(self):
        """
        分页请求的页码属性名，例如：currentPage、pageNumber等属性名

        :return: 提交请求的页码属性key
        """
        return 'pn'

    # 设置表单信息
    def setStaticFormValues(self):
        # 固定不变的请求参数
        formValues = {
            "storeCode": {
                "eese": [],
                "hktv": [
                    "P0122001"
                ]
            },
            "warehouseId": {
                "eese": [],
                "hktv": [
                    "P012200101",
                    "P012200109"
                ]
            },
            "status": "",
            "startDate": "2024-01-29T00:00:00+0800",
            "endDate": "2024-01-29T23:59:59+0800",
            "searchDateType": "PICK_UP_DATE",
            "deliveryMode": "STANDARD_DELIVERY",
            "courier": "",
            "download": False,
            "pn": 1,
            "ps": 20,
            "sortColumn": "ISSUE_DATE",
            "sortDirection": "DESC",
            "sortBy": "HKTV",
            "orderId": [
                ""
            ],
            "waybillNumbers": [
                ""
            ],
            "additionalColumns": {
                "recipient": True,
                "deliveryBy": True,
                "referenceNumber": True,
                "accUserName": True,
                "accMobile": True,
                "remarks": True,
                "dateContactedCustomer": True,
                "changeTimes": True,
                "overseasWaybill": True,
                "overseasDispatchDateStr": True,
                "overseasCarrier": True
            }
        }
        return formValues

class PrintWaybillsAndInvoiceProcessor(OrdersProcessor):
    # 设置Url
    def setUrl(self, dynamicParams=None):
        return "https://merchant-order-api.shoalter.com/order/printWaybillsAndInvoice"

    # 设置方法
    def setMethod(self):
        return MethodEnum.POST

    # 设置表单信息
    def setStaticFormValues(self):
        # 固定不变的请求参数
        formValues = {
            "courier": "HKTV",
            "waybills": "6562194581",
            "shipmentIds": "261419458",
            "orderIds": "H240128022144-P0122001",
            "paperSize": "LABEL_WAYBILL_ONLY"
        }
        return formValues