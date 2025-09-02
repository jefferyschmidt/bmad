import React from 'react';

function Home() {
  return (
    <div className="page">
      <h2>Welcome to Feet Gallery & Marketplace</h2>
      <p>Share your feet photos and discover unique foot jewelry!</p>
      <div style={{ marginTop: '2rem' }}>
        <h3>Features:</h3>
        <ul style={{ textAlign: 'left', maxWidth: '600px', margin: '0 auto' }}>
          <li>📸 Share feet photos in our gallery</li>
          <li>🛍️ Browse and buy handmade foot jewelry</li>
          <li>💎 Sell your own foot jewelry creations</li>
          <li>👥 Connect with other feet enthusiasts</li>
        </ul>
      </div>
    </div>
  );
}

export default Home;
