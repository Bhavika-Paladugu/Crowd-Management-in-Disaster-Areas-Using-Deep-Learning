import React, { useState, useEffect } from 'react';
import './Uploader.css';

const Uploader = () => {
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState('');
    const [processedImageVisible, setProcessedImageVisible] = useState(false);
    const [filePreview, setFilePreview] = useState(null);
    const [countOfPeople, setCountOfPeople] = useState(null);
    const [resources, setResources] = useState(null);

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
        setProcessedImageVisible(false);

        const reader = new FileReader();
        reader.onloadend = () => {
            setFilePreview(reader.result);
        };
        if (selectedFile) {
            reader.readAsDataURL(selectedFile);
        } else {
            setFilePreview(null);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!file) {
            setMessage('Please select a file');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch('http://localhost:3002/imageapi', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                setMessage('File submitted successfully');
                setProcessedImageVisible(true);
                fetchCountOfPeople();
                fetchResources();
            } else {
                setMessage('Error submitting file');
            }
        } catch (error) {
            console.error('Error submitting file:', error);
            setMessage('Error submitting file');
        }
    };

    const fetchCountOfPeople = async () => {
        try {
            const response = await fetch('http://localhost:3002/hehe');
            if (response.ok) {
                const data = await response.json();
                setCountOfPeople(data.count);
            } else {
                console.error('Failed to fetch count of people');
            }
        } catch (error) {
            console.error('Error fetching count of people:', error);
        }
    };

    const fetchResources = async () => {
        try {
            const response = await fetch('http://127.0.0.1:3002/resources_render');
            if (response.ok) {
                const data = await response.json();
                setResources(data); // Update resources state with received data
            } else {
                console.error('Failed to fetch resources allocation');
            }
        } catch (error) {
            console.error('Error fetching resources allocation:', error);
        }
    };

    const processedImagePath = 'http://localhost:3002/processed_image';

    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <h2>Victim Detection</h2>
            <form onSubmit={handleSubmit} style={{ width: '50%', maxWidth: '400px' }}>
                <div>
                    <input type="file" onChange={handleFileChange} />
                </div>
                {filePreview && (
                    <div>
                        <h3>Selected File Preview</h3>
                        <img src={filePreview} alt="Selected File Preview" style={{ width: '150%', height: '66%' }} />
                    </div>
                )}
                <div>
                    <button type="submit">Submit File</button>
                </div>
            </form>
            {message && <p>{message}</p>}
            <br />
            {processedImageVisible && (
                <div>
                    <img src={processedImagePath} style={{ marginLeft: '19%', width: '93%', height: '66%' }} alt="Processed Image" />
                    {countOfPeople !== null && <p>Count of People: {countOfPeople}</p>}
                    {resources && (
                        <div>
                            <h3>Resources Allocation</h3>
                            <ul>
                                {Object.entries(resources).map(([category, items]) => (
                                    <li key={category}>
                                        <strong>{category}</strong>
                                        <ul>
                                            {Object.entries(items).map(([itemName, quantity]) => (
                                                <li key={itemName}>
                                                    {itemName}: {quantity}
                                                </li>
                                            ))}
                                        </ul>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default Uploader;
