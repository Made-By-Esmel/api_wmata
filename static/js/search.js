// Used in search.html

window.onload = function () {
const input = document.getElementById("search-input");
  
var suggestionsContainer = document.querySelector(".suggestions-bar");
// var form = document.getElementById("se");

input.addEventListener("input", async (event) => {
    const value = event.target.value;

    if (value === "") {
        suggestionsContainer.style.display = "none";
        return;
    }

    var response = await fetch("https://api.dumbsheep123.repl.co/suggestions.json");
    var suggestionsData = await response.json();

    var suggestions = suggestionsData.filter(function (suggestion) {
        return suggestion.includes(value);
    });

    suggestionsContainer.innerHTML = "";

    if (suggestions.length === 0) {
        suggestionsContainer.style.display = "none";
        return;
    }

    suggestionsContainer.style.display = "block";
    suggestionsContainer.style.userSelect = "none";
    suggestionsContainer.style.cursor = "pointer";
    suggestionsContainer.style.width = '50%';
    suggestionsContainer.style.height = '200px';
    suggestionsContainer.style.backgroundColor = 'lightgray';
    suggestionsContainer.style.borderRadius = '5px';
    suggestionsContainer.style.overflowY = 'auto';
    suggestionsContainer.style.marginTop = '10px';
    suggestionsContainer.style.fontFamily = 'Poppins';
    for (let i = 0; i < Math.min(suggestions.length, 5); i++) {
        var suggestion = suggestions[i];
        var suggestionElement = document.createElement("div");
        suggestionElement.textContent = suggestion;
        suggestionsContainer.appendChild(suggestionElement);

        // Add a click event listener to the suggestion element
        suggestionElement.addEventListener("click", () => {
            input.value = suggestion;
            suggestionsContainer.style.display = "none";
        });
    }
});

form.addEventListener("submit", (event) => {
    event.preventDefault();
    var value = input.value;
    window.location.href = '/station/' + value;
  });
}