```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const FeetApp = () => {
  const [feet, setFeet] = useState([]);
  const [newFeetImage, setNewFeetImage] = useState(null);
  const [footJewelry, setFootJewelry] = useState([]);
  const [newFootJewelry, setNewFootJewelry] = useState({
    name: '',
    description: '',
    price: 0,
  });
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetchFeet();
    fetchFootJewelry();
    fetchUser();
  }, []);

  const fetchFeet = async () => {
    try {
      const response = await axios.get('/api/feet');
      setFeet(response.data);
    } catch (error) {
      console.error('Error fetching feet:', error);
    }
  };

  const fetchFootJewelry = async () => {
    try {
      const response = await axios.get('/api/foot-jewelry');
      setFootJewelry(response.data);
    } catch (error) {
      console.error('Error fetching foot jewelry:', error);
    }
  };

  const fetchUser = async () => {
    try {
      const response = await axios.get('/api/user');
      setUser(response.data);
    } catch (error) {
      console.error('Error fetching user:', error);
    }
  };

  const handleFeetImageUpload = async (e) => {
    setNewFeetImage(e.target.files[0]);
  };

  const handlePostFeet = async () => {
    try {
      const formData = new FormData();
      formData.append('image', newFeetImage);
      await axios.post('/api/feet', formData);
      setNewFeetImage(null);
      fetchFeet();
    } catch (error) {
      console.error('Error posting feet:', error);
    }
  };

  const handleCreateFootJewelry = async () => {
    try {
      await axios.post('/api/foot-jewelry', newFootJewelry);
      setNewFootJewelry({ name: '', description: '', price: 0 });
      fetchFootJewelry();
    } catch (error) {
      console.error('Error creating foot jewelry:', error);
    }
  };

  return (
    <div>
      <h1>Feet</h1>
      <div>
        <h2>Share Your Feet</h2>
        <input type="file" onChange={handleFeetImageUpload} />
        <button onClick={handlePostFeet}>Post Feet</button>
        <div>
          {feet.map((foot, index) => (
            <div key={index}>
              <img src={foot.imageUrl} alt={`Foot ${index}`} />
            </div>
          ))}
        </div>
      </div>
      <div>
        <h2>Foot Jewelry Marketplace</h2>
        {user ? (
          <>
            <h3>Sell Foot Jewelry</h3>
            <input
              type="text"
              placeholder="Name"
              value={newFootJewelry.name}
              onChange={(e) =>
                setNewFootJewelry({ ...newFootJewelry, name: e.target.value })
              }
            />
            <textarea
              placeholder="Description"
              value={newFootJewelry.description}
              onChange={(e) =>
                setNewFootJewelry({
                  ...newFootJewelry,
                  description: e.target.value,
                })
              }
            ></textarea>
            <input
              type="number"
              placeholder="Price"
              value={newFootJewelry.price}
              onChange={(e) =>
                setNewFootJewelry({
                  ...newFootJewelry,
                  price: parseFloat(e.target.value),
                })
              }
            />
            <button onClick={handleCreateFootJewelry}>Create Foot Jewelry</button>
          </>
        ) : (
          <p>Please log in to access the foot jewelry marketplace.</p>
        )}
        <div>
          {footJewelry.map((jewelry, index) => (
            <div key={index}>
              <h3>{jewelry.name}</h3>
              <p>{jewelry.description}</p>
              <p>Price: ${jewelry.price}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FeetApp;
```