document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('uploadForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from submitting normally
        
        // Get the form data
        const formData = new FormData();
        const fileInput = document.getElementById('fileInput');
        formData.append('file', fileInput.files[0]);
        
        // Submit the form data using fetch
        fetch('http://localhost:3000/imageapi', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            // Convert the blob to a URL
            const imageUrl = URL.createObjectURL(blob);
            
            // Display the uploaded image
            const uploadedImage = document.getElementById('uploadedImage');
            uploadedImage.src = imageUrl;
        })
        .catch(error => {
            console.error('Error uploading image:', error);
        });
    });
});
