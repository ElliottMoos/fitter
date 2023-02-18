var ctx = document.getElementById("fittings-by-fitter");

(async function () {
    const response = await fetch("/api/reports/fittings-by-fitter");
    const data = await response.json();

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: Object.keys(data),
            datasets: [
                {
                    label: "Fitter",
                    data: Object.values(data),
                },
            ],
        },
    });
})();
