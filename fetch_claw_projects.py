import os
import requests
import json

# 获取 GitHub Secrets 中的 CLAW_TOKEN
token = os.getenv("CLAW_TOKEN")  # 从 GitHub Actions Secret 中获取

if not token:
    raise Exception("❌ CLAW_TOKEN is missing! 请确保将 token 存储在 GitHub Secrets 中。")

# 设置 API 请求的头部，包含 Bearer token
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

# ClawCloud API URL
api_url = "https://ap-southeast-1.run.claw.cloud/api/projects"  # 请根据 ClawCloud 的文档修改此 URL

# 发送 GET 请求以获取项目信息
response = requests.get(api_url, headers=headers)

# 处理返回的响应
if response.status_code == 200:
    projects = response.json()
    print(f"✅ 成功获取 {len(projects)} 个项目:")
    for idx, project in enumerate(projects, 1):
        print(f"{idx}. {project.get('name', '未命名项目')}")

    # 将项目信息保存到一个 JSON 文件中
    with open("projects.json", "w", encoding="utf-8") as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)

else:
    print(f"❌ 获取项目失败: {response.status_code} {response.text}")
    # 打印详细错误信息
    print(f"完整错误信息: {response.content.decode('utf-8')}")
