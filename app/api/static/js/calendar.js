var script = document.getElementById("calendar-script");
var activeFitterId = script.getAttribute("data-active-fitter-id");
var activeFitterRole = script.getAttribute("data-active-fitter-role");

function previousWeek() {
    appointmentCalendar.startDate = appointmentCalendar.startDate.addDays(-7);
    appointmentCalendar.update()
    appointmentCalendar.events.load("/api/fittings")
}

function nextWeek() {
    appointmentCalendar.startDate = appointmentCalendar.startDate.addDays(7);
    appointmentCalendar.update()
    appointmentCalendar.events.load("/api/fittings")
}

async function getCustomers() {
    var customers = await DayPilot.Http.get("/api/customers");
    var customerResources = customers.data.map( function (customer) {
        return {name: `${customer.first_name} ${customer.last_name}`, id: customer.id}
    });

    return [customers, customerResources];
}

async function getStores() {
    var stores = await DayPilot.Http.get("/api/stores");
    var storeResources = stores.data.map(function (store) {
        return {name: store.name, id: store.id};
    });

    return [stores, storeResources];
}

async function getFitters() {
    var fitters = await DayPilot.Http.get("/api/fitters");
    var fitterResources = fitters.data.map(function (fitter) {
        return {name: `${fitter.first_name} ${fitter.last_name}`, id: fitter.id}
    });

    return [fitters, fitterResources];
}

async function getFittings() {
    result = await DayPilot.Http.get("/api/fittings");
    return result.data;
}

function fittingOverlaps(newStart, newEnd, start, end) {
    return (
        (newStart >= start && newStart < end)
        ||
        (newStart < start && newEnd > start)
    );
}

var appointmentCalendar = new DayPilot.Calendar("appointments", {
    viewType: "Week",
    eventMoveHandling: "JavaScript",
    eventClickHandling: "JavaScript",
    eventResizeHandling: "JavaScript",
    eventDeleteHandling: "Update"
});

appointmentCalendar.onEventClick = async function (args) {
    if (activeFitterId != args.e.data.fitter_id && activeFitterRole != "Lead") {
        args.preventDefault();
        return;
    }

    var [customers, customerResources] = await getCustomers();
    var [stores, storeResources] = await getStores();
    var [fitters, fitterResources] = await getFitters();

    var form = [
        {name: "Description", id: "text"},
        {name: "Customer", id: "customer_id", options: customerResources},
        {name: "Store", id: "store_id", options: storeResources},
        {name: "Fitter", id: "fitter_id", options: fitterResources}
    ];
    var modal = await DayPilot.Modal.form(form, args.e.data);
    if (modal.canceled) return;

    var barColor = fitters.data.filter(function (value) {
        return value.id == modal.result.fitter_id;
    })[0].calendar_color;

    var data = {
        text: modal.result.text,
        barColor: barColor,
        customer_id: modal.result.customer_id,
        store_id: modal.result.store_id,
        fitter_id: modal.result.fitter_id
    };
    var fittingId = args.e.data.id
    result = await DayPilot.Http.put(`/api/fittings/${fittingId}`, data)
    appointmentCalendar.events.load("/api/fittings")
};

appointmentCalendar.onEventMove = async function (args) {
    if (activeFitterId != args.e.data.fitter_id && activeFitterRole != "Lead") {
        args.preventDefault();
        return;
    };
    var fittingId = args.e.data.id;
    var newStart = args.newStart.value;
    var newEnd = args.newEnd.value;
    var data = {start: newStart, end: newEnd};

    var fittings = await getFittings();
    var overlappingFittings = fittings.filter(function (fitting) {
        if (
            args.e.data.fitter_id != fitting.fitter_id
            ||
            args.e.data.id == fitting.id
        ) {
            return false;
        }
        let start = new DayPilot.Date(fitting.start);
        let end = new DayPilot.Date(fitting.end);
        return fittingOverlaps(args.newStart, args.newEnd, start, end);
    });
    if (overlappingFittings.length > 0) {
        args.preventDefault();
        return;
    };

    result = await DayPilot.Http.put(`/api/fittings/${fittingId}`, data);
    appointmentCalendar.events.load("/api/fittings");
};

appointmentCalendar.onEventResize = async function (args) {
    if (activeFitterId != args.e.data.fitter_id && activeFitterRole != "Lead") {
        args.preventDefault();
        return;
    }
    var fittingId = args.e.data.id
    var newStart = args.newStart.value
    var newEnd = args.newEnd.value
    var data = {start: newStart, end: newEnd}

    var fittings = await getFittings();
    var overlappingFittings = fittings.filter(function (fitting) {
        if (
            args.e.data.fitter_id != fitting.fitter_id
            ||
            args.e.data.id == fitting.id
        ) {
            return false;
        }
        let start = new DayPilot.Date(fitting.start);
        let end = new DayPilot.Date(fitting.end);
        return fittingOverlaps(args.newStart, args.newEnd, start, end);
    });
    console.log(overlappingFittings);
    if (overlappingFittings.length > 0) {
        args.preventDefault();
        return;
    };

    result = await DayPilot.Http.put(`/api/fittings/${fittingId}`, data)
    appointmentCalendar.events.load("/api/fittings")
};

appointmentCalendar.onEventDelete = async function (args) {
    if (activeFitterId != args.e.data.fitter_id && activeFitterRole != "Lead") {
        args.preventDefault();
        return;
    }
    var fittingId = args.e.data.id
    result = await DayPilot.Http.delete(`/api/fittings/${fittingId}`)
    appointmentCalendar.events.load("/api/fittings")
};

appointmentCalendar.onTimeRangeSelect = async function (args) {
    var [customers, customerResources] = await getCustomers();
    var [stores, storeResources] = await getStores();
    var [fitters, fitterResources] = await getFitters();
    var fittings = await getFittings();

    var form = [
        {name: "Description", id: "text"},
        {name: "Customer", id: "customer_id", options: customerResources},
        {name: "Store", id: "store_id", options: storeResources},
        {name: "Fitter", id: "fitter_id", options: fitterResources}
    ];
    var modal = await DayPilot.Modal.form(form);
    if (modal.canceled) return;

    var barColor = fitters.data.filter(function (value) {
        return value.id == modal.result.fitter_id;
    })[0].calendar_color;

    var data = {
        start: args.start.value,
        end: args.end.value,
        text: modal.result.text,
        barColor: barColor,
        customer_id: modal.result.customer_id,
        store_id: modal.result.store_id,
        fitter_id: modal.result.fitter_id
    };

    var overlappingFittings = fittings.filter(function (fitting) {
        let start = new DayPilot.Date(fitting.start);
        let end = new DayPilot.Date(fitting.end);
        return fittingOverlaps(args.start, args.end, start, end);
    });
    if (overlappingFittings.length > 0) {
        args.preventDefault();
        return;
    };
    
    result = await DayPilot.Http.post("/api/fittings", data)
    appointmentCalendar.events.load("/api/fittings")
};

appointmentCalendar.init();
appointmentCalendar.events.load("/api/fittings");