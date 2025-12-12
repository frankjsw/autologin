from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)

driver.get("https://ap-southeast-1.run.claw.cloud/signin")
time.sleep(5)

github_btn = driver.find_element(By.XPATH, "//button[.//span[contains(text(),'GitHub')]]")
github_btn.click()

print("已点击 GitHub 登录按钮")

driver.quit()
