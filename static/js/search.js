import stationMap from 'https://api.dumbsheep123.repl.co/static/js/stationmap.js'

document.querySelector("form").addEventListener("submit", function (event) {
    event.preventDefault(); // prevent the form from submitting
    var dropdown = document.querySelector("#dropdown");
    var selectedOption = dropdown.options[dropdown.selectedIndex].value;
    var errorMessage = document.querySelector("#error-message");

    // validate the dropdown selection
    if (!selectedOption) {
        errorMessage.textContent = "Select an option!";
        errorMessage.style.display = "block";
        return;
    }

    if (selectedOption in stationMap) {
        window.location.href = stationMap[selectedOption];
      } else {
        alert('It would appear as though there\'s an error on our part that\'s preventing the completion of your request. Please try again later.');
      }
});