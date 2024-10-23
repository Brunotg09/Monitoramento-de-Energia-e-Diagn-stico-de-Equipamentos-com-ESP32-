if (!localStorage.getItem('authenticated')) {
    window.location.href = '/';
}

// Configuração dos gráficos
const temperatureCtx = document.getElementById('temperatureChart').getContext('2d');
const voltageCtx = document.getElementById('voltageChart').getContext('2d');
const currentCtx = document.getElementById('currentChart').getContext('2d');
const pressureCtx = document.getElementById('pressureChart').getContext('2d');
const humidityCtx = document.getElementById('humidityChart').getContext('2d');

// Estrutura para armazenar os dados
const dataStorage = {
    temperature: [],
    voltage: [],
    current: [],
    pressure: [],
    humidity: []
};

// Função para calcular médias
function calculateAverage(dataArray, intervalInMinutes) {
    const currentTime = new Date().getTime();
    const intervalInMs = intervalInMinutes * 60 * 1000;
    const filteredData = dataArray.filter(item => currentTime - item.timestamp <= intervalInMs);
    if (filteredData.length === 0) return 0;
    const sum = filteredData.reduce((acc, item) => acc + item.value, 0);
    return (sum / filteredData.length).toFixed(3);
}

const temperatureChart = new Chart(temperatureCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Temperatura (°C)',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        scales: {
            x: {
                title: { display: true, text: 'Tempo (s)' },
                beginAtZero: true
            },
            y: {
                title: { display: true, text: 'Temperatura (°C)' },
                beginAtZero: true
            }
        }
    }
});

const voltageChart = new Chart(voltageCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Voltagem (V)',
            data: [],
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        scales: {
            x: {
                title: { display: true, text: 'Tempo (s)' },
                beginAtZero: true
            },
            y: {
                title: { display: true, text: 'Voltagem (V)' },
                beginAtZero: true
            }
        }
    }
});

const currentChart = new Chart(currentCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Corrente (A)',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        scales: {
            x: {
                title: { display: true, text: 'Tempo (s)' },
                beginAtZero: true
            },
            y: {
                title: { display: true, text: 'Corrente (A)' },
                beginAtZero: true
            }
        }
    }
});

const pressureChart = new Chart(pressureCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Pressão (hPa)',
            data: [],
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        scales: {
            x: {
                title: { display: true, text: 'Tempo (s)' },
                beginAtZero: true
            },
            y: {
                title: { display: true, text: 'Pressão (hPa)' },
                beginAtZero: true
            }
        }
    }
});

const humidityChart = new Chart(humidityCtx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Umidade (%)',
            data: [],
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1,
            fill: false
        }]
    },
    options: {
        scales: {
            x: {
                title: { display: true, text: 'Tempo (s)' },
                beginAtZero: true
            },
            y: {
                title: { display: true, text: 'Umidade (%)' },
                beginAtZero: true
            }
        }
    }
});

