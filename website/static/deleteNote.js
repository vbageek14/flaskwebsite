function deleteNote(noteId) {
    // Ask for confirmation
    var confirmation = confirm("Are you sure you want to delete this recipe?");

    // If user confirms, proceed with deletion
    if (confirmation) {
        fetch("/delete-recipe", {
            method: "POST",
            body: JSON.stringify({ noteId: noteId, confirmation: "yes" }),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('meta[name="csrf-token"]').getAttribute('content')
            },
        })
            .then((_res) => {
                // Handle success or reload the page
                window.location.reload();
            })
            .catch((error) => console.error("Error:", error));
    } else {
        // If user cancels, do nothing
        console.log("Deletion canceled");
    }
}
