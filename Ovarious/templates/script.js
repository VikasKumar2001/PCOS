document.getElementById("prediction-form").addEventListener("submit", function(event) {
    // Prevent the form from submitting normally
    event.preventDefault();
  
    // Show the prediction text
    document.getElementById("prediction-text").classList.remove("hidden");
  });
  