var ctx = document.getElementById("fittings-today");
var today = new Date().toISOString().substring(0, 10);

(async function () {
    const response = await fetch(`/api/reports/fittings-today?today=${today}`);
    const data = await response.json();

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: Object.keys(data),
            datasets: [
                {
                    label: today,
                    data: Object.values(data),
                },
            ],
        },
    });
})();
