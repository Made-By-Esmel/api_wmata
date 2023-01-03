let rawText = document.getElementById("rawData").innerText;
let station = JSON.parse(rawText);
console.log(station)

let addedGroups = [0];

const occupancyStr = [
  "Empty",
  "Busy",
  "Full"
]

for (train in station.TRAINS) {
    let train_data = station.TRAINS[train];
    // Render only one row per group    
    console.log(addedGroups);
    if (addedGroups.includes(train_data.Group)) {
      continue;
    }
    addedGroups.push(train_data.Group);
  
    let img = document.createElement('img');
    img.src = `../static/svg/${train_data.Line}.svg`;
    img.width = 16;
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

    let trainRow = document.createElement('tr');
    trainRow.append(imgCol);
    trainRow.append(destCol);
    trainRow.append(timeCol);
    trainRow.append(carsCol);
    trainRow.append(occuCol);

    // Comment out this line if something breaks
    document.getElementById('trains').append(trainRow);

}
