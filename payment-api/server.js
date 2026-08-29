const express = require('express');
const cors = require('cors');
const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

const serviceStatus = {
  lastUpdated: new Date().toISOString(),
  overall: 'operational',
  services: [
    { name: 'Payment API', status: 'operational', uptime: '99.98%', latency: '45ms' },
    { name: 'Verve Network', status: 'operational', uptime: '99.95%', latency: '120ms' },
    { name: 'Merchant Portal', status: 'operational', uptime: '99.99%', latency: '32ms' },
    { name: 'Settlement Engine', status: 'operational', uptime: '99.97%', latency: '88ms' },
    { name: 'Fraud Detection', status: 'operational', uptime: '99.96%', latency: '210ms' },
    { name: 'Notification Service', status: 'maintenance', uptime: '98.50%', latency: 'N/A' }
  ]
};

app.get('/status', (req, res) => {
  serviceStatus.lastUpdated = new Date().toISOString();
  res.json(serviceStatus);
});

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', service: 'payment-api' });
});

app.get('/', (req, res) => {
  res.json({
    name: 'Interswitch Payment Status API',
    version: '1.0.0',
    endpoints: ['/status', '/health']
  });
});

app.listen(PORT, () => {
  console.log(`Payment API running on port ${PORT}`);
});
