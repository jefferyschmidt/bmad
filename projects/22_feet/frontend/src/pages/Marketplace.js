import React, { useState } from 'react';

function Marketplace() {
  const [products] = useState([
    { id: 1, name: 'Silver Foot Ring', price: 29.99, image: 'https://via.placeholder.com/300x200?text=Silver+Ring' },
    { id: 2, name: 'Gold Ankle Bracelet', price: 49.99, image: 'https://via.placeholder.com/300x200?text=Gold+Bracelet' },
    { id: 3, name: 'Pearl Toe Ring', price: 19.99, image: 'https://via.placeholder.com/300x200?text=Pearl+Ring' },
  ]);

  return (
    <div className="page">
      <h2>Foot Jewelry Marketplace</h2>
      <p>Discover unique handmade foot jewelry</p>
      
      <div className="marketplace-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <img src={product.image} alt={product.name} />
            <h3>{product.name}</h3>
            <p>${product.price}</p>
            <button className="btn">Add to Cart</button>
            <button className="btn">View Details</button>
          </div>
        ))}
      </div>
      
      <div style={{ marginTop: '2rem' }}>
        <button className="btn">Sell Your Jewelry</button>
      </div>
    </div>
  );
}

export default Marketplace;
