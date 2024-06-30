const dropArea = document.getElementById("drop-area");
const inputFile = document.getElementById("input-file");
const imageView = document.getElementById("img-view");

// Function to handle image upload
function uploadImage(file) {
    const reader = new FileReader();

    // Read the file as a data URL
    reader.readAsDataURL(file);

    // When the file is loaded
    reader.onload = function () {
        const imgLink = reader.result;
        imageView.style.backgroundImage = `url(${imgLink})`;
        imageView.textContent = "";
        imageView.style.border = "none";

        // Send the image to the server for processing
        sendImageToServer(reader.result);
    };
}

// Function to send the image to the Flask server for processing

//     //Harshil's code -->
// function sendImageToServer(imageData) {
//     // Construct the FormData object
//     const formData = new FormData();
//     formData.append('file', imageData);

//     // Send a POST request to the Flask server
//     fetch('http://127.0.0.1:3000/imageapi', {
//         method: 'POST',
//         body: formData // Use the FormData object as the request body
//     })
//     .then(response => response.text())
//     .then(processedImagePath => {
//         // Processed image received from server
//         console.log("Processed image path received from server:", processedImagePath);
//         // Update the processed image in the HTML
//         document.getElementById('processed-image').src = processedImagePath;
//     })
//     .catch(error => {
//         // Handle errors
//         console.error('Error:', error);
//     });
// }





function sendImageToServer(imageData) {
    // Construct the payload
    const image = {
        image: imageData
    };

    // Send a POST request to the Flask server
    fetch('http://127.0.0.1:3000/imageapi', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'  // Set the content type to JSON
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.text())
    .then(processedImagePath => {
        // Processed image received from server
        console.log("Processed image path received from server:", processedImagePath);
        // Update the processed image in the HTML
        document.getElementById('processed-image').src = processedImagePath;
    })
    .catch(error => {
        // Handle errors
        console.error('Error:', error);
    });
}



//Bhavika' code
// function sendImageToServer(imageData) {
//     // Construct the payload
//     const formData = new FormData();
//     formData.append('file', inputFile.files[0]);

//     // Send a POST request to the Flask server
//     fetch('http://127.0.0.1:3000/imageapi', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(payload)
//     })
//     .then(response => response.text())
//     .then(processedImagePath => {
//         // Processed image received from server
//         console.log("Processed image path received from server:", processedImagePath);
//         // Update the processed image in the HTML
//         document.getElementById('processed-image').src = processedImagePath;
//     })
//     .catch(error => {
//         // Handle errors
//         console.error('Error:', error);
//     });
// }

// Event listener for file input change
inputFile.addEventListener("change", function () {
    if (inputFile.files.length > 0) {
        uploadImage(inputFile.files[0]);
    }
});

// Event listener for dragover
dropArea.addEventListener("dragover", function (e) {
    e.preventDefault();
});

// Event listener for drop
dropArea.addEventListener("drop", function (e) {
    e.preventDefault();
    if (e.dataTransfer.files.length > 0) {
        uploadImage(e.dataTransfer.files[0]);
    }
});
