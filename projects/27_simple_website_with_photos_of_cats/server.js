```javascript
const express = require('express');
const { Pool } = require('pg');

const app = express();
const port = process.env.PORT || 3000;

// PostgreSQL connection
const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT,
});

// Middleware
app.use(express.json());

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

// Cat Photo routes
app.get('/api/photos', async (req, res, next) => {
  try {
    const { page = 1, limit = 10, sort, filter } = req.query;
    const offset = (page - 1) * limit;

    let query = 'SELECT cp.id, cp.url, pm.caption, pm.breed, pm.color, cp.created_at FROM cat_photos cp JOIN photo_metadata pm ON cp.id = pm.cat_photo_id';
    const params = [];

    if (sort) {
      query += ' ORDER BY ?';
      params.push(sort);
    }

    if (filter) {
      query += ' WHERE ?';
      params.push(filter);
    }

    query += ' LIMIT ? OFFSET ?';
    params.push(limit, offset);

    const { rows } = await pool.query(query, params);
    const totalCount = await pool.query('SELECT COUNT(*) FROM cat_photos');

    res.json({
      data: rows,
      pagination: {
        current_page: page,
        total_pages: Math.ceil(totalCount.rows[0].count / limit),
        total_items: totalCount.rows[0].count,
      },
    });
  } catch (err) {
    next(err);
  }
});

app.get('/api/photos/:id', async (req, res, next) => {
  try {
    const { id } = req.params;
    const { rows } = await pool.query(
      'SELECT cp.id, cp.url, pm.caption, pm.breed, pm.color, cp.created_at FROM cat_photos cp JOIN photo_metadata pm ON cp.id = pm.cat_photo_id WHERE cp.id = $1',
      [id]
    );

    if (rows.length === 0) {
      return res.status(404).json({ error: 'Cat photo not found' });
    }

    res.json(rows[0]);
  } catch (err) {
    next(err);
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
```