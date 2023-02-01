// Used in search.html
window.onload = function () {
const input = document.getElementById("search-input");
if (!input) {
    console.error("The input element could not be found");
    return;
}
var suggestionsContainer = document.querySelector(".suggestions");
var form = document.getElementById("search-form");

input.addEventListener("input", async (event) => {
    const value = event.target.value;

    if (value === "") {
        suggestionsContainer.style.display = "none";
        return;
    }

    var response = await fetch("https://pub-e0e86bcdb20a447ea11d8706a676342f.r2.dev/suggestions.json");
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
    for (let i = 0; i < Math.min(suggestions.length, 5); i++) {
        var suggestion = suggestions[i];
        var suggestionElement = document.createElement("div");
        suggestionElement.textContent = suggestion;
        suggestionsContainer.appendChild(suggestionElement);

        // Add a click event listener to the suggestion element
        suggestionElement.addEventListener("click", () => {
            input.value = suggestion;
            suggestionsContainer.style.display = "none";
            form.submit();
        });
    }
});

form.addEventListener("submit", (event) => {
    event.preventDefault();
    var value = input.value;
    window.location.href = '/station/' + value;
  });
}