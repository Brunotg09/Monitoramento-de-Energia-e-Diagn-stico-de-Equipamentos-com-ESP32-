document.addEventListener('DOMContentLoaded', function () {
    // Obter dados de consumo
    fetch('/getConsumptionData')
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById('consumptionTable').getElementsByTagName('tbody')[0];
            data.forEach(row => {
                let newRow = tableBody.insertRow();
                row.forEach(cell => {
                    let newCell = newRow.insertCell();
                    let newText = document.createTextNode(cell);
                    newCell.appendChild(newText);
                });
            });
        });

    // Obter estatísticas de consumo
    fetch('/getConsumptionStats')
        .then(response => response.json())
        .then(stats => {
            document.getElementById('dailyTotal').innerText = stats.daily_total.toFixed(2) + " kWh";
            document.getElementById('dailyAvg').innerText = stats.daily_avg[0].toFixed(2) + " V, " + stats.daily_avg[1].toFixed(2) + " A";
            document.getElementById('monthlyTotal').innerText = stats.monthly_total.toFixed(2) + " kWh";
            document.getElementById('monthlyAvg').innerText = stats.monthly_avg[0].toFixed(2) + " V, " + stats.monthly_avg[1].toFixed(2) + " A";
            document.getElementById('anomaliesStatus').innerText = stats.anomalies;
        });

    // Enviar relatório diário
    document.getElementById('sendReportBtn').addEventListener('click', function () {
        fetch('/sendDailyReport')
            .then(response => response.json())
            .then(data => {
                alert(data.status);
            });
    });
});


/*
CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    humidity FLOAT,
    temperature FLOAT,
    pressure FLOAT,
    voltage FLOAT,
    current FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
*/
