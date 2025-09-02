Here's the TypeScript React component for the main page of the Guitar Site application:

```tsx
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { FaSearch, FaRegThumbsUp, FaRegCommentAlt, FaShareAlt } from 'react-icons/fa';

interface Guitar {
  id: string;
  title: string;
  brand: string;
  model: string;
  year: number;
  description: string;
  imageUrl: string;
  userId: string;
  user: {
    id: string;
    name: string;
    avatar: string;
  };
  likes: number;
  comments: number;
}

const Home: React.FC = () => {
  const [guitars, setGuitars] = useState<Guitar[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  useEffect(() => {
    // Fetch featured guitar posts from the API
    const fetchGuitars = async () => {
      const response = await fetch('/api/guitars?featured=true');
      const data = await response.json();
      setGuitars(data);
    };
    fetchGuitars();
  }, []);

  const handleSearch = () => {
    router.push({
      pathname: '/explore',
      query: { q: searchQuery },
    });
  };

  return (
    <div className="bg-gray-100 min-h-screen">
      <header className="bg-navy-blue py-6 shadow-md">
        <div className="container mx-auto px-4 flex items-center justify-between">
          <a href="/" className="text-2xl font-bold text-white">
            Guitar Site
          </a>
          <div className="flex items-center">
            <input
              type="text"
              placeholder="Search for guitars..."
              className="px-4 py-2 rounded-l-md border-gray-300 border-r-0 focus:outline-none focus:ring-2 focus:ring-orange"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button
              className="bg-orange px-4 py-2 rounded-r-md text-white hover:bg-orange-500 focus:outline-none focus:ring-2 focus:ring-orange"
              onClick={handleSearch}
            >
              <FaSearch />
            </button>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-6">Featured Guitars</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {guitars.map((guitar) => (
            <div key={guitar.id} className="bg-white rounded-lg shadow-md overflow-hidden">
              <img src={guitar.imageUrl} alt={guitar.title} className="w-full h-48 object-cover" />
              <div className="p-4">
                <h2 className="text-xl font-bold">{guitar.title}</h2>
                <p className="text-gray-500 mb-2">
                  {guitar.brand} {guitar.model} ({guitar.year})
                </p>
                <p className="text-gray-700 mb-4">{guitar.description}</p>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <img src={guitar.user.avatar} alt={guitar.user.name} className="w-8 h-8 rounded-full" />
                    <span className="text-gray-500">{guitar.user.name}</span>
                  </div>
                  <div className="flex items-center space-x-2 text-gray-500">
                    <span className="flex items-center space-x-1">
                      <FaRegThumbsUp />
                      <span>{guitar.likes}</span>
                    </span>
                    <span className="flex items-center space-x-1">
                      <FaRegCommentAlt />
                      <span>{guitar.comments}</span>
                    </span>
                    <FaShareAlt />
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>

      <footer className="bg-navy-blue text-white py-4">
        <div className="container mx-auto px-4 flex items-center justify-between">
          <p>&copy; 2023 Guitar Site. All rights reserved.</p>
          <nav>
            <ul className="flex space-x-4">
              <li>
                <a href="#" className="hover:text-orange">
                  Home
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-orange">
                  Explore
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-orange">
                  Profile
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </footer>
    </div>
  );
};

export default Home;
```