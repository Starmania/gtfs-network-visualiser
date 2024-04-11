var socket = io(),
    selector = $(".selectpicker");


socket.on('connect', function () {
    console.log('Connected to the server');
});

socket.on('disconnect', function () {
    // Reload the page if the server disconnects
    setTimeout(() => {
        location.reload();
    }, 850);
});

socket.on('fetchRoutes', function (data) {
    // debugger;
    console.log(data);

    selector.empty();
    selector.prop('disabled', false);
    selector.attr('data-none-selected-text', 'Select a route...');
    selector.selectpicker('render');

    $.each(data, function (index, value) {
        // Strip name to 24 characters
        let raw_name = JSON.parse(value["route_long_name"]);
        let short_name = raw_name.length > 20 ? raw_name.substring(0, 20) + "..." : raw_name;

        let is_special = value["route_id"][0] === "T"

        // Create a fancy badge for the route_id
        var fancy_id = document.createElement("span");
        fancy_id.classList.add("badge");
        fancy_id.style.backgroundColor = value["route_color"];
        // Inverse black/white text color if background is too dark
        if (relativeLuminance(value["route_color"]) < 0.5) {
            fancy_id.style.color = "white";
        }
        fancy_id.innerText = value["route_id"];

        let option = new Option(value["route_id"] + ' - ' + short_name, short_name, is_special, is_special);
        // Add data-tokens
        option.setAttribute("data-tokens", value["route_long_name"]);
        option.setAttribute("title", value["route_id"]);
        option.setAttribute("data-content", fancy_id.outerHTML + " - " + short_name);
        selector.append(option);
    });
    selector.selectpicker('refresh');
});

// On document ready
socket.on('connect', (() => { socket.emit("fetch", { "type": "routes" }) }));
