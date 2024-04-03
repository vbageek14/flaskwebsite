function toggleRecipe(noteId) {
    var recipeDiv = document.getElementById("recipe_" + noteId);
    if (recipeDiv.style.display === "none") {
        recipeDiv.style.display = "block";
    } else {
        recipeDiv.style.display = "none";
    }
}
