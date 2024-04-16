document.addEventListener("DOMContentLoaded", function() {
    // Get references to HTML elements
    var tagSelect = document.getElementById("tag-select");
    var getRandomRecipeBtn = document.getElementById("get-random-recipe-btn");
    var randomRecipeNameDisplay = document.getElementById("randomRecipeName");
    var randomRecipeDisplay = document.getElementById("randomRecipe")
    var randomRecipeLinkDisplay = document.getElementById("randomRecipeLink")

    // Event listener for the button click
    getRandomRecipeBtn.addEventListener("click", function() {
        // Get the selected tag
        var selectedTag = tagSelect.value;
        
        // Send a request to the server to fetch a random note associated with the selected tag
        fetch("/random-recipe?tag=" + selectedTag)
            .then(response => response.json())
            .then(data => {
                // Display the random note
                randomRecipeNameDisplay.textContent = data.note;
                randomRecipeDisplay.textContent = data.recipe;
                randomRecipeLinkDisplay.href = data.link
                randomRecipeLinkDisplay.textContent = data.link
            })
            .catch(error => console.error('Error:', error));
    });
});

document.addEventListener("DOMContentLoaded", function() {
    var getRandomRecipeBtn = document.getElementById("get-random-recipe-btn");
    var randomRecipeSection = document.getElementById("randomRecipeSection");
    var tagSelect = document.getElementById("tag-select");

    getRandomRecipeBtn.addEventListener("click", function() {
            if (tagSelect.value !== "nothing") {
                randomRecipeSection.style.display = "block";
            }
    });
});
