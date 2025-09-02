```typescript
import React, { useState } from 'react';
import Link from 'next/link';
import { FaSearch, FaRegThumbsUp, FaRegCommentAlt } from 'react-icons/fa';

interface Guitar {
  id: string;
  name: string;
  brand: string;
  model: string;
  description: string;
  imageUrl: string;
  userId: string;
  user: {
    id: string;
    name: string;
    avatar: string;
  };
  comments: {
    id: string;
    content: string;
    userId: string;
    user: {
      id: string;
      name: string;
      avatar: string;
    };
  }[];
  likes: number;
}

const HomePage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [guitars, setGuitars] = useState<Guitar[]>([
    {
      id: '1',
      name: 'Gibson Les Paul Standard',
      brand: 'Gibson',
      model: 'Les Paul Standard',
      description: 'A classic electric guitar with a timeless design.',
      imageUrl: '/guitars/gibson-les-paul.jpg',
      userId: '1',
      user: {
        id: '1',
        name: 'John Doe',
        avatar: '/avatars/john-doe.jpg',
      },
      comments: [
        {
          id: '1',
          content: 'This guitar is amazing!',
          userId: '2',
          user: {
            id: '2',
            name: 'Jane Smith',
            avatar: '/avatars/jane-smith.jpg',
          },
        },
      ],
      likes: 15,
    },
    // Add more guitar data
  ]);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const filteredGuitars = guitars.filter((guitar) =>
    guitar.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="bg-gray-100 min-h-screen">
      <header className="bg-navy-blue py-4 px-6">
        <div className="container mx-auto flex justify-between items-center">
          <Link href="/">
            <a className="text-white text-2xl font-bold">Guitar Site</a>
          </Link>
          <div className="flex items-center">
            <div className="relative">
              <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Search guitars"
                className="bg-white rounded-full py-2 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-orange"
                value={searchQuery}
                onChange={handleSearch}
              />
            </div>
            <Link href="/profile">
              <a className="ml-4 bg-orange rounded-full py-2 px-4 text-white hover:bg-orange-dark focus:outline-none focus:ring-2 focus:ring-orange">
                Create Profile
              </a>
            </Link>
          </div>
        </div>
      </header>

      <main className="container mx-auto py-8">
        <h1 className="text-4xl font-bold mb-6">Featured Guitars</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {filteredGuitars.map((guitar) => (
            <div key={guitar.id} className="bg-white rounded-lg shadow-md">
              <img
                src={guitar.imageUrl}
                alt={guitar.name}
                className="w-full h-48 object-cover rounded-t-lg"
              />
              <div className="p-4">
                <div className="flex items-center mb-2">
                  <img
                    src={guitar.user.avatar}
                    alt={guitar.user.name}
                    className="w-8 h-8 rounded-full mr-2"
                  />
                  <h3 className="text-lg font-bold">{guitar.user.name}</h3>
                </div>
                <h2 className="text-xl font-bold mb-2">{guitar.name}</h2>
                <p className="text-gray-600 mb-4">{guitar.description}</p>
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <FaRegThumbsUp className="text-gray-400 mr-1" />
                    <span className="text-gray-600">{guitar.likes}</span>
                  </div>
                  <div className="flex items-center">
                    <FaRegCommentAlt className="text-gray-400 mr-1" />
                    <span className="text-gray-600">
                      {guitar.comments.length}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
};

export default HomePage;
```