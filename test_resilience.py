import requests
import time
import subprocess


def test_db_failure_recovery():
    # 1. 停掉MySQL容器（模拟数据库断开）
    print("=== 停止MySQL容器 ===")
    subprocess.run(["docker", "stop", "mysql_db"], check=True)
    time.sleep(2)  # 等待容器完全停止

    # 2. 发起订单请求，验证服务报错（500/503）
    print("=== 数据库断开后发起请求 ===")
    res = requests.post(
        "http://127.0.0.1:5000/order",
        json={"item": "book", "qty": 1}
    )
    print(f"请求状态码：{res.status_code}，响应内容：{res.json()}")
    assert res.status_code in (500, 503), "数据库断开后未返回错误状态码"

    # 3. 恢复MySQL容器
    print("=== 启动MySQL容器 ===")
    subprocess.run(["docker", "start", "mysql_db"], check=True)
    time.sleep(5)  # 等待数据库完全启动（MySQL启动需时间）

    # 4. 再次发起请求，验证服务恢复
    print("=== 数据库恢复后发起请求 ===")
    res2 = requests.post(
        "http://127.0.0.1:5000/order",
        json={"item": "book", "qty": 1}
    )
    print(f"请求状态码：{res2.status_code}，响应内容：{res2.json()}")
    assert res2.status_code == 200, "数据库恢复后服务未正常响应"

    print("容错性测试通过：数据库断开报错，恢复后正常！")


if __name__ == "__main__":
    test_db_failure_recovery()