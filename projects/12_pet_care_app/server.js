```javascript
const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const { Pool } = require('pg');

// PostgreSQL connection
const pool = new Pool({
  user: 'your_postgres_user',
  host: 'your_postgres_host',
  database: 'your_postgres_database',
  password: 'your_postgres_password',
  port: 5432
});

// Middleware setup
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something went wrong!');
});

// Routes
app.get('/api/pets', async (req, res, next) => {
  try {
    const { rows } = await pool.query('SELECT * FROM pets');
    res.json(rows);
  } catch (err) {
    next(err);
  }
});

app.post('/api/pets', async (req, res, next) => {
  try {
    const { name, type } = req.body;
    const { rows } = await pool.query('INSERT INTO pets (name, type) VALUES ($1, $2) RETURNING *', [name, type]);
    res.status(201).json(rows[0]);
  } catch (err) {
    next(err);
  }
});

app.get('/api/feedings', async (req, res, next) => {
  try {
    const { rows } = await pool.query('SELECT * FROM feedings');
    res.json(rows);
  } catch (err) {
    next(err);
  }
});

app.post('/api/feedings', async (req, res, next) => {
  try {
    const { pet_id, timestamp, amount } = req.body;
    const { rows } = await pool.query('INSERT INTO feedings (pet_id, timestamp, amount) VALUES ($1, $2, $3) RETURNING *', [pet_id, timestamp, amount]);
    res.status(201).json(rows[0]);
  } catch (err) {
    next(err);
  }
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
```