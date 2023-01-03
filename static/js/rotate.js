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

    // Render only one row per group    
    console.log(addedGroups);
    if (addedGroups.includes(station.TRAINS[train].Group)) {
      continue;
    }
    addedGroups.push(station.TRAINS[train].Group);
  
    let img = document.createElement('img');
    img.src = `../static/svg/${station.TRAINS[train].Line}.svg`;
    img.width = 16;
    let imgCol = document.createElement('td');
    imgCol.append(img);

    let destCol = document.createElement('td');
    destCol.innerText = station.TRAINS[train].Destination;
    
    let unit = document.createElement('span');
    unit.className = 'unit';
    unit.innerText = typeof station.TRAINS[train].Min === 'number' ? "MIN" : ""; //TODO: Add functionality
    let timeText = document.createTextNode(`${station.TRAINS[train].Min}\u00A0`);
    let timeCol = document.createElement('td');
    timeCol.className = station.TRAINS[train].Min;
    timeCol.append(timeText);
    timeCol.append(unit);

    let carsCol = document.createElement('td');
    carsCol.innerText = station.TRAINS[train].Car;
    
    let occuCol = document.createElement('td');
    occuCol.innerText = occupancyStr[station.TRAINS[train].Oc];

    let trainRow = document.createElement('tr');
    trainRow.append(imgCol);
    trainRow.append(destCol);
    trainRow.append(timeCol);
    trainRow.append(carsCol);
    trainRow.append(occuCol);

    // Comment out this line if something breaks
    document.getElementById('trains').append(trainRow);

}
