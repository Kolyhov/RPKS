let ws;
let satellites = new Map();
let objectPosition = null;

let layout = {
    title: { text: 'GPS Map', font: { color: '#00ff00' } },
    xaxis: {
        title: 'X (км)',
        range: [-150, 150],
        gridcolor: '#333333',
        color: '#ffffff'
    },
    yaxis: {
        title: 'Y (км)',
        range: [-150, 150],
        gridcolor: '#333333',
        color: '#ffffff'
    },
    paper_bgcolor: '#111111',
    plot_bgcolor: '#000000',
    font: { color: '#ffffff' },
    margin: { t: 30, b: 30, l: 30, r: 30 }
};

Plotly.newPlot('plot', [], layout, { responsive: true, displayModeBar: false });

function connect() {
    ws = new WebSocket('ws://localhost:4001');
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleData(data);
    };
    
    ws.onclose = () => setTimeout(connect, 2000);
}

function handleData(data) {
    // Добавляем спутник
    satellites.set(data.id, {
        x: data.x,
        y: data.y,
        sentAt: data.sentAt,
        receivedAt: data.receivedAt,
        time: Date.now()
    });
  
    const now = Date.now();
    for (let [id, sat] of satellites.entries()) {
        if (now - sat.time > 3000) {
            satellites.delete(id);
        }
    }

    // Триангуляция если есть 3+ спутника
    if (satellites.size >= 3) {
        objectPosition = triangulate();
    }

    updatePlot();
    updateInfo();
}

function triangulate() {
    const sats = Array.from(satellites.values()).slice(0, 3);
    const [s1, s2, s3] = sats;
    
    // Расчет расстояний
    const lightSpeed = 299792.458; // км/с
    const r1 = ((s1.receivedAt - s1.sentAt) / 1000) * lightSpeed;
    const r2 = ((s2.receivedAt - s2.sentAt) / 1000) * lightSpeed;
    const r3 = ((s3.receivedAt - s3.sentAt) / 1000) * lightSpeed;
    
    // Триангуляция
    const A = 2 * (s2.x - s1.x);
    const B = 2 * (s2.y - s1.y);
    const C = r1*r1 - r2*r2 - s1.x*s1.x + s2.x*s2.x - s1.y*s1.y + s2.y*s2.y;
    
    const D = 2 * (s3.x - s2.x);
    const E = 2 * (s3.y - s2.y);
    const F = r2*r2 - r3*r3 - s2.x*s2.x + s3.x*s3.x - s2.y*s2.y + s3.y*s3.y;
    
    const x = (C * E - F * B) / (E * A - B * D);
    const y = (C * D - A * F) / (B * D - A * E);
    
    return { x, y };
}

function updatePlot() {
    const traces = [];
    
    // Спутники
    if (satellites.size > 0) {
        traces.push({
            x: Array.from(satellites.values()).map(s => s.x),
            y: Array.from(satellites.values()).map(s => s.y),
            mode: 'markers',
            type: 'scatter',
            name: 'Супутники',
            marker: { size: 8, color: '#00ff00', symbol: 'diamond' }
        });
    }
    
    if (objectPosition) {
        traces.push({
            x: [objectPosition.x],
            y: [objectPosition.y],
            mode: 'markers',
            type: 'scatter',
            name: 'Об\'єкт',
            marker: { size: 12, color: '#ff0000', symbol: 'circle' }
        });
    }
    
    Plotly.react('plot', traces, layout);
}

function updateInfo() {
  
    if (objectPosition) {
        document.getElementById('position').innerHTML = `
            <div class="object-pos">
                X: ${objectPosition.x.toFixed(1)} км<br>
                Y: ${objectPosition.y.toFixed(1)} км
            </div>
        `;
    } else {
        document.getElementById('position').innerHTML = 
            '<div style="color: #666;">Недостатньо супутників</div>';
    }
    
    
    if (satellites.size === 0) {
        document.getElementById('satellites').innerHTML = 
            '<div style="color: #666;">Немає сигналу</div>';
    } else {
        let html = '';
        let i = 1;
        for (let [id, sat] of satellites.entries()) {
            html += `<div class="satellite">Супутник ${i++}: ${sat.x.toFixed(0)}, ${sat.y.toFixed(0)}</div>`;
        }
        document.getElementById('satellites').innerHTML = html;
    }
}

async function updateConfig() {
    const config = {
        messageFrequency: parseInt(document.getElementById('frequency').value),
        satelliteSpeed: parseInt(document.getElementById('satSpeed').value),
        objectSpeed: parseInt(document.getElementById('objSpeed').value)
    };
    
    try {
        await fetch('http://localhost:4001/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });
    } catch (e) {
        console.log('Помилка оновлення');
    }
}

connect();