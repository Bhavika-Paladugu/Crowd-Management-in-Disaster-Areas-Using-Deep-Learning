// import React, { useState, useEffect } from 'react';
import { Container, TextField, Button } from '@mui/material';


// const ImageUploader = () => {
//   const [image, setImage] = useState(null);

//   const handleImageChange = (e) => {
//     const file = e.target.files[0];
//     setImage(file);
//   };

//   const handleUpload = () => {
//     // You can implement your upload logic here, for example, using fetch to send the image to your server
//     // Don't forget to handle the image file in your server-side code
//     console.log('Uploading image:', image);
//   };

//   return (
//     <Container maxWidth="sm">
//       <TextField
//         type="file"
//         onChange={handleImageChange}
//         variant="outlined"
//         fullWidth
//         InputLabelProps={{ shrink: true }}
//       />
//       <Button
//         variant="contained"
//         color="primary"
//         onClick={handleUpload}
//         disabled={!image}
//         style={{ marginTop: '1rem' }}
//       >
//         Upload Image
//       </Button>
//     </Container>
//   );
// };

// export default ImageUploader;


import React, { useState } from 'react';
// import { Button, Container, TextField } from '@material-ui/core';

const ImageUploader = () => {
  const [image, setImage] = useState(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
  };

  const handleUpload = () => {
    if (!image) return; // No image selected, do nothing

    // Create FormData object to send the image data
    const formData = new FormData();
    formData.append('file', image);

    // Make a POST request to the API endpoint
    fetch('http://localhost:3000/imageapi', {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to upload image');
      }
      return response.json();
    })
    .then(data => {
      console.log('Image uploaded successfully:', data);
      // Handle response from the API if needed
    })
    .catch(error => {
      console.error('Error uploading image:', error);
      // Handle error
    });
  };

  return (
    <Container maxWidth="sm">
      <TextField
        type="file"
        onChange={handleImageChange}
        variant="outlined"
        fullWidth
        InputLabelProps={{ shrink: true }}
      />
      <Button
        variant="contained"
        color="primary"
        onClick={handleUpload}
        disabled={!image}
        style={{ marginTop: '1rem' }}
      >
        Upload Image
      </Button>
    </Container>
  );
};

export default ImageUploader;
