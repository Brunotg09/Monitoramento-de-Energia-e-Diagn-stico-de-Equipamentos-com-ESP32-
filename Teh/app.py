# pip install flask flask-cors flask-mail fpdf schedule
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_mail import Mail, Message
from fpdf import FPDF
import datetime
import schedule
import time
import threading
import random

app = Flask(__name__)
CORS(app)

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'brunotg2004@academico.ufs.br'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'bruno2004antoniotg@gmail.com'
app.config['MAIL_PASSWORD'] = 'bruno2004tg'
mail = Mail(app)

users = {"admin": "password123"}

# Dados fictícios para simulação
sensor_data = []

def generate_fictitious_data():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    humidity = round(random.uniform(30, 70), 2)
    temperature = round(random.uniform(20, 30), 2)
    pressure = round(random.uniform(1000, 1020), 2)
    voltage = round(random.uniform(220, 240), 2)
    current = round(random.uniform(5, 15), 2)
    sensor_data.append([now, humidity, temperature, pressure, voltage, current])

# Gera dados fictícios a cada 3 segundos
def generate_data_continuously():
    while True:
        generate_fictitious_data()
        time.sleep(3)

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

@app.route('/getData', methods=['POST'])
def get_data():
    generate_fictitious_data()
    if sensor_data:
        latest_data = sensor_data[-1]
        return jsonify({
            'temperature': latest_data[2],
            'voltage': latest_data[4],
            'current': latest_data[5],
            'pressure': latest_data[3],
            'humidity': latest_data[1]
        })
    else:
        return jsonify({'error': 'No data available'})


@app.route('/consumption')
def consumption():
    stats = calculate_consumption_stats()
    anomalies = check_anomalies(stats)
    return render_template('consumption.html', stats=stats, anomalies=anomalies)

@app.route('/getConsumptionData', methods=['GET'])
def get_consumption_data():
    return jsonify(sensor_data)

def calculate_consumption_stats():
    if not sensor_data:
        return {
            "daily_avg": [0, 0],
            "monthly_avg": [0, 0],
            "daily_total": [0],
            "monthly_total": [0]
        }
    avg_voltage = sum(data[4] for data in sensor_data) / len(sensor_data)
    avg_current = sum(data[5] for data in sensor_data) / len(sensor_data)
    total_consumption = sum(data[4] * data[5] for data in sensor_data)
    return {
        "daily_avg": [avg_voltage, avg_current],
        "monthly_avg": [avg_voltage, avg_current],
        "daily_total": [total_consumption],
        "monthly_total": [total_consumption]
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
    
    # Título e data
    pdf.cell(200, 10, txt="Relatório de Consumo", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Data: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align='L')
    pdf.ln(10)
    
    # Dados dos sensores
    for row in data:
        pdf.cell(200, 10, txt=f"Data/Hora: {row[0]}, Umidade: {row[1]}, Temperatura: {row[2]}, Pressão: {row[3]}, Voltagem: {row[4]}, Corrente: {row[5]}", ln=True, align='L')
    pdf.ln(10)
    
    # Estatísticas de consumo
    pdf.cell(200, 10, txt=f"Consumo Diário Total: {stats['daily_total'][0]:.2f} kWh", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Média Diária de Consumo: {stats['daily_avg'][0]:.2f} V, {stats['daily_avg'][1]:.2f} A", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Consumo Mensal Total: {stats['monthly_total'][0]:.2f} kWh", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Média Mensal de Consumo: {stats['monthly_avg'][0]:.2f} V, {stats['monthly_avg'][1]:.2f} A", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Status do Consumo: {anomalies}", ln=True, align='L')
    
    # Salvar PDF
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
    anomalies = check_anomalies(stats)
    send_email(sensor_data, stats, anomalies)
    return jsonify({'status': 'Email enviado com sucesso!'})

def job():
    stats = calculate_consumption_stats()
    anomalies = check_anomalies(stats)
    send_email(sensor_data, stats, anomalies)

def run_scheduler():
    schedule.every(15).days.at("08:00").do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
