# 最终版
from flask import Flask, render_template_string, request, jsonify
import sqlite3
import os  # 处理数据库文件路径

app = Flask(__name__)


# === 1. 初始化测试数据库 ===
def init_db():
    # SQLite是文件数据库，加check_same_thread=False（允许多线程访问，适配并发）
    conn = sqlite3.connect("users.db", check_same_thread=False)
    c = conn.cursor()
    # 给username加唯一索引（加速查重，优化并发注册）
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)''')
    # 插入测试用户（复用原逻辑）
    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("test", "123456"))
    conn.commit()
    conn.close()


# 初始化数据库（启动时执行）
init_db()

# === 2. 登录页面 ===
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>用户登录</title>
    <style>
        .login-box { width: 300px; margin: 50px auto; padding: 20px; border: 1px solid #ccc; }
        .login-box h2 { text-align: center; margin-bottom: 20px; }
        .form-item { margin-bottom: 15px; }
        .form-item label { display: block; margin-bottom: 5px; }
        .form-item input { width: 100%; padding: 8px; box-sizing: border-box; }
        .login-btn { width: 100%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>用户登录</h2>
        <form id="login-form" method="POST" action="/login">
            <div class="form-item">
                <label for="username">用户名：</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-item">
                <label for="password">密码：</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="login-btn">登录</button>
        </form>
    </div>
</body>
</html>
"""


@app.route('/')
@app.route('/login', methods=["GET"])
def login_page():
    """返回登录页面"""
    return render_template_string(LOGIN_HTML)


# === 3. 注册接口 ===
@app.route('/register', methods=["POST"])
def register_api():
    """用户注册接口（防SQL注入，适配并发）"""
    # 兼容JSON/表单请求（复用原登录接口的逻辑）
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        return jsonify({"success": False, "message": "用户名/密码不能为空"}), 400

    # 复用原参数化查询逻辑（防SQL注入）
    sql = "INSERT INTO users (username, password) VALUES (?, ?)"

    try:
        # SQLite并发优化：加check_same_thread=False
        conn = sqlite3.connect("users.db", check_same_thread=False)
        c = conn.cursor()
        # 插入数据（唯一索引自动防止重复注册）
        c.execute(sql, (username, password))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "注册成功"}), 201
    except sqlite3.IntegrityError:
        # 用户名重复（唯一索引触发）
        return jsonify({"success": False, "message": "用户名已存在"}), 409
    except Exception as e:
        return jsonify({"success": False, "message": f"服务器错误：{str(e)}"}), 400


# === 4. 防SQL注入的登录接口 ===
@app.route('/login', methods=["POST"])
def login_api_protect():
    """登录接口（参数化查询，防护SQL注入）"""
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    username = data.get("username", "")
    password = data.get("password", "")

    # 参数化查询（SQLite用?作为占位符）
    sql = "SELECT * FROM users WHERE username = ? AND password = ?"

    try:
        conn = sqlite3.connect("users.db", check_same_thread=False)  # 新增：适配并发
        c = conn.cursor()
        c.execute(sql, (username, password))  # 参数化执行，自动转义特殊字符
        user = c.fetchone()
        conn.close()

        if user:
            return jsonify({"success": True, "message": "登录成功"}), 200
        else:
            return jsonify({"success": False, "message": "用户名或密码错误"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": f"服务器错误：{str(e)}"}), 400


if __name__ == "__main__":
    # 关闭debug的重载（避免并发冲突），保留原端口
    app.run(debug=False, port=5000)