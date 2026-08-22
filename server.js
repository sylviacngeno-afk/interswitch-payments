const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(path.join(__dirname, 'web')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'web', 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Interswitch Portal running on port ${PORT}`);
  console.log(`Open: http://localhost:${PORT}`);
});
