# auto_login_claw.py

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

USERNAME = os.getenv("GITHUB_LOGIN_USER")
PASSWORD = os.getenv("GITHUB_LOGIN_PASS")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

try:
    # 打开 ClawCloud 登录页
    driver.get("https://ap-southeast-1.run.claw.cloud/signin")
    time.sleep(2)

    # 点击 GitHub 登录按钮（定位可能需要更新）
    github_btn = driver.find_element(By.XPATH, "//button[contains(., 'GitHub')]")
    github_btn.click()
    time.sleep(2)

    # 切换到 GitHub 登录页面
    driver.switch_to.window(driver.window_handles[-1])

    # 输入 GitHub 用户名和密码
    driver.find_element(By.ID, "login_field").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.NAME, "commit").click()

    time.sleep(5)

    # 授权（如果有授权页面）
    # 这里只是示例，可能需要根据实际页面调整
    try:
        allow_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Authorize')]")
        allow_btn.click()
        time.sleep(3)
    except Exception:
        pass

    # 回到 ClawCloud 控制台
    print("登录完成，当前 URL:", driver.current_url)

finally:
    driver.quit()
