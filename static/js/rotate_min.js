let rawText=document.getElementById("rawData").innerText,station=JSON.parse(rawText);console.log(station);let addedGroups=[0];const occupancyStr=["Empty","Busy","Full"];for(train in station.TRAINS){if(console.log(addedGroups),addedGroups.includes(station.TRAINS[train].Group))continue;addedGroups.push(station.TRAINS[train].Group);let c=document.createElement('img');c.src=`../static/svg/${station.TRAINS[train].Line}.svg`,c.width=16;let e=document.createElement('td');e.append(c);let h=document.createElement('td');h.innerText=station.TRAINS[train].Destination;let d=document.createElement('span');d.className='unit',d.innerText=typeof station.TRAINS[train].Min=='number'?"MIN":"";let i=document.createTextNode(`${station.TRAINS[train].Min}\u00A0`),b=document.createElement('td');b.className=station.TRAINS[train].Min,b.append(i),b.append(d);let f=document.createElement('td');f.innerText=station.TRAINS[train].Car;let g=document.createElement('td');g.innerText=occupancyStr[station.TRAINS[train].Oc];let a=document.createElement('tr');a.append(e),a.append(h),a.append(b),a.append(f),a.append(g),document.getElementById('trains').append(a)}