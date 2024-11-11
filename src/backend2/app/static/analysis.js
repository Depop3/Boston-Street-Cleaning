document.addEventListener('DOMContentLoaded', function() {
    // Fetch analysis data
    fetch('/api/analysis-data')
        .then(response => response.json())
        .then(data => {
            // Create District Chart
            const districtCtx = document.getElementById('districtChart').getContext('2d');
            new Chart(districtCtx, {
                type: 'bar',
                data: {
                    labels: data.districts.map(d => d.name),
                    datasets: [{
                        label: 'Number of Streets',
                        data: data.districts.map(d => d.count),
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Create Schedule Chart
            const scheduleCtx = document.getElementById('scheduleChart').getContext('2d');
            new Chart(scheduleCtx, {
                type: 'pie',
                data: {
                    labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5'],
                    datasets: [{
                        data: data.schedule_distribution,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.5)',
                            'rgba(54, 162, 235, 0.5)',
                            'rgba(255, 206, 86, 0.5)',
                            'rgba(75, 192, 192, 0.5)',
                            'rgba(153, 102, 255, 0.5)'
                        ]
                    }]
                },
                options: {
                    responsive: true
                }
            });
        })
        .catch(error => {
            console.error('Error fetching analysis data:', error);
        });
});