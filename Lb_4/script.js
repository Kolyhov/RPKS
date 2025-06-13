let ws;
let data = { 
    r: [], 
    theta: [], 
    mode: 'markers', 
    type: 'scatterpolar', 
    marker: { color: [], size: 8, colorscale: 'Viridis' } 
};

let layout = {
    polar: {
        radialaxis: { title: 'км', range: [0, 150], color: '#ffffff' },
        angularaxis: { direction: 'clockwise', color: '#ffffff' },
        bgcolor: '#000000'
    },
    paper_bgcolor: '#111111',
    plot_bgcolor: '#000000',
    font: { color: '#ffffff' },
    margin: { t: 10, b: 10, l: 10, r: 10 },
    autosize: true,
    width: null,
    height: null
};

Plotly.newPlot('chart', [data], layout, { 
    responsive: true, 
    displayModeBar: false 
}).then(() => {
    Plotly.Plots.resize('chart');
});

function connect() {
    ws = new WebSocket('ws://localhost:4000');
    
    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        process(msg);
    };
    
    ws.onclose = () => setTimeout(connect, 2000);
}

function process(msg) {
    msg.echoResponses.forEach(echo => {
        const distance = (echo.time * 299792.458) / 2;
        data.r.push(distance);
        data.theta.push(msg.scanAngle);
        data.marker.color.push(echo.power);
    });

    if (data.r.length > 8) {
        data.r.splice(0, data.r.length - 8);
        data.theta.splice(0, data.theta.length - 8);
        data.marker.color.splice(0, data.marker.color.length - 8);
    }

    Plotly.update('chart', { 
        r: [data.r], 
        theta: [data.theta], 
        'marker.color': [data.marker.color] 
    });
    
    showTargets();
}

function showTargets() {
    if (data.r.length === 0) {
        document.getElementById('targets').innerHTML = '<div style="color: #666;">Немає цілей</div>';
        return;
    }
    
    let html = '';
    for (let i = 0; i < data.r.length; i++) {
        html += `<div class="target">
            Ціль ${i + 1}: ${data.r[i].toFixed(1)}км, ${data.theta[i].toFixed(0)}°
        </div>`;
    }
    document.getElementById('targets').innerHTML = html;
}

async function updateParams() {
    const params = {
        measurementsPerRotation: parseInt(document.getElementById('measurements').value),
        rotationSpeed: parseInt(document.getElementById('speed').value),
        targetSpeed: parseInt(document.getElementById('target').value)
    };
    
    try {
        const response = await fetch('http://localhost:4000/config', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(params)
        });
        
        if (response.ok) {
            console.log('Параметри оновлено');
        }
    } catch (e) {
        console.log('Помилка оновлення:', e);
    }
}

connect();