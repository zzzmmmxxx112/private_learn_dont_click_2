# test_browser.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time


def test_login_page_with_chrome():
    """使用Chrome浏览器测试"""
    print("===开始Chrome浏览器测试===")
    driver = None
    try:
        # 自动下载并配置ChromeDriver（无需手动写路径）
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(10)
        driver.get("http://127.0.0.1:5000/login")

        assert "登录" in driver.title, "页面标题未包含'登录'关键词"
        login_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login-btn"))
        )
        assert login_button.text == "登录", "登录按钮文本不正确"

        print("Chrome浏览器测试通过！")
    except Exception as e:
        print(f"Chrome浏览器测试失败：{str(e)}")
    finally:
        if driver:
            time.sleep(2)
            driver.quit()


if __name__ == "__main__":
    # 延迟3秒，确保Flask登录服务已启动
    time.sleep(3)
    # 执行所有浏览器测试
    test_login_page_with_chrome()
    print("\n 测试执行完成！")