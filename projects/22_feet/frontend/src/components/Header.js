import React from 'react';
import { Link } from 'react-router-dom';

function Header() {
  return (
    <header className="header">
      <h1>Feet Gallery & Marketplace</h1>
      <nav className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/gallery">Gallery</Link>
        <Link to="/marketplace">Marketplace</Link>
      </nav>
    </header>
  );
}

export default Header;
