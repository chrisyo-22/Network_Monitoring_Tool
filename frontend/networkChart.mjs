document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('realtimeChart').getContext('2d');
    const chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',

        // The data for our dataset
        data: {
            datasets: [{
                label: 'Network Activity',
                backgroundColor: 'rgba(0, 255, 0, 0.5)', // semi-transparent green
                borderColor: 'rgb(0, 255, 0)',
                data: [] // Placeholder for data points
            }]
        },

        // Configuration options
        options: {
            scales: {
                x: {
                    type: 'realtime',
                    realtime: {
                        duration: 20000,
                        refresh: 1000,
                        delay: 2000,
                        onRefresh: function (chart) {
                            chart.data.datasets.forEach(function (dataset) {
                                dataset.data.push({
                                    x: Date.now(),
                                    y: Math.random() * 100 // Random data, replace with actual data
                                });
                            });
                        }
                    }
                },
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    display: true
                }
            }
        }
    });
});
