```jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom';
import axios from 'axios';

// Components
import PhotoGrid from './components/PhotoGrid';
import PhotoDetails from './components/PhotoDetails';
import About from './components/About';

const App = () => {
  const [catPhotos, setCatPhotos] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchCatPhotos(currentPage);
  }, [currentPage]);

  const fetchCatPhotos = async (page) => {
    try {
      const response = await axios.get(`/api/photos?page=${page}&limit=20&search=${searchQuery}`);
      setCatPhotos(response.data.data);
      setTotalPages(response.data.pagination.total_pages);
    } catch (error) {
      console.error('Error fetching cat photos:', error);
    }
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  const handleSearch = (query) => {
    setSearchQuery(query);
    setCurrentPage(1);
    fetchCatPhotos(1);
  };

  return (
    <Router>
      <div className="app">
        <header>
          <nav>
            <ul>
              <li>
                <Link to="/">Home</Link>
              </li>
              <li>
                <Link to="/gallery">Photo Gallery</Link>
              </li>
              <li>
                <Link to="/about">About</Link>
              </li>
            </ul>
            <div className="search-bar">
              <input
                type="text"
                placeholder="Search cat photos..."
                value={searchQuery}
                onChange={(e) => handleSearch(e.target.value)}
              />
            </div>
          </nav>
        </header>

        <Switch>
          <Route path="/gallery">
            <PhotoGrid catPhotos={catPhotos} onPageChange={handlePageChange} totalPages={totalPages} />
          </Route>
          <Route path="/photo/:id">
            <PhotoDetails />
          </Route>
          <Route path="/about">
            <About />
          </Route>
          <Route path="/">
            <PhotoGrid catPhotos={catPhotos} onPageChange={handlePageChange} totalPages={totalPages} />
          </Route>
        </Switch>
      </div>
    </Router>
  );
};

export default App;
```