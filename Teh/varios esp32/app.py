# pip install flask mysql-connector-python flask-cors flask-mail fpdf
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
import mysql.connector
from flask_mail import Mail, Message
from fpdf import FPDF
import datetime
import schedule
import time
import threading

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="seu_usuario",
    password="sua_senha",
    database="seu_banco_de_dados"
)
cursor = db.cursor()

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'seu_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'sua_senha'
mail = Mail(app)

users = {"admin": "password123"}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('dashboard'))
        else:
            return "Login falhou. Usuário ou senha incorretos."
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    stats = calculate_consumption_stats()
    anomalies = check_anomalies(stats)
    return render_template('dashboard.html', stats=stats, anomalies=anomalies)

@app.route('/sensorData', methods=['POST'])
def get_sensor_data():
    data = request.json
    sensor = data['sensor']
    humidity = data['humidity']
    temperature = data['temperature']
    pressure = data['pressure']
    voltage = data['voltage']
    current = data['current']
    query = "INSERT INTO sensor_data (sensor, humidity, temperature, pressure, voltage, current) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (sensor, humidity, temperature, pressure, voltage, current)
    cursor.execute(query, values)
    db.commit()
    return jsonify({'status': 'success'})

@app.route('/consumption')
def consumption():
    stats = calculate_consumption_stats()
    anomalies = check_anomalies(stats)
    return render_template('consumption.html', stats=stats, anomalies=anomalies)

@app.route('/getConsumptionData', methods=['GET'])
def get_consumption_data():
    query = "SELECT * FROM sensor_data"
    cursor.execute(query)
    data = cursor.fetchall()
    return jsonify(data)

def calculate_consumption_stats():
    query = "SELECT AVG(voltage), AVG(current) FROM sensor_data WHERE timestamp >= NOW() - INTERVAL 1 DAY"
    cursor.execute(query)
    daily_avg = cursor.fetchone()
    query = "SELECT AVG(voltage), AVG(current) FROM sensor_data WHERE timestamp >= NOW() - INTERVAL 1 MONTH"
    cursor.execute(query)
    monthly_avg = cursor.fetchone()
    query = "SELECT SUM(voltage * current) FROM sensor_data WHERE timestamp >= NOW() - INTERVAL 1 DAY"
    cursor.execute(query)
    daily_total = cursor.fetchone()
    query = "SELECT SUM(voltage * current) FROM sensor_data WHERE timestamp >= NOW() - INTERVAL 1 MONTH"
    cursor.execute(query)
    monthly_total = cursor.fetchone()
    return {
        "daily_avg": daily_avg,
        "monthly_avg": monthly_avg,
        "daily_total": daily_total,
        "monthly_total": monthly_total
    }

def check_anomalies(stats):
    threshold_voltage = 240  # Exemplo de valor de referência
    threshold_current = 10  # Exemplo de valor de referência
    if stats['daily_avg'][0] > threshold_voltage or stats['daily_avg'][1] > threshold_current:
        return "Anomalia detectada"
    return "Consumo normal"

def generate_pdf(data, stats, anomalies):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Relatório de Consumo", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Data: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align='L')
    pdf.ln(10)
    for row in data:
        pdf.cell(200, 10, txt=f"Sensor: {row[1]}, Umidade: {row[2]}, Temperatura: {row[3]}, Pressão: {row[4]}, Voltagem: {row[5]}, Corrente: {row[6]}", ln=True, align='L')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Consumo Diário Total: {stats['daily_total'][0]:.2f} kWh", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Média Diária de Consumo: {stats['daily_avg'][0]:.2f} V, {stats['daily_avg'][1]:.2f} A", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Consumo Mensal Total: {stats['monthly_total'][0]:.2f} kWh", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Média Mensal de Consumo: {stats['monthly_avg'][0]:.2f} V, {stats['monthly_avg'][1]:.2f} A", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Status do Consumo: {anomalies}", ln=True, align='L')
    pdf.output("consumo.pdf")

def send_email(data, stats, anomalies):
    generate_pdf(data, stats, anomalies)
    msg = Message("Relatório de Consumo Diário", sender="seu_email@gmail.com", recipients=["destinatario_email@gmail.com"])
    msg.body = "Segue em anexo o relatório de consumo diário."
    with app.open_resource("consumo.pdf") as fp:
        msg.attach("consumo.pdf", "application/pdf", fp.read())
    mail.send(msg)

@app.route('/sendDailyReport', methods=['GET'])
def send_daily_report():
    stats = calculate_consumption_stats()
    query = "SELECT * FROM sensor_data"
    cursor.execute(query)
    data = cursor.fetchall()
    anomalies = check_anomalies(stats)
    send_email(data, stats, anomalies)
    return jsonify({'status': 'Email enviado com sucesso!'})

def job():
    stats = calculate_consumption_stats()
    query = "SELECT * FROM sensor_data WHERE DATE(timestamp) >= DATE(NOW()) - INTERVAL 15 DAY"
    cursor.execute(query)
    data = cursor.fetchall()
    anomalies = check_anomalies(stats)
    send_email(data, stats, anomalies)

def run_scheduler():
    schedule.every(15).days.at("08:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
