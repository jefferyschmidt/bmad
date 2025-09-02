import React, { useState } from 'react';

function Gallery() {
  const [photos] = useState([
    { id: 1, url: 'https://via.placeholder.com/300x200?text=Feet+Photo+1', caption: 'Beautiful feet photo' },
    { id: 2, url: 'https://via.placeholder.com/300x200?text=Feet+Photo+2', caption: 'Another great shot' },
    { id: 3, url: 'https://via.placeholder.com/300x200?text=Feet+Photo+3', caption: 'Feet in nature' },
  ]);

  return (
    <div className="page">
      <h2>Feet Gallery</h2>
      <p>Browse and share feet photos with the community</p>
      
      <div className="gallery-grid">
        {photos.map(photo => (
          <div key={photo.id} className="gallery-item">
            <img src={photo.url} alt={photo.caption} />
            <div style={{ padding: '1rem' }}>
              <p>{photo.caption}</p>
            </div>
          </div>
        ))}
      </div>
      
      <div style={{ marginTop: '2rem' }}>
        <button className="btn">Upload Photo</button>
      </div>
    </div>
  );
}

export default Gallery;
