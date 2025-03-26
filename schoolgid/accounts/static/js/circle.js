const all = parseInt(document.getElementById('info1').getAttribute('data-lentgh'));
document.addEventListener("DOMContentLoaded", function () { 
    for (let i = 0; i < all; i++) {
        var ctx = document.getElementById(`progressChart-${i}`).getContext('2d');
        var progress = parseFloat(document.getElementById(`progressChart-${i}`).getAttribute('data-current_value'));
        var maxValue = 5;   // Максимальное значение
        var percentage = (progress / maxValue) * 100;

        // Плагин для добавления текста в центр
        const centerTextPlugin = {
            id: 'centerText',
            afterDraw(chart) {
                const { ctx, chartArea: { width, height } } = chart;
                ctx.save();
                ctx.font = 'bold 18px Arial';
                ctx.fillStyle = 'white';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                // Используем уникальное значение progress для каждого круга
                const progress = chart.config.data.datasets[0].data[0] / 20; // Доступ к текущему прогрессу через chart
                ctx.fillText(progress.toFixed(2), width / 2, height / 2); // Отображаем прогресс
                ctx.restore();
            }
        };

        console.log(progress);
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [percentage, 100 - percentage], // Заполненная и пустая часть
                    backgroundColor: ['transparent', 'transparent'],
                    borderWidth: 2,
                    borderColor: ['#5b6d8a', 'transparent']
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    legend: { display: false },  
                    tooltip: { enabled: false }
                },
                cutout: '0%',  // Толщина круга
            },
            plugins: [centerTextPlugin] // Включаем плагин
        });    
    }
});