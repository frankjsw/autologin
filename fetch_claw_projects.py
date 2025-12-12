import requests

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyVWlkIjoiYzVkNWUxNGYtMTFjYS00NDExLWE5OWQtOTFiNWZlYTFjMzMzIiwidXNlckNyVWlkIjoiMjI3NTQ2ZDktYjBhNS00Yjg4LThhOTUtNWIzNTcxOWUzNDY3IiwidXNlckNyTmFtZSI6IjAyYTRiMWg0IiwicmVnaW9uVWlkIjoiMTE1Mjc2ZjctOTI5MS00OTAzLWI4ZDctNzY3ZjNmYjdiNzJkIiwidXNlcklkIjoiQzJlTE5ITmhkSiIsIndvcmtzcGFjZUlkIjoibnMtMDJhNGIxaDQiLCJ3b3Jrc3BhY2VVaWQiOiI3ODE3Y2ExZi02NDY4LTQxM2QtOWYxOC02MGYyYmE1MzdiYWIiLCJpYXQiOjE3NjU1MTcxNTcsImV4cCI6MTc2NjEyMTk1N30.Ri086MJuWOVYpdF9kxDBmB-yAlgghuemAWOhIQ-9KsI'  # 替换为你的 token
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

api_url = "https://ap-southeast-1.run.claw.cloud/api/projects"  # 确认此 URL 是正确的

try:
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # 如果响应返回 4xx 或 5xx 错误，会抛出异常

    if response.status_code == 200:
        print("✅ 请求成功")
        print(response.json())
    else:
        print(f"❌ 请求失败，状态码: {response.status_code}")
        print(f"响应内容: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"请求失败，错误信息: {e}")
