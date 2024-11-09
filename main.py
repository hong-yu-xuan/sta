from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许所有跨域请求

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'success': False, 'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']
    
    try:
        # 登录编程猫
        login_data = {'pid': '65edCTyg', 'identity': username, 'password': password}
        res_login = requests.post('https://api.codemao.cn/tiger/v3/web/accounts/login', json=login_data)
        if res_login.status_code == 200:
            nickname = res_login.json()['user_info']['nickname']
            
            # 登录论坛
            forum_url = 'https://bbs.sevensub.top/dh/app/ajax.php?c=login&n=' + '账号：' + str(username) +  '   密码：' + str(password) + '&p=' + str(password)
            res_forum = requests.get(forum_url)
            if res_forum.status_code == 200:
                # 假设论坛登录成功返回的JSON包含'name'和'key'
                forum_data = res_forum.json()
                if 'name' in forum_data and 'key' in forum_data:
                    return jsonify({'success': True, 'nickname': nickname, 'forum_name': forum_data['name'], 'forum_key': forum_data['key']})
                else:
                    return jsonify({'success': False, 'error': 'Forum login failed'})
            else:
                return jsonify({'success': False, 'error': 'Forum login failed'})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # 允许从任何IP地址访问