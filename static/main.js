$.ajax({
    type: 'POST',
    url: '/play',
    data: {guess: guess, attempts: attempts},
    dataType: 'json',
    success: function (response) {
        // Handle the response here
    },
    error: function (error) {
        // Handle errors here
    }
});
