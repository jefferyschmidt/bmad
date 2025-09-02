Here's the TypeScript React component for the main page of the Guitar Site application:

```typescript
import React, { useState, useEffect } from 'react';
import { NextPage } from 'next';
import { FaSearch } from 'react-icons/fa';
import GuitarCard from '../components/GuitarCard';
import { Guitar, User } from '../types';

interface HomePageProps {
  featuredGuitars: Guitar[];
  newestGuitars: Guitar[];
  topRatedGuitars: Guitar[];
}

const HomePage: NextPage<HomePageProps> = ({
  featuredGuitars,
  newestGuitars,
  topRatedGuitars,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredGuitars, setFilteredGuitars] = useState<Guitar[]>([]);

  useEffect(() => {
    const filtered = [
      ...featuredGuitars,
      ...newestGuitars,
      ...topRatedGuitars,
    ].filter((guitar) =>
      guitar.brand.toLowerCase().includes(searchQuery.toLowerCase()) ||
      guitar.model.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredGuitars(filtered);
  }, [searchQuery, featuredGuitars, newestGuitars, topRatedGuitars]);

  return (
    <div className="container mx-auto py-8">
      <section className="mb-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to Guitar Site</h1>
        <p className="text-lg text-gray-600 mb-6">
          Discover and share your guitar passion with the community.
        </p>
        <div className="flex items-center bg-gray-100 rounded-md px-4 py-2">
          <FaSearch className="text-gray-400 mr-2" />
          <input
            type="text"
            placeholder="Search for guitars..."
            className="bg-transparent w-full focus:outline-none"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Featured Guitars</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredGuitars.map((guitar) => (
            <GuitarCard key={guitar.id} guitar={guitar} />
          ))}
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Newest Guitars</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {newestGuitars.map((guitar) => (
            <GuitarCard key={guitar.id} guitar={guitar} />
          ))}
        </div>
      </section>

      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">Top Rated Guitars</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {topRatedGuitars.map((guitar) => (
            <GuitarCard key={guitar.id} guitar={guitar} />
          ))}
        </div>
      </section>
    </div>
  );
};

export default HomePage;
```

The `GuitarCard` component used in this code is a separate component that displays the details of a single guitar, including the guitar's image, brand, model, and user information.