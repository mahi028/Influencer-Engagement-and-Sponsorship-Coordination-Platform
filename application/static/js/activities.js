function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`;
}
  
function generateRandomColors(n) {
    const colors = [];
    for (let i = 0; i < n; i++) {
        colors.push(getRandomColor());
    }
    return colors;
}

function create_data(label, data, chart_name){
    let r_data = {
        labels: label, 
        datasets: [{
            label: chart_name,
            data: data,
            backgroundColor: generateRandomColors(label.length),
            hoverOffset: 4
        }],
    };
    return r_data;
}

function new_chart(label, data, type, el, chart_name){
    new Chart(el, {
        type: type,
        data: create_data(label, data, chart_name),
        options: {
            scales: {
            y: {
                beginAtZero: true
            }
            }
        }
        });
    }

function create_chart(url, type, id, chart_name){
    const cont = document.getElementById('chart_cont');
    canv = `
        <div id="parent_${id}" style="margin: 10px; width: 300px !important; height: 300px !important;">
            <center>
                <h3>${chart_name}</h3>
                <canvas id="${id}"></canvas>
            </center>
        </div>
    `;
    if(cont.children.length%3 == 0){
        canv.innerHTML += '<\n>';
    };
    cont.innerHTML += canv;

    setTimeout(()=>{
        const el = document.getElementById(id);
        fetch(url)
        .then(response=>{return response.json()})
        .then(data=>{
            let label = Object.keys(data);
            let n_data = Object.values(data);
            new_chart(label, n_data, type, el, chart_name);
        });
    }, 0)
}

create_chart('http://127.0.0.1:5000/api/activity/request_data/request_stats', 'doughnut', 'request_stats', 'Colab Stats');
create_chart('http://127.0.0.1:5000/api/activity/request_data/active_camps', 'doughnut', 'active_camps', 'Active Campaigns');
create_chart('http://127.0.0.1:5000/api/activity/request_data/active_users', 'doughnut', 'active_users', 'Active Users');
create_chart('http://127.0.0.1:5000/api/activity/request_data/active_posts', 'doughnut', 'active_posts', 'Active Posts');
