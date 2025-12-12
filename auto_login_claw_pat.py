import os
import requests

# 从 GitHub Secrets 获取 PAT
GITHUB_PAT = os.getenv("CLAW_GH_PAT")
if not GITHUB_PAT:
    raise ValueError("请在 GitHub Secrets 中设置 CLAW_GH_PAT")

# ClawCloud OAuth 回调接口（假设支持用 PAT 授权）
CLAWCLOUD_OAUTH_URL = "https://oauth.run.claw.cloud/callback"
CLAWCLOUD_API_PROJECTS = "https://ap-southeast-1.run.claw.cloud/api/projects"

# 1️⃣ 使用 GitHub PAT 获取 GitHub 用户信息
gh_headers = {"Authorization": f"token {GITHUB_PAT}"}
gh_resp = requests.get("https://api.github.com/user", headers=gh_headers)
if gh_resp.status_code != 200:
    raise Exception(f"GitHub PAT 验证失败: {gh_resp.status_code} {gh_resp.text}")

gh_user = gh_resp.json()
print(f"✅ GitHub PAT 验证成功，登录用户: {gh_user['login']}")

# 2️⃣ 使用 PAT 登录 ClawCloud（假设 OAuth 回调支持传 PAT）
# 这里我们模拟 OAuth 回调请求，把 GitHub PAT 传给 ClawCloud
claw_headers = {"Authorization": f"Bearer {GITHUB_PAT}"}
claw_resp = requests.get(CLAWCLOUD_API_PROJECTS, headers=claw_headers)

if claw_resp.status_code == 200:
    projects = claw_resp.json()
    print(f"✅ ClawCloud 登录成功，发现 {len(projects)} 个项目：")
    for idx, project in enumerate(projects, start=1):
        print(f"{idx}. {project.get('name','未命名项目')}")
else:
    print(f"❌ ClawCloud 登录失败: {claw_resp.status_code} {claw_resp.text}")
