import os
import requests
from bs4 import BeautifulSoup

# 从 GitHub Secrets 获取 Personal Access Token
PAT = os.getenv("CLAW_GH_PAT")
if not PAT:
    raise ValueError("请在 GitHub Secrets 中设置 CLAW_GH_PAT")

# GitHub API 验证 PAT
headers = {
    "Authorization": f"token {PAT}",
    "Accept": "application/vnd.github.v3+json"
}

resp = requests.get("https://api.github.com/user", headers=headers)
if resp.status_code != 200:
    print("❌ GitHub PAT 验证失败")
    print("状态码:", resp.status_code)
    print(resp.text)
    exit(1)

user = resp.json()
print(f"✅ GitHub PAT 验证成功，登录用户: {user['login']}")

# -------------------------------
# 使用 PAT 登录 ClawCloud
# -------------------------------
# ClawCloud OAuth 登录接口
LOGIN_URL = "https://ap-southeast-1.run.claw.cloud/api/oauth/github"  # 假设 ClawCloud 提供 API
session = requests.Session()

# 这里假设 ClawCloud 支持通过 Authorization Code 或 Token 获取 session
# 如果 ClawCloud 支持 token 登录，可在这里直接传 token
payload = {
    "github_token": PAT
}
login_resp = session.post(LOGIN_URL, json=payload)

if login_resp.status_code != 200:
    print("❌ ClawCloud 登录失败")
    print(login_resp.text)
    exit(1)

print("✅ ClawCloud 登录成功")

# -------------------------------
# 获取控制台页面并解析项目列表
# -------------------------------
DASHBOARD_URL = "https://ap-southeast-1.run.claw.cloud/dashboard"
dashboard_resp = session.get(DASHBOARD_URL)

if dashboard_resp.status_code != 200:
    print("❌ 无法访问控制台")
    exit(1)

soup = BeautifulSoup(dashboard_resp.text, "html.parser")

# 假设项目列表在 class="project-card" 中
projects = soup.find_all(class_="project-card")
print(f"发现 {len(projects)} 个项目:")

for idx, project in enumerate(projects, start=1):
    title = project.find("h3")
    print(f"{idx}. {title.text.strip() if title else '未命名项目'}")
