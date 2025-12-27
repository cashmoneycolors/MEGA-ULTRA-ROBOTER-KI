import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

function getArgValue(flag) {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return undefined;
  const value = process.argv[idx + 1];
  if (!value || value.startsWith('-')) return undefined;
  return value;
}

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const portArg = getArgValue('--port');
const port = portArg ? Number.parseInt(portArg, 10) : 3000;
const hostArg = getArgValue('--host');
const host = hostArg || process.env.MEGA_BIND_HOST || '0.0.0.0';

const webhookBase = (process.env.MEGA_WEBHOOK_BASE || 'http://127.0.0.1:8503').replace(/\/+$/, '');

async function proxyJson(req, res, targetUrl, init) {
  try {
    const r = await fetch(targetUrl, init);
    const text = await r.text();
    res.writeHead(r.status, {
      'Content-Type': r.headers.get('content-type') || 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
    });
    res.end(text);
  } catch (err) {
    res.writeHead(502, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
    res.end(JSON.stringify({ ok: false, error: String(err) }));
  }
}

async function readRequestBody(req) {
  return await new Promise((resolve, reject) => {
    const chunks = [];
    req.on('data', (c) => chunks.push(c));
    req.on('end', () => resolve(Buffer.concat(chunks)));
    req.on('error', reject);
  });
}

const server = createServer((req, res) => {
  const url = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`);
  const pathname = url.pathname;

  if (pathname === '/status' || pathname === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ ok: true, status: 'running' }));
    return;
  }

  if (pathname === '/mobile') {
    const filePath = path.join(__dirname, 'public', 'mobile_dashboard.html');
    readFile(filePath)
      .then((buf) => {
        res.writeHead(200, {
          'Content-Type': 'text/html; charset=utf-8',
          'Cache-Control': 'no-store',
        });
        res.end(buf);
      })
      .catch((err) => {
        res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end(`Failed to load mobile dashboard: ${String(err)}`);
      });
    return;
  }

  if (pathname === '/api/stats') {
    proxyJson(req, res, `${webhookBase}/stats`, { method: 'GET' });
    return;
  }

  if (pathname === '/api/paypal/create-order' && req.method === 'POST') {
    readRequestBody(req)
      .then((body) => proxyJson(req, res, `${webhookBase}/paypal/create-order`, {
        method: 'POST',
        headers: { 'Content-Type': req.headers['content-type'] || 'application/json' },
        body,
      }))
      .catch((err) => {
        res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' });
        res.end(JSON.stringify({ ok: false, error: String(err) }));
      });
    return;
  }

  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Hello World!\n');
});

server.listen(port, host, () => {
  console.log(`Listening on ${host}:${port}`);
});

// run with `node server.mjs --port 3000 --host 0.0.0.0`
