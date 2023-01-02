let rawText = document.getElementById("rawData").innerText;
let station = JSON.parse(rawText);
console.log(station)

station.foreach(train => {
    let img = document.createElement('img');
    img.src = `../static/svg/${train.Line}`;
    img.width = 16;
    let imgCol = document.createElement('td');
    imgCol.append(img);

    let destCol = document.createElement('td');
    destCol.innerText = train.Destination;
    
    let unit = document.createElement('span');
    unit.className = 'unit';
    unit.innerText = "MIN"; //TODO: Add functionality
    let timeText = document.createTextNode(`${train.Min}\u00A0`);
    let timeCol = document.createElement('td');
    timeCol.append(timeText);
    timeCol.append(unit);

    let carsCol = document.createElement('td');
    carsCol.innerText = train.Car;
    
    let occuCol = document.createElement('td');
    occuCol.innerText = train.Oc;

    let trainRow = document.createElement('tr')
    trainRow.append(imgCol)
    trainRow.append(destCol)
    trainRow.append(timeCol)
    trainRow.append(carsCol)
    trainRow.append(occuCol)

    // Comment out this line if something breaks
    document.getElementById('trains').append(trainRow);

});
