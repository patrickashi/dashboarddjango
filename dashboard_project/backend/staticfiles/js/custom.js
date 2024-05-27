document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM Loaded");

    const sidebar = document.getElementById("sidebar");
    const toggleButton = document.getElementById("toggle-button");

    // Check if sidebar and toggleButton exist
    if (sidebar && toggleButton) {
        toggleButton.addEventListener("click", function () {
            console.log("Button Clicked");
            sidebar.classList.toggle("active");
        });
    } else {
        console.error("Sidebar or toggle button not found.");
    }
});
