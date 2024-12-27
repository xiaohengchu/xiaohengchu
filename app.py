from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import bcrypt
import mysql.connector
from mysql.connector import pooling
import logging

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Flask 应用初始化
app = Flask(__name__)
#CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:8080", "http://10.207.114.43:8080"]}})
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"
jwt = JWTManager(app)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "dbudbu",
    "database": "world",
}

db_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=10, **db_config)

# 登录接口
@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.json
        username = data["username"]
        password = data["password"]
        print(username,"--username")
        # 数据库查询
        conn = db_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode(), user["password"].encode()):
            #token = create_access_token(identity={"username": username})
            token = create_access_token(identity=username)
            logging.info(f"User '{username}' logged in successfully.")
            return jsonify(access_token=token), 200
        return jsonify({"msg": "Invalid username or password"}), 401
    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({"msg": "Server error"}), 500
    
# 获取光谱年份列表
@app.route("/api/years", methods=["GET"])
@jwt_required()
def get_years():
    try:
        current_user = get_jwt_identity()  # 获取当前用户的 identity
        logging.info(f"Current user in /api/years: {current_user}")  # 打印当前用户信息
        
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        query = "SELECT DISTINCT DATE_FORMAT(Date, '%Y%m%d') AS year FROM StarSpectral ORDER BY year;"
        logging.debug(f"Executing query: {query}")
        cursor.execute(query)
        years = [row[0] for row in cursor.fetchall()]
        logging.info(f"Fetched years: {years}")  # 打印获取到的年份列表
        return jsonify(years)
    except Exception as e:
        logging.error(f"Error fetching years: {e}", exc_info=True)  # 记录完整堆栈跟踪
        return jsonify({"msg": "Server error"}), 500
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
# 获取光谱数据
@app.route("/api/spectrum", methods=["GET"])
@jwt_required()
def get_spectrum():
    try:
        years_str = request.args.get("year")
        if not years_str:
            return jsonify({"msg": "No years selected"}), 400

        logging.info(f"Received year parameter: {years_str}")
        years = [int(year.strip()) for year in years_str.split(',')]
        logging.info(f"Parsed years: {years}")

        placeholders = ', '.join(['%s'] * len(years))
        query = f"SELECT * FROM StarSpectral WHERE Date IN ({placeholders})"
        logging.debug(f"Executing query: {query}")

        conn = db_pool.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, years)
        data = cursor.fetchall()

        if not data:
            return jsonify({"msg": "No data found for the selected years"}), 404

        logging.info(f"Fetched spectrum data: {data}")
        return jsonify(data)
    except ValueError as e:
        logging.error(f"Invalid year format: {e}")
        return jsonify({"msg": "Invalid year format"}), 400
    except mysql.connector.Error as db_err:
        logging.error(f"Database error: {db_err}", exc_info=True)
        return jsonify({"msg": "Database error"}), 500
    except Exception as e:
        logging.error(f"Error fetching spectrum data: {e}", exc_info=True)
        return jsonify({"msg": "Server error"}), 500
    finally:
        # 确保仅当 conn 不为 None 且已建立连接时才关闭连接
        if 'conn' in locals() and conn is not None:
            if hasattr(conn, 'is_connected') and conn.is_connected():
                conn.close()
            else:
                logging.warning("Connection was already closed or not established.")

# 更新速度值
@app.route("/api/spectrum/speed", methods=["POST"])
@jwt_required()
def update_speed():
    try:
        data = request.json
        conn = db_pool.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE spectrum_data SET speed = %s WHERE id = %s", (data["speed"], data["id"]))
        conn.commit()
        conn.close()
        logging.info(f"Updated speed for ID {data['id']} to {data['speed']}.")
        return jsonify({"msg": "Speed updated successfully"})
    except Exception as e:
        logging.error(f"Error updating speed: {e}")
        return jsonify({"msg": "Server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)