import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Uploader.css';

const Uploader = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [processedImageUrl, setProcessedImageUrl] = useState(null);
  const [injuryLabel, setInjuryLabel] = useState(null);


  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    if (selectedFile) {
      const formData = new FormData();
      formData.append('file', selectedFile);

      try {
        const response = await axios.post('http://127.0.0.1:3002/injured_image', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });

        const processedImageUrl = response.data.saved_image_path;
        setProcessedImageUrl(processedImageUrl);
        setSelectedFile(null);
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };

  const fetchProcessedImage = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:3002/injured', {
        responseType: 'arraybuffer',
      });

      const blob = new Blob([response.data], { type: 'image/jpeg' });
      const imageUrl = URL.createObjectURL(blob);

      const imgElement = document.createElement('img');
      imgElement.src = imageUrl;
      imgElement.alt = 'Processed Image';
      imgElement.className = 'processed-image';

      const container = document.getElementById('imageContainer');
      container.innerHTML = '';
      container.appendChild(imgElement);
    } catch (error) {
      console.error('Error fetching processed image:', error);
    }
  };

  const fetchInjuredContent = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:3002/label');
      const injuryLabel = response.data;

      setInjuryLabel(injuryLabel);
    } catch (error) {
      console.error('Error fetching injured content:', error);
    }
  };

  return (
    <div className="uploader-container">
      <h2>Injury Classification</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="fileInput">Select a file:</label>
          <input
            type="file"
            className="form-control-file"
            id="fileInput"
            onChange={handleFileChange}
            accept=".jpg, .jpeg, .png"
            required
          />
        </div>
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </form>

      <button onClick={fetchProcessedImage} className="btn btn-primary mt-3">
        Fetch Processed Image
      </button>

      <div id="imageContainer" className="processed-image-container mt-3"></div>
      {injuryLabel && (
        <div className="injury-label-container mt-3">
          <h3>Injury Label</h3>
          <p>{injuryLabel}</p>
        </div>
      )}

      <button onClick={fetchInjuredContent} className="btn btn-primary mt-3">
        Fetch Injured Content
      </button>
    </div>
  );
};

export default Uploader;
