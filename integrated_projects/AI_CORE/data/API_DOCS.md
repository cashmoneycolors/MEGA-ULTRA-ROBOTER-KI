# Autonomous Wealth System - API Documentation

## Overview
REST API for the Autonomous Wealth Generation System. All endpoints require authentication via API key.

## Authentication
Include API key in request header:
```
X-API-Key: your-api-key-here
```

## Endpoints

### System Status
**GET** `/api/status`

Get current system status.

**Response:**
```json
{
  "capital": 11077582.63,
  "target": 10000,
  "progress": 110775.83,
  "cycles": 8,
  "art_assets": 1057,
  "trades": 44,
  "active_clones": 22,
  "timestamp": "2025-11-28T05:30:37.397875"
}
```

### Transactions
**GET** `/api/transactions`

Get recent transactions (last 100).

**Response:**
```json
[
  {
    "id": 1,
    "timestamp": "2025-11-28T04:47:16",
    "type": "profit",
    "amount": 217.50,
    "balance": 317.50
  }
]
```

### Clones
**GET** `/api/clones`

Get all active clones.

**Response:**
```json
[
  {
    "id": 1,
    "created_at": "2025-11-28T04:47:18",
    "status": "active",
    "profit": 0
  }
]
```

### Execute Cycle
**POST** `/api/cycle`

Execute production cycle manually.

**Response:**
```json
{
  "profit": 1754482.15,
  "capital": 2208751.78,
  "status": "success"
}
```

### Analytics
**GET** `/api/analytics`

Get analytics data.

**Response:**
```json
{
  "art_profit": 9348765.5,
  "trading_profit": 47469.88,
  "avg_cycle_profit": 579964.72,
  "total_profit": 9396235.38
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "error": "API key required"
}
```

### 403 Forbidden
```json
{
  "error": "Invalid API key"
}
```

### 500 Server Error
```json
{
  "error": "Internal server error"
}
```

## Rate Limiting
- 1000 requests per hour per API key
- Excess requests return 429 Too Many Requests

## Examples

### Get Status
```bash
curl -H "X-API-Key: your-key" http://localhost:5000/api/status
```

### Execute Cycle
```bash
curl -X POST -H "X-API-Key: your-key" http://localhost:5000/api/cycle
```

### Get Analytics
```bash
curl -H "X-API-Key: your-key" http://localhost:5000/api/analytics
```

## Webhooks
Subscribe to system events:
- `cycle.completed` - Production cycle completed
- `milestone.reached` - Capital milestone reached
- `error.occurred` - System error occurred

## SDK

### Python
```python
import requests

headers = {"X-API-Key": "your-key"}
response = requests.get("http://localhost:5000/api/status", headers=headers)
print(response.json())
```

### JavaScript
```javascript
const headers = {"X-API-Key": "your-key"};
fetch("http://localhost:5000/api/status", {headers})
  .then(r => r.json())
  .then(data => console.log(data));
```

## Support
For issues or questions, contact: support@wealth-system.com
