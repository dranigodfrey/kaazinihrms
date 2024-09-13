 $(document).ready(function() {
            $.ajax({
                url: "{% url 'employee_title_data' %}", // URL of the view returning JSON data
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    const ctx = document.getElementById('employeeTitleChart').getContext('2d');
                    const employeeTitleChart = new Chart(ctx, {
                        type: 'bar',
                        data: {
                            labels: data.titles,
                            datasets: [{
                                label: 'Number of Employees',
                                data: data.counts,
                                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                                borderColor: 'rgba(54, 162, 235, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            indexAxis: 'y', // This option configures the chart to be horizontal
                            scales: {
                                x: {
                                    beginAtZero: true
                                }
                            },
                            plugins: {
                                legend: {
                                    display: false
                                },
                                title: {
                                    display: true,
                                    text: 'Number of Employees by Title'
                                }
                            }
                        }
                    });
                },
                error: function(error) {
                    console.error("Error fetching data:", error);
                }
            });
        });
 