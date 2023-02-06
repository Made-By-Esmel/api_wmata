let sourceUrlRoot = "api.dumbsheep123.repl.co";

function updateJSONAndDump() {

    let station_code = document.getElementById("stationId").innerText;
    
    let xhr = new XMLHttpRequest();
    xhr.open('GET', `https://${sourceUrlRoot}/backend/station/${station_code}`);
    xhr.send();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            // console.log(xhr.responseText);
            document.getElementById("rawData").innerText = xhr.responseText;
            renderJSON();
        } else {
            console.log("Something Went Wrong");
            // sourceUrlRoot = 'api.esmel.xyz';
        }
    }
}

function renderJSON() {
    let rawText = document.getElementById("rawData").innerText;
    let station = JSON.parse(rawText);
    // console.log(station)

    let addedGroups = [0];

    const occupancyStr = [
        "No Data",
        "Not Crowded",
        "Somewhat Crowded",
        "Full"
    ];

    for (train in station.TRAINS) {
        let train_data = station.TRAINS[train];
        // Render only one row per group    
        // console.log(addedGroups);
        if (addedGroups.includes(train_data.Group)) {
        continue;
        }
        addedGroups.push(train_data.Group);
    
        let img = document.createElement('img');
        img.src = `https://pub-e0e86bcdb20a447ea11d8706a676342f.r2.dev/${train_data.Line}.svg`;
        img.width = 25; // Originally 16
        let imgCol = document.createElement('td');
        imgCol.append(img);

        let destCol = document.createElement('td');
        destCol.innerText = train_data.Destination;
        
        let unit = document.createElement('span');
        unit.className = 'unit';
        unit.innerText = typeof train_data.Min === 'number' ? "MIN" : ""; //TODO: Add functionality
        let timeText = document.createTextNode(`${train_data.Min}\u00A0`);
        let timeCol = document.createElement('td');
        timeCol.className = train_data.Min;
        timeCol.append(timeText);
        timeCol.append(unit);

        let carsCol = document.createElement('td');
        carsCol.innerText = train_data.Car;
        
        let occuCol = document.createElement('td');
        occuCol.innerText = occupancyStr[train_data.Oc];
        // let pg = document.createElement('progress')
        // pg.max = 2;
        // pg.value = train_data.Oc - 1 < 0 ? 0 : train_data.Oc - 1;
        // pg.className = `pg-${train_data.Oc}`;
        // occuCol.append(pg);

        let trainRow = document.createElement('tr');
        trainRow.id = `train-${train}`;
        trainRow.append(imgCol);
        trainRow.append(destCol);
        trainRow.append(timeCol);
        trainRow.append(carsCol);
        trainRow.append(occuCol);

        if (document.getElementById(`train-${train}`)) {
            // Comment out this line if something breaks
            document.getElementById(`train-${train}`).replaceWith(trainRow);
        } else {
            document.getElementById('trains').append(trainRow);
        }

        // window.navigator.vibrate(50);
    }
}

renderJSON();

setInterval(
    function() {
        updateJSONAndDump();
        
    }, 5 * 1000
);