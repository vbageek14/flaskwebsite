document.addEventListener("DOMContentLoaded", function() {
    // Get references to HTML elements
    var tagSelect = document.getElementById("tag-select");
    var getRandomNoteBtn = document.getElementById("get-random-note-btn");
    var randomNoteDisplay = document.getElementById("randomNote");
    var randomNoteRecipeDisplay = document.getElementById("randomNoteRecipe")
    var randomNoteRecipeLinkDisplay = document.getElementById("randomNoteRecipeLink")

    // Event listener for the button click
    getRandomNoteBtn.addEventListener("click", function() {
        // Get the selected tag
        var selectedTag = tagSelect.value;
        
        // Send a request to the server to fetch a random note associated with the selected tag
        fetch("/random-note?tag=" + selectedTag)
            .then(response => response.json())
            .then(data => {
                // Display the random note
                randomNoteDisplay.textContent = data.note;
                randomNoteRecipeDisplay.textContent = data.recipe;
                randomNoteRecipeLinkDisplay.href = data.link
                randomNoteRecipeLinkDisplay.textContent = data.link
            })
            .catch(error => console.error('Error:', error));
    });
});
