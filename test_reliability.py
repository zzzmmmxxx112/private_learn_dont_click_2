import time
import requests


def test_reliability():
    start = time.time()
    success_count = 0
    fail_count = 0

    # 循环1000次发起请求，验证长时间运行稳定性
    for i in range(1000):
        res = requests.post(
            "http://127.0.0.1:5000/order",
            json={"item": "book", "qty": 1}
        )
        # 断言状态码为200（成功）或400（库存不足）
        assert res.status_code == 200 or res.status_code == 400, f"第{i + 1}次请求异常，状态码：{res.status_code}"

        if res.status_code == 200:
            success_count += 1
        else:
            fail_count += 1

        # 每100次打印进度
        if (i + 1) % 100 == 0:
            print(f"已运行{i + 1}次，成功：{success_count}，失败（库存不足）：{fail_count}")

    end = time.time()
    print(f"\n 可靠性测试完成！")
    print(f"总运行时长：{end - start:.2f} 秒")
    print(f"总请求数：1000，成功：{success_count}，失败（库存不足）：{fail_count}")


if __name__ == "__main__":
    test_reliability()