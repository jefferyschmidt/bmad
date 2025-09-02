Here is a TypeScript API route that matches the system architecture requirements:

```typescript
import { NextApiRequest, NextApiResponse } from 'next';
import { Pool } from 'pg';

// Database connection
const pool = new Pool({
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  host: process.env.POSTGRES_HOST,
  database: process.env.POSTGRES_DB,
  port: parseInt(process.env.POSTGRES_PORT || '5432', 10),
});

// Type definitions
interface Guitar {
  id: number;
  userId: number;
  brand: string;
  model: string;
  year: number;
  description: string;
  photos: string[];
}

interface ApiResponse<T> {
  data: T;
  error?: string;
}

// API route handler
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<ApiResponse<Guitar>>
) {
  if (req.method === 'POST') {
    try {
      const { userId, brand, model, year, description, photos } = req.body;
      const { rows } = await pool.query(
        'INSERT INTO guitars (userId, brand, model, year, description, photos) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *',
        [userId, brand, model, year, description, photos]
      );
      const newGuitar: Guitar = rows[0];
      res.status(201).json({ data: newGuitar });
    } catch (error) {
      res.status(500).json({ error: 'Error creating guitar' });
    }
  } else if (req.method === 'GET') {
    try {
      const { id } = req.query;
      const { rows } = await pool.query('SELECT * FROM guitars WHERE id = $1', [
        id,
      ]);
      if (rows.length === 0) {
        res.status(404).json({ error: 'Guitar not found' });
      } else {
        const guitar: Guitar = rows[0];
        res.status(200).json({ data: guitar });
      }
    } catch (error) {
      res.status(500).json({ error: 'Error retrieving guitar' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
```