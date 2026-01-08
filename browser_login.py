from flask import Flask, render_template_string

app = Flask(__name__)

# 极简登录页面的 HTML 模板（内嵌到代码中，无需单独创建 HTML 文件）
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
        <form id="login-form">
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

@app.route('/login')
def login_page():
    """返回登录页面"""
    return render_template_string(LOGIN_HTML)

if __name__ == '__main__':
    # 启动Flask服务，端口5000，允许外部访问
    app.run(host='127.0.0.1', port=5000, debug=True)