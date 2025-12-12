import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 从 Secrets 环境变量读取 GitHub 账号密码
USERNAME = os.getenv("CLAW_GH_USER")
PASSWORD = os.getenv("CLAW_GH_PASS")

if not USERNAME or not PASSWORD:
    raise ValueError("请在 GitHub Secrets 中设置 CLAW_GH_USER 和 CLAW_GH_PASS")

# Chrome 配置
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

# 启动 Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # 打开 ClawCloud 登录页面
    driver.get("https://ap-southeast-1.run.claw.cloud/signin")
    time.sleep(2)

    # 点击 GitHub 登录按钮（可能需要根据实际页面调整定位）
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

    # 如果有授权页面，点击授权
    try:
        allow_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Authorize')]")
        allow_btn.click()
        time.sleep(3)
    except Exception:
        pass

    # 切换回 ClawCloud 页面
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(3)

    # 验证登录成功
    current_url = driver.current_url
    login_success = False

    # 方法1: 检查 URL
    if "dashboard" in current_url or "console" in current_url:
        login_success = True

    # 方法2: 检查页面元素（例如用户名显示在右上角）
    try:
        user_element = driver.find_element(By.XPATH, f"//span[contains(text(), '{USERNAME}')]")
        login_success = True
    except:
        pass

    if login_success:
        print("✅ 登录成功")
        print("当前 URL:", driver.current_url)
        # 可选: 输出控制台项目数量
        try:
            projects = driver.find_elements(By.CLASS_NAME, "project-card")  # 根据实际页面调整
            print(f"发现 {len(projects)} 个项目")
        except:
            pass
    else:
        print("❌ 登录失败")
        print("当前 URL:", driver.current_url)

finally:
    driver.quit()
