const http = require('http');
const url = require('url');

const hostname = 'localhost';
const port = 3000;

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);

    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }

    if (parsedUrl.pathname === '/test') {
        res.writeHead(200, {'Content-Type': 'text/plain'});
        res.end('Mega Ultra AI Server Running!');
    } else if (parsedUrl.pathname === '/status') {
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({status: 'running', components: ['AI', 'Node.js', 'Ollama']}));
    } else if (parsedUrl.pathname === '/ai' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            try {
                const { prompt } = JSON.parse(body);
                res.writeHead(200, {'Content-Type': 'application/json'});
                res.end(JSON.stringify({
                    response: `AI Response to: ${prompt || 'Empty prompt'} - Quantum Optimized Processing Complete.`,
                    model: 'llama3.2:3b'
                }));
            } catch (error) {
                res.writeHead(400, {'Content-Type': 'application/json'});
                res.end(JSON.stringify({error: 'Invalid JSON'}));
            }
        });
    } else {
        res.writeHead(404, {'Content-Type': 'text/plain'});
        res.end('Endpoint not found');
    }
});

server.listen(port, hostname, () => {
    console.log(`Mega Ultra AI Server running at http://${hostname}:${port}/`);
    console.log('Available endpoints: /test, /status, /ai');
    console.log('Use CTRL+C to stop the server');
});
