import json
import logging

from reqTools.HttpRequestProcessor import SimpleHttpRequestProcessor
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptography.fernet import Fernet


log = logging.getLogger(__name__)

class LogonProcessor(SimpleHttpRequestProcessor):
    # 设置cookie文件名称
    def setCookieFileName(self):
        return "zalora.txt"

    def logon(self,chromedriverPath):
        # 设置Selenium驱动
        service = Service(chromedriverPath)
        driver = webdriver.Chrome(service=service)

        # 打开登录页面
        driver.get('https://sellercenter.zalora.com.hk/new/user/auth/login?redirect_to=/order')

        wait = WebDriverWait(driver, 100)  # 等待最多100秒
        element_present = EC.presence_of_element_located((By.ID, 'submit'))  # 根据实际元素修改
        wait.until(element_present)

        # 找到用户名和密码的输入框
        username_input = driver.find_element(By.ID, 'email')  # 用实际的元素标识替代 'username'
        password_input = driver.find_element(By.ID, 'password')  # 用实际的元素标识替代 'password'

        # 输入用户名和密码
        cipher_suite = Fernet()
        username = cipher_suite.decrypt()
        password = cipher_suite.decrypt()

        username_input.send_keys(username)
        password_input.send_keys(password)

        # 找到登录按钮并点击
        login_button = driver.find_element(By.ID, 'submit')  # 用实际的元素标识替代 'login-button'
        login_button.click()

        # 等待特定的元素出现
        wait = WebDriverWait(driver, 100)  # 等待最多100秒
        element_present = EC.presence_of_element_located((By.ID, 'unified-communication-header'))  # 根据实际元素修改
        wait.until(element_present)

        cookies = driver.get_cookies()
        log.debug("loggedCookies:" + json.dumps(cookies))

        loggedCookies = {cookie['name']: cookie['value'] for cookie in cookies}

        # 关闭浏览器
        driver.quit()
        return loggedCookies


class OrdersProcessor(LogonProcessor):

    def setUrl(self, dynamicParams=None):
        return 'https://sellercenter.zalora.com.hk/export/index/download/export-action/Order%2COrderToShip%2COrderDocumentsAsPdf/key/843178/format/xlsx'