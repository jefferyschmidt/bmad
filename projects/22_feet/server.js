```javascript
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const pg = require('pg');

const app = express();
const port = process.env.PORT || 3000;

// Connect to PostgreSQL database
const pool = new pg.Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false
  }
});

// Middleware setup
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

// Routes

// Feet photo sharing
app.get('/feet', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM feet');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.post('/feet', async (req, res) => {
  try {
    const { imageUrl, description } = req.body;
    await pool.query('INSERT INTO feet (image_url, description) VALUES ($1, $2)', [imageUrl, description]);
    res.status(201).json({ message: 'Feet photo uploaded successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

// Foot jewelry marketplace
app.get('/jewelry', async (req, res) => {
  try {
    const { rows } = await pool.query('SELECT * FROM jewelry');
    res.json(rows);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

app.post('/jewelry', async (req, res) => {
  try {
    const { name, description, price } = req.body;
    await pool.query('INSERT INTO jewelry (name, description, price) VALUES ($1, $2, $3)', [name, description, price]);
    res.status(201).json({ message: 'Foot jewelry item added successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Server error' });
  }
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal server error' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
```