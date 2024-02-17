input.addEventListener('change', function(event) {
    const file = event.target.files[0];

    if (file) {
        // Create a new FormData object and append the file to it
        const formData = new FormData();
        formData.append('file', file);

        // Send a POST request to the '/upload' endpoint with the file data
        fetch('/upload', {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                // Parse the JSON response to get the URL of the uploaded image
                response.json().then(data => {
                    const imageUrl = data.url;
                    // Set the 'src' attribute of the 'uploaded-image' img tag to the URL of the uploaded image
                    const img = document.getElementById('uploaded-image');
                    img.src = imageUrl;
                });
            } else {
                // Handle the error response
            }
        });
    } else {
        // Set the 'src' attribute of the 'uploaded-image' img tag to a placeholder image
        const img = document.getElementById('uploaded-image');
        //img.src = '';
    }
});
