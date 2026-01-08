from flask import Flask, request, jsonify
import pymysql
from pymysql.err import OperationalError

app = Flask(__name__)


# === 新增：数据库连接配置（适配Docker MySQL） ===
def get_db_conn():
    """获取数据库连接（模拟订单/库存存储到数据库）"""
    return pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="123456",
        database="test_db",
        charset="utf8mb4"
    )


# === 原order接口：仅新增“查询数据库库存”（替代内存库存） ===
@app.route("/order", methods=["POST"])
def order():
    item = request.json.get("item")
    qty = request.json.get("qty", 1)

    # 新增：从数据库查询库存（替代原内存inventory）
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        # 初始化库存表（首次执行创建）
        cursor.execute("CREATE TABLE IF NOT EXISTS inventory (item VARCHAR(20) PRIMARY KEY, stock INT)")
        # 初始化book库存为10
        cursor.execute("INSERT IGNORE INTO inventory (item, stock) VALUES ('book', 10)")
        conn.commit()

        # 查询库存
        cursor.execute("SELECT stock FROM inventory WHERE item = %s", (item,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "不存在的商品"}), 400
        stock = result[0]

        if stock < qty:
            return jsonify({"error": "库存不足"}), 400

        # 扣减库存
        cursor.execute("UPDATE inventory SET stock = stock - %s WHERE item = %s", (qty, item))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "剩余库存": stock - qty})

    # 捕获数据库连接异常（断开数据库时触发）
    except OperationalError as e:
        return jsonify({"error": "数据库连接失败", "msg": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "系统错误", "msg": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)