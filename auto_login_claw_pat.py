import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PAT = os.getenv("CLAW_GH_PAT")
if not PAT:
    raise ValueError("请在 GitHub Secrets 中设置 CLAW_GH_PAT")

# 配置 Chrome 无头模式
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    driver.get("https://ap-southeast-1.run.claw.cloud/signin")
    time.sleep(2)

    # 点击 GitHub 登录按钮
    github_btns = driver.find_elements(By.XPATH, "//button[contains(., 'GitHub')]")
    if not github_btns:
        raise Exception("未找到 GitHub 登录按钮")
    github_btns[0].click()
    time.sleep(3)

    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(2)

    # 如果 GitHub 登录需要用户名和 PAT
    try:
        username_input = driver.find_element(By.ID, "login_field")
        password_input = driver.find_element(By.ID, "password")
        username_input.send_keys("YOUR_GITHUB_USERNAME")  # 用你的 GitHub 用户名替换
        password_input.send_keys(PAT)
        driver.find_element(By.NAME, "commit").click()
        time.sleep(5)
    except:
        pass

    # 显式等待授权按钮，使用不同的定位方法
    try:
        # 等待授权按钮，使用不同的定位策略
        allow_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Authorize') or contains(text(),'Grant')]"))
        )
        allow_btn.click()
        time.sleep(3)
    except Exception as e:
        print(f"授权按钮点击失败: {e}")
        raise

    # 切换回 ClawCloud 页面
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

    # 验证登录
    login_success = False
    current_url = driver.current_url
    if "dashboard" in current_url or "console" in current_url:
        login_success = True
    else:
        try:
            projects = driver.find_elements(By.CLASS_NAME, "project-card")
            if projects:
                login_success = True
        except:
            pass

    if login_success:
        print("✅ 登录成功，当前 URL:", driver.current_url)
        projects = driver.find_elements(By.CLASS_NAME, "project-card")
        print(f"发现 {len(projects)} 个项目:")
        for idx, project in enumerate(projects, start=1):
            title = project.find_element(By.TAG_NAME, "h3").text if project.find_elements(By.TAG_NAME, "h3") else "未命名项目"
            print(f"{idx}. {title}")
    else:
        # 登录失败，截屏
        screenshot_file = "login_failed.png"
        driver.save_screenshot(screenshot_file)
        print("❌ 登录失败，当前 URL:", driver.current_url)
        print(f"已保存截图: {screenshot_file}")

finally:
    driver.quit()
