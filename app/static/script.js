$(document).ready(function() {
  // Handle form submission
  $('#form').submit(function(event) {
    event.preventDefault();

    // Get the user's preferences
    const title = $('#title').val();

    // Send a POST request to the Flask backend
    $.ajax({
      type: 'POST',
      url: '/app/recommend',
      data: JSON.stringify({ name: title }),
      contentType: 'application/json',
      success: function(response) {
        // Clear the previous recommendations
        $('#recommendations').empty();

        // Iterate through the list of recommended movies
        for (const movie of response) {
          // Create a list item for the movie
          const item = $('<li>').text(movie.name);

          // Add the list item to the recommendations list
          $('#recommendations').append(item);
        }
      }
    });
  });
});
