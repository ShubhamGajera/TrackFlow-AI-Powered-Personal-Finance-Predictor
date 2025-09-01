// Chart setup for predictions page
document.addEventListener('DOMContentLoaded', function() {
    // Get the prediction chart canvas
    const predChartCtx = document.getElementById('predChart');
    
    if (predChartCtx) {
        // Extract data from the page
        const months = JSON.parse(predChartCtx.getAttribute('data-months') || '[]');
        const totals = JSON.parse(predChartCtx.getAttribute('data-totals') || '[]');
        const prediction = parseFloat(predChartCtx.getAttribute('data-prediction') || '0');
        
        // Add prediction point
        const allMonths = [...months];
        const allTotals = [...totals];
        
        if (months.length > 0) {
            // Get next month for prediction
            const lastMonth = months[months.length - 1];
            const [year, month] = lastMonth.split('-').map(Number);
            let nextMonth = month + 1;
            let nextYear = year;
            if (nextMonth > 12) {
                nextMonth = 1;
                nextYear++;
            }
            allMonths.push(`${nextYear}-${String(nextMonth).padStart(2, '0')}`);
            allTotals.push(prediction);
        }
        
        // Create gradient
        const gradient = predChartCtx.getContext('2d').createLinearGradient(0, 0, 0, 400);
        gradient.addColorStop(0, 'rgba(99, 102, 241, 0.5)');
        gradient.addColorStop(1, 'rgba(99, 102, 241, 0)');
        
        // Create the chart
        new Chart(predChartCtx, {
            type: 'line',
            data: {
                labels: allMonths,
                datasets: [{
                    label: 'Monthly Expenses',
                    data: allTotals.slice(0, -1),
                    borderColor: '#6366f1',
                    borderWidth: 2,
                    pointBackgroundColor: '#6366f1',
                    pointRadius: 4,
                    tension: 0.4,
                    fill: true,
                    backgroundColor: gradient
                }, {
                    label: 'Predicted Expense',
                    data: Array(allTotals.length - 1).fill(null).concat(prediction),
                    borderColor: '#f43f5e',
                    borderWidth: 2,
                    pointBackgroundColor: '#f43f5e',
                    pointRadius: 6,
                    pointStyle: 'star',
                    tension: 0.4,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            color: '#94a3b8',
                            font: {
                                family: 'system-ui'
                            }
                        }
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        backgroundColor: '#1e293b',
                        titleColor: '#e2e8f0',
                        bodyColor: '#e2e8f0',
                        borderColor: '#475569',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ₹${context.parsed.y.toFixed(2)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            display: false,
                            drawBorder: false
                        },
                        ticks: {
                            color: '#94a3b8',
                            font: {
                                family: 'system-ui'
                            }
                        }
                    },
                    y: {
                        grid: {
                            color: '#334155',
                            drawBorder: false
                        },
                        ticks: {
                            color: '#94a3b8',
                            font: {
                                family: 'system-ui'
                            },
                            callback: function(value) {
                                return '₹' + value.toFixed(2);
                            }
                        }
                    }
                }
            }
        });
    }
});