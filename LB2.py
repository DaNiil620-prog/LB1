from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import sqlite3
import xml.etree.ElementTree as ET

app = Flask(__name__)

# [Easy] Запуск веб-сервера та обробка GET-запиту
@app.route("/", methods=["GET"])
def hello_world():
    return "Hello World!"

# [Easy-Medium] Обробка запиту з параметрами в URL
@app.route("/currency", methods=["GET"])
def get_currency_static():
    key = request.args.get('key')
    if key == "value":
        return "USD - 41,5"
    return "Invalid key or parameters"

# [Medium] Обробка заголовків запиту
@app.route("/headers", methods=["GET"])
def handle_headers():
    content_type = request.headers.get("Content-Type")
    data = {"currency": "USD", "rate": "41.5"}

    if content_type == "application/json":
        return jsonify(data)
    elif content_type == "application/xml":
        root = ET.Element("response")
        ET.SubElement(root, "currency").text = data["currency"]
        ET.SubElement(root, "rate").text = data["rate"]
        return ET.tostring(root, encoding="unicode"), 200, {'Content-Type': 'application/xml'}
    else:
        return "USD - 41,5"

# [Medium-Hard] Динамічне отримання курсів валют із API НБУ
def get_currency_rate(date):
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    params = {"date": date.strftime("%Y%m%d"), "json": "true"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        for item in data:
            if item["cc"] == "USD":
                return f"USD - {item['rate']}"
    return "Error fetching data"

@app.route("/currency/dynamic", methods=["GET"])
def get_dynamic_currency():
    param = request.args.get("param")
    if param == "today":
        today = datetime.now()
        return get_currency_rate(today)
    elif param == "yesterday":
        yesterday = datetime.now() - timedelta(days=1)
        return get_currency_rate(yesterday)
    else:
        return "Invalid parameter"

# [Hard] Збереження текстових даних у файл
@app.route("/save_to_file", methods=["POST"])
def save_to_file():
    data = request.data.decode("utf-8")
    with open("data.txt", "a") as file:
        file.write(data + "\n")
    return "Data saved to file!"

# [Hard2] Збереження текстових даних у SQLite
def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/save_to_db", methods=["POST"])
def save_to_db():
    data = request.data.decode("utf-8")
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (content) VALUES (?)", (data,))
    conn.commit()
    conn.close()
    return "Data saved to database!"

# Ініціалізація бази даних
init_db()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
