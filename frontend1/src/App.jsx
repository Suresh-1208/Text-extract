import React, { useState } from 'react';
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [loading, setLoading] = useState(false);

  const handleImageChange = (event) => {
    setImage(event.target.files[0]);
    setExtractedText('');
  };

  const handleExtractText = async () => {
    if (!image) {
      alert('Please select an image first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', image);

    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/extract_text', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setExtractedText(data.extracted_text || 'No text found.');
      } else {
        setExtractedText('Failed to extract text.');
      }
    } catch (error) {
      setExtractedText(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Image Text Extractor</h1>
      <input type="file" accept="image/*" onChange={handleImageChange} />
      <button onClick={handleExtractText} disabled={loading}>
        {loading ? 'Extracting...' : 'Extract Text'}
      </button>
      <div id="result">
        <h3>Extracted Text:</h3>
        <pre>{extractedText}</pre>
      </div>
    </div>
  );
}

export default App;
