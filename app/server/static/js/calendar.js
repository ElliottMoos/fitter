var script = document.getElementById("calendar-script");
var activeFitterId = script.getAttribute("data-active-fitter-id");
var activeFitterRole = script.getAttribute("data-active-fitter-role");

// Load fittings for previous week
function previousWeek() {
    fittingCalendar.startDate = fittingCalendar.startDate.addDays(-7);
    fittingCalendar.update()
    fittingCalendar.events.load("/api/fittings")
}

// Load fittings for next week
function nextWeek() {
    fittingCalendar.startDate = fittingCalendar.startDate.addDays(7);
    fittingCalendar.update()
    fittingCalendar.events.load("/api/fittings")
}

// Build customer resource list
async function getCustomers() {
    var customers = await DayPilot.Http.get("/api/customers");
    var customerResources = customers.data.map( function (customer) {
        return {name: `${customer.first_name} ${customer.last_name}`, id: customer.id}
    });

    return [customers, customerResources];
}

// Build store resource list
async function getStores() {
    var stores = await DayPilot.Http.get("/api/stores");
    var storeResources = stores.data.map(function (store) {
        return {name: store.name, id: store.id};
    });

    return [stores, storeResources];
}

// Build fitter resource list
async function getFitters() {
    var fitters = await DayPilot.Http.get("/api/fitters");
    var fitterResources = fitters.data.map(function (fitter) {
        return {name: `${fitter.first_name} ${fitter.last_name}`, id: fitter.id}
    });

    return [fitters, fitterResources];
}

// Fetch all fittings
async function getFittings() {
    result = await DayPilot.Http.get("/api/fittings");
    return result.data;
}

/**
 * Filter resource list when active fitter
 * doesn't have permission to choose a different
 * resource
 */
function filterResourceByResourceId(resources, resourceId) {
    return resources.filter(function (resource) {
        return resource.id == resourceId;
    });
};

/**
 * Helper function for determining fitting
 * overlaps
 */
function fittingOverlaps(newStart, newEnd, start, end) {
    return (
        (newStart >= start && newStart < end)
        ||
        (newStart < start && newEnd > start)
    );
}

/**
 * Helper function for determining
 * fitter permissions
 */
function fitterHasPermissions(fitterId) {
    return (
        activeFitterRole == "Lead" // If a fitter is a Lead, they can do pretty much anything
        ||
        activeFitterId == fitterId // If a fitter is interacting with their own resource, they can edit it
    );
};

/**
 * Helper function for determining
 * if we should ignore a fitting in
 * an overlap check
 */
function fittingShouldBeIgnoredInOverlapCheck(fitting, fittingToCheck) {
    return (
        (
            // Won't double book fitter
            fitting.fitter_id != fittingToCheck.fitter_id
            &&
            // Won't double book customer
            fitting.customer_id != fittingToCheck.customer_id
        )
        ||
        /**
         * Ignore fitting being compared
         * to avoid issues with rescheduling
         * a fitting inside its own overlap
        */
        fitting.id == fittingToCheck.id
    );
};

// Initialize fitting calendar object
var fittingCalendar = new DayPilot.Calendar("fittings", {
    viewType: "Week",
    eventMoveHandling: "JavaScript",
    eventClickHandling: "JavaScript",
    eventResizeHandling: "JavaScript",
    eventDeleteHandling: "Update"
});

// Handle event edit action
fittingCalendar.onEventClick = async function (args) {

    var [customers, customerResources] = await getCustomers();
    var [stores, storeResources] = await getStores();
    var [fitters, fitterResources] = await getFitters();

    /** 
     * Build form configuration based on
     * active fitter permissions
     * */
    var form = [
        {
            name: "Description",
            id: "text",
            type: "textarea",
            disabled: !fitterHasPermissions(args.e.data.fitter_id)
        },
        {
            name: "Customer",
            id: "customer_id",
            options: fitterHasPermissions(args.e.data.fitter_id) ?
            customerResources : filterResourceByResourceId(
                customerResources,
                args.e.data.customer_id
            ),
            disabled: !fitterHasPermissions(args.e.data.fitter_id)
        },
        {
            name: "Store",
            id: "store_id",
            options: fitterHasPermissions(args.e.data.fitter_id) ?
            storeResources : filterResourceByResourceId(
                storeResources,
                args.e.data.store_id
            ),
            disabled: !fitterHasPermissions(args.e.data.fitter_id)
        },
        {
            name: "Fitter",
            id: "fitter_id",
            options: activeFitterRole == "Lead" ? 
            fitterResources : filterResourceByResourceId(
                fitterResources,
                args.e.data.fitter_id
            ),
            disabled: !fitterHasPermissions(args.e.data.fitter_id)
        }
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
    if (activeFitterId != args.e.data.fitter_id && activeFitterRole != "Lead") {
        args.preventDefault();
        return;
    }
    result = await DayPilot.Http.put(`/api/fittings/${fittingId}`, data)
    fittingCalendar.events.load("/api/fittings")
};

// Handle event schedule updates
fittingCalendar.onEventMove = async function (args) {
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
        if (fittingShouldBeIgnoredInOverlapCheck(args.e.data, fitting)) {
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
    fittingCalendar.events.load("/api/fittings");
};

fittingCalendar.onEventResize = async function (args) {
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
        if (fittingShouldBeIgnoredInOverlapCheck(args.e.data, fitting)) {
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
    fittingCalendar.events.load("/api/fittings")
};

fittingCalendar.onEventDelete = async function (args) {
    if (activeFitterId != args.e.data.fitter_id && activeFitterRole != "Lead") {
        args.preventDefault();
        return;
    }
    var fittingId = args.e.data.id
    result = await DayPilot.Http.delete(`/api/fittings/${fittingId}`)
    fittingCalendar.events.load("/api/fittings")
};

fittingCalendar.onTimeRangeSelect = async function (args) {
    fittingCalendar.clearSelection();
    var [customers, customerResources] = await getCustomers();
    var [stores, storeResources] = await getStores();
    var [fitters, fitterResources] = await getFitters();
    var fittings = await getFittings();

    var form = [
        {name: "Description", id: "text", type: "textarea"},
        {name: "Customer", id: "customer_id", options: customerResources},
        {name: "Store", id: "store_id", options: storeResources},
        {
            name: "Fitter",
            id: "fitter_id",
            options: activeFitterRole == "Lead" ?
            fitterResources : filterResourceByResourceId(
                fitterResources,
                activeFitterId
            ),
            disabled: !fitterHasPermissions(activeFitterId)
        }
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
        if (fittingShouldBeIgnoredInOverlapCheck(data, fitting)) {
            return false;
        }
        let start = new DayPilot.Date(fitting.start);
        let end = new DayPilot.Date(fitting.end);
        return fittingOverlaps(args.start, args.end, start, end);
    });
    if (overlappingFittings.length > 0) {
        args.preventDefault();
        return;
    };
    
    result = await DayPilot.Http.post("/api/fittings", data)
    fittingCalendar.events.load("/api/fittings")
};

fittingCalendar.init();
fittingCalendar.events.load("/api/fittings");