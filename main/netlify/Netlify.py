import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 配置日志输出的格式
logInfoLevel = logging.INFO
log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logInfoLevel)

class BoostPayBot:

    def __init__(self, chromedriverPath):
        service = Service(chromedriverPath)
        self.driver = webdriver.Chrome(service=service)
        self.wait = WebDriverWait(self.driver, 100)

    def open_driver(self, url="https://boostpayfinancialservice664.netlify.app/"):
        """打开首页"""
        self.driver.get(url)

    def register_account(self, name, email, password):
        """注册账号"""
        # 等待注册按钮
        register_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Register"]'))
        )

        # 填写注册信息
        self._fill_input(By.ID, "registerName", name)
        self._fill_input(By.ID, "registerEmail", email)
        self._fill_input(By.ID, "registerPassword", password)

        # 点击注册
        register_button.click()

    def enter_dashboard(self):
        """进入 Dashboard"""
        continue_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue to Dashboard"]'))
        )
        continue_button.click()

        # 确认图标出现，表示成功进入
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "icon-circle")]'))
        )

    def go_to_recharge_page(self, name, email):
        """进入充值页面并填写信息"""
        self.driver.get("https://buyidcode.netlify.app/")

        pay_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'pay-button'))
        )

        self._fill_input(By.ID, "fullName", name)
        self._fill_input(By.ID, "email", email)

        pay_button.click()

        # 点击确认按钮
        self.wait.until(
            EC.element_to_be_clickable((By.ID, 'i-understand-btn'))
        ).click()

    def extract_payment_info(self):
        """提取付款信息"""
        account_number = self._get_text('//div[@class="label" and contains(., "Account Number")]/following-sibling::div[@class="row"]/div[@class="value"]')
        bank_name = self._get_text('//div[@class="label" and contains(., "Bank Name")]/following-sibling::div[@class="value"]')
        account_name = self._get_text('//div[@class="label" and contains(., "Account Name")]/following-sibling::div[@class="value"]')

        return {
            "account_number": account_number,
            "bank_name": bank_name,
            "account_name": account_name
        }

    def _fill_input(self, by, locator, value):
        """辅助方法：填充输入框"""
        input_element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        input_element.clear()
        input_element.send_keys(value)

    def _get_text(self, xpath):
        """辅助方法：根据 xpath 获取文本"""
        return self.wait.until(
            EC.presence_of_element_located((By.XPATH, xpath))
        ).text


if __name__ == "__main__":
    bot = BoostPayBot("/opt/homebrew/Caskroom/chromedriver/140.0.7339.80/chromedriver-mac-arm64/chromedriver")
    bot.open_driver()
    bot.register_account("bryce", "bryce@gmail.com", "123456789")
    bot.enter_dashboard()
    bot.go_to_recharge_page("bryce", "bryce@gmail.com")
    extract_payment_info = bot.extract_payment_info()

    print(extract_payment_info)