function updateCharts() {
    fetch('/getData', {
        method: 'POST'  // Usar o método POST
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('Erro ao obter dados:', data.error);
            return;
        }

        const temperature = data.temperature;
        const voltage = data.voltage;
        const current = data.current;
        const pressure = data.pressure;
        const humidity = data.humidity;
        const now = new Date().toLocaleTimeString();
        const timestamp = new Date().getTime();

        // Armazena os dados com timestamps
        dataStorage.temperature.push({ value: temperature, timestamp: timestamp });
        dataStorage.voltage.push({ value: voltage, timestamp: timestamp });
        dataStorage.current.push({ value: current, timestamp: timestamp });
        dataStorage.pressure.push({ value: pressure, timestamp: timestamp });
        dataStorage.humidity.push({ value: humidity, timestamp: timestamp });

        // Limita o número de pontos visíveis no gráfico
        const maxVisiblePoints = 50;

        // Atualiza os gráficos com os dados
        temperatureChart.data.labels.push(now);
        if (temperatureChart.data.labels.length > maxVisiblePoints) {
            temperatureChart.data.labels.shift();
            temperatureChart.data.datasets[0].data.shift();
        }
        temperatureChart.data.datasets[0].data.push(temperature);
        temperatureChart.update();
        document.getElementById('temperatureValue').innerText = `Temperatura: ${temperature.toFixed(3)} °C`;

        voltageChart.data.labels.push(now);
        if (voltageChart.data.labels.length > maxVisiblePoints) {
            voltageChart.data.labels.shift();
            voltageChart.data.datasets[0].data.shift();
        }
        voltageChart.data.datasets[0].data.push(voltage);
        voltageChart.update();
        document.getElementById('voltageValue').innerText = `Voltagem: ${voltage.toFixed(3)} V`;

        currentChart.data.labels.push(now);
        if (currentChart.data.labels.length > maxVisiblePoints) {
            currentChart.data.labels.shift();
            currentChart.data.datasets[0].data.shift();
        }
        currentChart.data.datasets[0].data.push(current);
        currentChart.update();
        document.getElementById('currentValue').innerText = `Corrente: ${current.toFixed(3)} A`;

        pressureChart.data.labels.push(now);
        if (pressureChart.data.labels.length > maxVisiblePoints) {
            pressureChart.data.labels.shift();
            pressureChart.data.datasets[0].data.shift();
        }
        pressureChart.data.datasets[0].data.push(pressure);
        pressureChart.update();
        document.getElementById('pressureValue').innerText = `Pressão: ${pressure.toFixed(3)} hPa`;

        humidityChart.data.labels.push(now);
        if (humidityChart.data.labels.length > maxVisiblePoints) {
            humidityChart.data.labels.shift();
            humidityChart.data.datasets[0].data.shift();
        }
        humidityChart.data.datasets[0].data.push(humidity);
        humidityChart.update();
        document.getElementById('humidityValue').innerText = `Umidade: ${humidity.toFixed(3)} %`;

        // Calcular médias e atualizar os gráficos
        const avgTemperature5 = calculateAverage(dataStorage.temperature, 5);
        const avgVoltage5 = calculateAverage(dataStorage.voltage, 5);
        const avgCurrent5 = calculateAverage(dataStorage.current, 5);
        const avgPressure5 = calculateAverage(dataStorage.pressure, 5);
        const avgHumidity5 = calculateAverage(dataStorage.humidity, 5);

        const avgTemperature10 = calculateAverage(dataStorage.temperature, 10);
        const avgVoltage10 = calculateAverage(dataStorage.voltage, 10);
        const avgCurrent10 = calculateAverage(dataStorage.current, 10);
        const avgPressure10 = calculateAverage(dataStorage.pressure, 10);
        const avgHumidity10 = calculateAverage(dataStorage.humidity, 10);

        const avgTemperature60 = calculateAverage(dataStorage.temperature, 60);
        const avgVoltage60 = calculateAverage(dataStorage.voltage, 60);
        const avgCurrent60 = calculateAverage(dataStorage.current, 60);
        const avgPressure60 = calculateAverage(dataStorage.pressure, 60);
        const avgHumidity60 = calculateAverage(dataStorage.humidity, 60);

        const avgTemperature1440 = calculateAverage(dataStorage.temperature, 1440);
        const avgVoltage1440 = calculateAverage(dataStorage.voltage, 1440);
        const avgCurrent1440 = calculateAverage(dataStorage.current, 1440);
        const avgPressure1440 = calculateAverage(dataStorage.pressure, 1440);
        const avgHumidity1440 = calculateAverage(dataStorage.humidity, 1440);

        console.log('Médias: 5 minutos', avgTemperature5, avgVoltage5, avgCurrent5, avgPressure5, avgHumidity5);
        console.log('Médias: 10 minutos', avgTemperature10, avgVoltage10, avgCurrent10, avgPressure10, avgHumidity10);
        console.log('Médias: 1 hora', avgTemperature60, avgVoltage60, avgCurrent60, avgPressure60, avgHumidity60);
        console.log('Médias: 24 horas', avgTemperature1440, avgVoltage1440, avgCurrent1440, avgPressure1440, avgHumidity1440);
    })
    .catch(error => console.error('Erro ao atualizar gráficos:', error));
}


function updateConsumptionMetrics() {
    fetch('/getConsumptionStats')
        .then(response => response.json())
        .then(data => {
            // Atualiza as métricas de consumo no dashboard
            document.getElementById('dailyTotal').innerText = data.daily_total.toFixed(2) + " kWh";
            document.getElementById('dailyAvg').innerText = data.daily_avg[0].toFixed(2) + " V, " + data.daily_avg[1].toFixed(2) + " A";
            document.getElementById('monthlyTotal').innerText = data.monthly_total.toFixed(2) + " kWh";
            document.getElementById('monthlyAvg').innerText = data.monthly_avg[0].toFixed(2) + " V, " + data.monthly_avg[1].toFixed(2) + " A";
            document.getElementById('anomaliesStatus').innerText = data.anomalies;
        })
        .catch(error => console.error('Erro ao atualizar métricas de consumo:', error));
}

// Chama a função para atualizar as métricas de consumo
updateConsumptionMetrics();

// Atualiza as métricas de consumo a cada 5 minutos (300000 ms)
setInterval(updateConsumptionMetrics, 300000);

setInterval(updateCharts, 3000);

updateCharts();
