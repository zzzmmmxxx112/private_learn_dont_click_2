# test_sql.py
import requests


def test_sql():
    """测试SQL注入payload：' OR 1=1 --"""
    # 登录接口地址
    url = "http://127.0.0.1:5000/login"
    # SQL注入payload（用户名构造注入语句，密码任意）
    payload = {
        "username": "' OR 1=1 --",  # 核心注入语句
        "password": "xxx"  # 密码任意，注入后会忽略密码校验
    }

    # 发送POST请求（JSON格式）
    res = requests.post(url, json=payload)
    print(f"响应状态码：{res.status_code}")
    print(f"响应内容：{res.json()}")

    # 断言：
    # - 漏洞版：状态码200，登录成功（注入生效）
    # - 防护版：状态码401，用户名/密码错误（注入失效）
    try:
        # 验证注入是否被防护（预期结果：要么400错误，要么返回error相关信息）
        assert res.status_code == 400 or "error" in res.text.lower() or not res.json()["success"]
        print("SQL注入被防护，测试通过！")
    except AssertionError:
        print("SQL注入成功，接口存在漏洞！")


if __name__ == "__main__":
    test_sql()