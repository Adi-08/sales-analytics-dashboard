const chartPalette = ["#16645a", "#d7804b", "#4f7890", "#d2ad54", "#829b79"];
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { labels: { color: "#45524f", usePointStyle: true, padding: 18 } }
    }
};

function createBarChart(canvasId, labels, values, label, horizontal = false) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    new Chart(canvas, {
        type: "bar",
        data: {
            labels,
            datasets: [{
                label,
                data: values,
                backgroundColor: horizontal ? chartPalette : "#247d70",
                borderRadius: 4,
                maxBarThickness: 42
            }]
        },
        options: {
            ...chartOptions,
            indexAxis: horizontal ? "y" : "x",
            plugins: { ...chartOptions.plugins, legend: { display: false } },
            scales: {
                x: { grid: { display: horizontal, color: "#e9eeeb" }, ticks: { color: "#687570" } },
                y: { beginAtZero: true, grid: { color: "#e9eeeb" }, ticks: { color: "#687570" } }
            }
        }
    });
}

function createCategoryChart() {
    const canvas = document.getElementById("categoryRevenueChart");
    if (!canvas) return;

    new Chart(canvas, {
        type: "doughnut",
        data: {
            labels: window.dashboardCharts.categories.labels,
            datasets: [{
                data: window.dashboardCharts.categories.values,
                backgroundColor: chartPalette,
                borderColor: "#ffffff",
                borderWidth: 3
            }]
        },
        options: { ...chartOptions, cutout: "62%" }
    });
}

if (window.dashboardCharts) {
    createBarChart(
        "monthlyRevenueChart",
        window.dashboardCharts.monthly.labels,
        window.dashboardCharts.monthly.values,
        "Revenue"
    );
    createCategoryChart();
    createBarChart(
        "topProductsChart",
        window.dashboardCharts.products.labels,
        window.dashboardCharts.products.values,
        "Revenue",
        true
    );
}
