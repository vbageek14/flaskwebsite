function toggleAllRecipes() {
    const recipeSections = document.querySelectorAll('.collapse');
    const firstSection = recipeSections[0];
    const isCollapsed = firstSection.classList.contains('show');
    
    recipeSections.forEach((section) => {
        if (isCollapsed) {
            section.classList.remove('show');
        } else {
            section.classList.add('show');
        }
    });
}


// Add an event listener to the "Toggle All Recipes" button
const toggleButton = document.querySelector('.btn.btn-outline-primary');
toggleButton.addEventListener('click', toggleAllRecipes);