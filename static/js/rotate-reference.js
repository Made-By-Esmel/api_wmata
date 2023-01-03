//DO NOT USE FOR PRODUCTION


let rawDataElement = document.getElementById("rawData");
let rawText = rawDataElement.innerText;
let station = JSON.parse(rawText);
console.log(station);

let trainsElement = document.getElementById('trains');
let addedGroups = [0];

for (let train of station.TRAINS) {
  let trainData = train;
  // Render only one row per group    
  console.log(addedGroups);
  if (addedGroups.includes(trainData.Group)) {
    continue;
  }
  addedGroups.push(trainData.Group);
 
  let img = document.createElement('img');
  img.src = `../static/svg/${trainData.Line}.svg`;
  img.width = 16;
  let imgCol = document.createElement('td');
  imgCol.append(img);

  let destCol = document.createElement('td');
  let destText = document.createTextNode(trainData.Destination);
  destCol.append(destText);
 
  let unit = document.createElement('span');
  unit.className = 'unit';
  unit.innerText = typeof trainData.Min === 'number' ? "MIN" : ""; //TODO: Add functionality
  let timeText = document.createTextNode(`${trainData.Min}\u00A0`);
  let timeCol = document.createElement('td');
  timeCol.className = trainData.Min;
  timeCol.append(timeText);
  timeCol.append(unit);

  let carsCol = document.createElement('td');
  let carsText = document.createTextNode(trainData.Car);
  carsCol.append(carsText);
 
  let occuCol = document.createElement('td');
  let occuText;
  switch (trainData.Oc) {
    case 0:
      occuText = document.createTextNode("Empty");
      break;
    case 1:
      occuText = document.createTextNode("Busy");
      break;
    case 2:
      occuText = document.createTextNode("Full");
      break;