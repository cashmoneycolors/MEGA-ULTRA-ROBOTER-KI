#!/usr/bin/env node
/**
 * SICHERHEITSHINWEIS: Kritische Secrets (z.B. JWT_SECRET, MAINTENANCE_KEY) werden ausschließlich über Umgebungsvariablen bezogen oder sicher zur Laufzeit generiert. Niemals hardcodieren!
 * Wenn ein Secret generiert wird, erscheint eine gelbe Warnung (console.warn). Siehe Projektdoku und Copilot-Instructions.
 */

const crypto = require('crypto');

function getSecretEnvOrGenerate(envName, length = 32) {
    const value = process.env[envName];
    if (value) return value;
    const generated = crypto.randomBytes(length).toString('base64url');
    console.warn(`\x1b[33mWARNUNG: ${envName} nicht gefunden, generiere zur Laufzeit! Niemals hardcodieren!\x1b[0m`);
    return generated;
}

// Beispiel für kritische Secrets
const JWT_SECRET = getSecretEnvOrGenerate('JWT_SECRET', 32);
const MAINTENANCE_KEY = getSecretEnvOrGenerate('MAINTENANCE_KEY', 32);

/**
 * 🔥 MEGA ULTRA AI SYSTEM - ENHANCED OPENGAZAI SERVER V2.0 🔥
 * MAXIMALE SICHERHEIT UND PERFORMANCE OPTIMIERUNG
 * Erweiterte Autonomie mit Ollama Integration
 * Erstellt: 03. Oktober 2025 - Verbessert für maximale Sicherheit
 */

const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const helmet = require('helmet');
const cors = require('cors');
const compression = require('compression');
const morgan = require('morgan');
const fs = require('fs').promises;
const path = require('path');
const crypto = require('crypto');
const os = require('os');
const cluster = require('cluster');
const winston = require('winston');
const minimist = require('minimist');

// ===============================
// 🎯 KOMMANDOZEILEN-ARGUMENTE
// ===============================
const args = minimist(process.argv.slice(2), {
    default: {
        port: process.env.PORT || 3000,
        'admin-port': process.env.ADMIN_PORT || 3001,
        'secure-mode': process.env.ENABLE_SSL === 'true' || false,
        'rate-limit': process.env.ENABLE_RATE_LIMITING === 'true' || true,
        'max-requests-per-minute': parseInt(process.env.MAX_FAILED_REQUESTS_PER_MINUTE) || 60,
        'enable-logging': process.env.ENABLE_REQUEST_LOGGING === 'true' || true,
        'cluster-mode': process.env.ENABLE_CLUSTER_MODE === 'true' || false,
        'workers': parseInt(process.env.CLUSTER_WORKERS) || os.cpus().length
    }
});

// =================== WICHTIG: SECRET-HANDLING (MAXIMALE SICHERHEIT) ===================
// Secrets wie JWT_SECRET und MAINTENANCE_KEY dürfen NIEMALS im Quellcode hardcodiert werden!
// 1. Immer zuerst per Umgebungsvariable beziehen (z.B. aus Docker, .env, CI/CD, Key Vault).
// 2. Falls nicht gesetzt, wird der Server NICHT gestartet (Produktionssicherheit).
// 3. Entwickler:innen werden explizit gewarnt, wenn ein Secret fehlt.
// ======================================================================================
if (!process.env.JWT_SECRET) {
    console.error('[FATAL] JWT_SECRET ist NICHT gesetzt! Bitte Secret als Umgebungsvariable setzen (z.B. export JWT_SECRET=...) – Niemals im Code speichern!');
    process.exit(1);
}
if (!process.env.MAINTENANCE_KEY) {
    console.error('[FATAL] MAINTENANCE_KEY ist NICHT gesetzt! Bitte Secret als Umgebungsvariable setzen (z.B. export MAINTENANCE_KEY=...) – Niemals im Code speichern!');
    process.exit(1);
}
// ===============================
// 🔧 ERWEITERTE KONFIGURATION
// ===============================
const CONFIG = {
    // Basis-Konfiguration
    PORT: parseInt(args.port),
    ADMIN_PORT: parseInt(args['admin-port']),
    OLLAMA_TARGET_URL: process.env.OLLAMA_TARGET_URL || 'http://localhost:11434',
    
    // Sicherheit
    JWT_SECRET: process.env.JWT_SECRET || (() => { throw new Error('JWT_SECRET ist erforderlich!'); })(),
    MAINTENANCE_KEY: process.env.MAINTENANCE_KEY || (() => { throw new Error('MAINTENANCE_KEY ist erforderlich!'); })(),
    API_KEY: process.env.API_KEY || crypto.randomBytes(32).toString('hex'),
    
    // Features
    SECURE_MODE: args['secure-mode'],
    ENABLE_RATE_LIMITING: args['rate-limit'],
    MAX_REQUESTS_PER_MINUTE: args['max-requests-per-minute'],
    ENABLE_LOGGING: args['enable-logging'],
    ENABLE_CLUSTER: args['cluster-mode'],
    CLUSTER_WORKERS: args.workers,
    
    // Pfade
    DATA_PATH: process.env.DATA_PATH || './data',
    LOG_PATH: process.env.LOG_PATH || './logs',
    
    // Erweiterte Einstellungen
    LLM_MODEL_NAME: process.env.LLM_MODEL_NAME || 'llama3.2:3b',
    DEFAULT_TOKEN_LIMIT: parseInt(process.env.DEFAULT_TOKEN_LIMIT) || 10000000,
    MAX_RATE_LIMIT_FACTOR: parseInt(process.env.MAX_RATE_LIMIT_FACTOR) || 120,
    ENABLE_INTRUSION_DETECTION: process.env.ENABLE_INTRUSION_DETECTION === 'true' || true,
    ENABLE_PREDICTIVE_SCALING: process.env.ENABLE_PREDICTIVE_SCALING === 'true' || true,
    
    // Performance
    REQUEST_TIMEOUT: 300000, // 5 Minuten
    MAX_FILE_SIZE: '50mb',
    COMPRESSION_LEVEL: 6
};

// ===============================
// 📝 ERWEITERTE LOGGING-KONFIGURATION
// ===============================
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
    ),
    transports: [
        new winston.transports.File({ 
            filename: path.join(CONFIG.LOG_PATH, 'error.log'), 
            level: 'error',
            maxsize: 10485760, // 10MB
            maxFiles: 5
        }),
        new winston.transports.File({ 
            filename: path.join(CONFIG.LOG_PATH, 'combined.log'),
            maxsize: 10485760, // 10MB
            maxFiles: 5
        }),
        new winston.transports.Console({
            format: winston.format.combine(
                winston.format.colorize(),
                winston.format.simple()
            )
        })
    ]
});

// ===============================
// 📊 ERWEITERTE METRIKEN-SAMMLUNG
// ===============================
class AdvancedMetrics {
    constructor() {
        this.startTime = Date.now();
        this.totalRequests = 0;
        this.errorCount = 0;
        this.activeConnections = 0;
        this.requestsPerSecond = 0;
        this.avgResponseTime = 0;
        this.requestHistory = [];
        this.ipRequestCount = new Map();
        this.suspiciousIPs = new Set();
        
        // Metriken alle 10 Sekunden aktualisieren
        setInterval(() => this.updateMetrics(), 10000);
        
        // IP-Zähler alle Stunde zurücksetzen
        setInterval(() => this.resetIPCounters(), 3600000);
    }
    
    recordRequest(ip, responseTime) {
        this.totalRequests++;
        this.activeConnections = Math.max(0, this.activeConnections);
        
        // Request-Geschichte für RPS-Berechnung
        const now = Date.now();
        this.requestHistory.push(now);
        
        // Behalte nur Requests der letzten Minute
        this.requestHistory = this.requestHistory.filter(time => now - time <= 60000);
        
        // Response-Zeit-Durchschnitt aktualisieren
        if (responseTime) {
            this.avgResponseTime = (this.avgResponseTime + responseTime) / 2;
        }
        
        // IP-Tracking für Intrusion Detection
        if (ip) {
            const count = this.ipRequestCount.get(ip) || 0;
            this.ipRequestCount.set(ip, count + 1);
            
            // Verdächtige IP markieren (>1000 Requests pro Stunde)
            if (count > 1000) {
                this.suspiciousIPs.add(ip);
                logger.warn(`Suspicious IP detected: ${ip} with ${count} requests`);
            }
        }
    }
    
    recordError(type) {
        this.errorCount++;
        logger.error(`Error recorded: ${type}`);
    }
    
    connectionOpened() {
        this.activeConnections++;
    }
    
    connectionClosed() {
        this.activeConnections = Math.max(0, this.activeConnections - 1);
    }
    
    updateMetrics() {
        const now = Date.now();
        const recentRequests = this.requestHistory.filter(time => now - time <= 60000);
        this.requestsPerSecond = recentRequests.length / 60;
    }
    
    resetIPCounters() {
        this.ipRequestCount.clear();
        this.suspiciousIPs.clear();
        logger.info('IP counters reset');
    }
    
    getMetrics() {
        return {
            uptime: Date.now() - this.startTime,
            totalRequests: this.totalRequests,
            errorCount: this.errorCount,
            activeConnections: this.activeConnections,
            requestsPerSecond: this.requestsPerSecond,
            avgResponseTime: this.avgResponseTime,
            memoryUsage: process.memoryUsage(),
            cpuUsage: process.cpuUsage(),
            suspiciousIPs: Array.from(this.suspiciousIPs),
            topIPs: Array.from(this.ipRequestCount.entries())
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10)
        };
    }
}

const metrics = new AdvancedMetrics();

// ===============================
// 🛡️ ERWEITERTE SICHERHEITS-MIDDLEWARE
// ===============================
const securityMiddleware = (req, res, next) => {
    const clientIP = req.ip || req.connection.remoteAddress || 'unknown';
    
    // Intrusion Detection
    if (CONFIG.ENABLE_INTRUSION_DETECTION && metrics.suspiciousIPs.has(clientIP)) {
        logger.warn(`Blocked request from suspicious IP: ${clientIP}`);
        return res.status(429).json({ 
            error: 'Rate limit exceeded',
            message: 'Your IP has been temporarily blocked due to suspicious activity'
        });
    }
    
    // Request-Größe prüfen
    if (req.headers['content-length'] && parseInt(req.headers['content-length']) > 52428800) { // 50MB
        logger.warn(`Large request blocked from ${clientIP}: ${req.headers['content-length']} bytes`);
        return res.status(413).json({
            error: 'Request too large',
            message: 'Request size exceeds maximum allowed limit'
        });
    }
    
    // Suspicious User-Agent prüfen
    const userAgent = req.headers['user-agent'] || '';
    const suspiciousPatterns = [
        /bot/i, /crawler/i, /spider/i, /scraper/i,
        /curl/i, /wget/i, /python/i, /go-http/i
    ];
    
    const isSuspicious = suspiciousPatterns.some(pattern => pattern.test(userAgent));
    if (isSuspicious && !req.path.startsWith('/api/')) {
        logger.warn(`Suspicious User-Agent blocked: ${userAgent} from ${clientIP}`);
        return res.status(403).json({
            error: 'Access denied',
            message: 'Your request has been blocked by security policies'
        });
    }
    
    // SQL Injection Detection (vereinfacht)
    const body = JSON.stringify(req.body || {}) + (req.url || '');
    const sqlPatterns = [
        /(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|CREATE)\b)/i,
        /(\'|\"|;|--|\*|\||\^|\$)/i,
        /(\bOR\b|\bAND\b).*=.*=/i
    ];
    
    const hasSQLInjection = sqlPatterns.some(pattern => pattern.test(body));
    if (hasSQLInjection) {
        logger.error(`SQL Injection attempt from ${clientIP}: ${body.substring(0, 200)}`);
        return res.status(400).json({
            error: 'Invalid request',
            message: 'Request contains potentially malicious content'
        });
    }
    
    next();
};

// ===============================
// 📊 REQUEST-TRACKING MIDDLEWARE
// ===============================
const trackingMiddleware = (req, res, next) => {
    const startTime = Date.now();
    const clientIP = req.ip || req.connection.remoteAddress || 'unknown';
    
    metrics.connectionOpened();
    
    res.on('finish', () => {
        const responseTime = Date.now() - startTime;
        metrics.recordRequest(clientIP, responseTime);
        metrics.connectionClosed();
        
        if (res.statusCode >= 400) {
            metrics.recordError(`HTTP_${res.statusCode}`);
        }
    });
    
    next();
};

// ===============================
// 🔐 JWT-MIDDLEWARE (ERWEITERT)
// ===============================
const jwtMiddleware = (req, res, next) => {
    // Öffentliche Endpunkte
    const publicPaths = ['/health', '/status', '/metrics'];
    if (publicPaths.includes(req.path)) {
        return next();
    }
    
    const authHeader = req.headers.authorization;
    const apiKeyHeader = req.headers['x-api-key'];
    
    // API-Key Authentication
    if (apiKeyHeader === CONFIG.API_KEY) {
        req.user = { type: 'api-key', authenticated: true };
        return next();
    }
    
    // JWT Authentication
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({
            error: 'Authentication required',
            message: 'Valid Bearer token or API key required'
        });
    }
    
    const token = authHeader.substring(7);
    
    try {
        const decoded = jwt.verify(token, CONFIG.JWT_SECRET);
        req.user = decoded;
        
        // Token-Limit prüfen (falls vorhanden)
        if (decoded.tokenLimit && decoded.tokensUsed >= decoded.tokenLimit) {
            return res.status(429).json({
                error: 'Token limit exceeded',
                message: 'Your token usage limit has been reached'
            });
        }
        
        next();
    } catch (err) {
        logger.error(`JWT verification failed: ${err.message}`);
        return res.status(401).json({
            error: 'Invalid token',
            message: 'Token verification failed'
        });
    }
};

// ===============================
// 🚀 CLUSTER-MODE UNTERSTÜTZUNG
// ===============================
if (CONFIG.ENABLE_CLUSTER && cluster.isMaster) {
    logger.info(`🚀 Starting ${CONFIG.CLUSTER_WORKERS} workers in cluster mode`);
    
    for (let i = 0; i < CONFIG.CLUSTER_WORKERS; i++) {
        cluster.fork();
    }
    
    cluster.on('exit', (worker, code, signal) => {
        logger.error(`Worker ${worker.process.pid} died with code ${code} and signal ${signal}`);
        logger.info('Starting a new worker...');
        cluster.fork();
    });
    
    // Master-Prozess für Cluster-Management
    return;
}

// ===============================
// 🌐 EXPRESS APP SETUP (ERWEITERT)
// ===============================
const app = express();
const adminApp = express();

// Basis-Middleware für beide Apps
[app, adminApp].forEach(application => {
    // Sicherheits-Headers
    application.use(helmet({
        contentSecurityPolicy: {
            directives: {
                defaultSrc: ["'self'"],
                styleSrc: ["'self'", "'unsafe-inline'"],
                scriptSrc: ["'self'"],
                imgSrc: ["'self'", "data:", "https:"],
            }
        },
        hsts: CONFIG.SECURE_MODE,
        noSniff: true,
        frameguard: { action: 'deny' }
    }));
    
    // CORS-Konfiguration
    application.use(cors({
        origin: (origin, callback) => {
            // Localhost und lokale IPs erlauben
            if (!origin || /^https?:\/\/(localhost|127\.0\.0\.1|192\.168\.|10\.|172\.16\.)/.test(origin)) {
                callback(null, true);
            } else {
                callback(new Error('Not allowed by CORS'));
            }
        },
        credentials: true,
        methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        allowedHeaders: ['Content-Type', 'Authorization', 'X-API-Key', 'X-Maintenance-Key']
    }));
    
    // Kompression
    application.use(compression({ level: CONFIG.COMPRESSION_LEVEL }));
    
    // Body Parser mit Limits
    application.use(express.json({ 
        limit: CONFIG.MAX_FILE_SIZE,
        verify: (req, res, buf) => {
            // Request-Body für Security-Checks verfügbar machen
            req.rawBody = buf;
        }
    }));
    application.use(express.urlencoded({ 
        extended: true, 
        limit: CONFIG.MAX_FILE_SIZE 
    }));
    
    // Erweiterte Sicherheits-Middleware
    application.use(securityMiddleware);
    
    // Request-Tracking
    application.use(trackingMiddleware);
    
    // Logging (falls aktiviert)
    if (CONFIG.ENABLE_LOGGING) {
        application.use(morgan('combined', {
            stream: {
                write: (message) => logger.info(message.trim())
            }
        }));
    }
});

// ===============================
// 📊 RATE LIMITING (ERWEITERT)
// ===============================
if (CONFIG.ENABLE_RATE_LIMITING) {
    const createRateLimit = (windowMs, max, message) => rateLimit({
        windowMs,
        max,
        message: { error: 'Rate limit exceeded', message },
        standardHeaders: true,
        legacyHeaders: false,
        keyGenerator: (req) => req.ip || 'anonymous',
        handler: (req, res) => {
            const clientIP = req.ip || 'unknown';
            logger.warn(`Rate limit exceeded for IP: ${clientIP}`);
            res.status(429).json({
                error: 'Rate limit exceeded',
                message: 'Too many requests, please try again later'
            });
        }
    });
    
    // Verschiedene Rate Limits für verschiedene Endpunkte
    app.use('/api/chat', createRateLimit(60000, 30, 'Too many chat requests'));
    app.use('/api/', createRateLimit(60000, CONFIG.MAX_REQUESTS_PER_MINUTE, 'Too many API requests'));
    app.use('/', createRateLimit(60000, CONFIG.MAX_REQUESTS_PER_MINUTE * 2, 'Too many requests'));
    
    // Strikte Limits für Admin-App
    adminApp.use('/', createRateLimit(60000, 20, 'Too many admin requests'));
}

// ===============================
// 🎯 HAUPTSERVER - ERWEITERTE ROUTEN
// ===============================

// JWT-Middleware auf API-Routen anwenden
app.use('/api', jwtMiddleware);

// Gesundheitscheck (öffentlich)
app.get('/health', (req, res) => {
    res.json({
        status: 'ok',
        timestamp: new Date().toISOString(),
        version: '2.0.0',
        uptime: Date.now() - metrics.startTime,
        server: 'OpenGazAI Enhanced'
    });
});

// Status-Endpunkt (öffentlich)
app.get('/status', (req, res) => {
    res.json({
        status: 'running',
        timestamp: new Date().toISOString(),
        config: {
            model: CONFIG.LLM_MODEL_NAME,
            secureMode: CONFIG.SECURE_MODE,
            rateLimiting: CONFIG.ENABLE_RATE_LIMITING,
            intrusionDetection: CONFIG.ENABLE_INTRUSION_DETECTION
        }
    });
});

// Metriken-Endpunkt (öffentlich, aber begrenzt)
app.get('/metrics', (req, res) => {
    const publicMetrics = {
        uptime: Date.now() - metrics.startTime,
        totalRequests: metrics.totalRequests,
        activeConnections: metrics.activeConnections,
        requestsPerSecond: metrics.requestsPerSecond,
        timestamp: new Date().toISOString()
    };
    res.json(publicMetrics);
});

// Token-Endpunkt für Authentifizierung
app.post('/auth/token', (req, res) => {
    try {
        const { username, password, apiKey } = req.body;
        
        // Einfache API-Key basierte Authentifizierung für Demo
        if (apiKey === CONFIG.API_KEY) {
            const token = jwt.sign({
                type: 'api',
                authenticated: true,
                tokenLimit: CONFIG.DEFAULT_TOKEN_LIMIT,
                tokensUsed: 0,
                iat: Math.floor(Date.now() / 1000),
                exp: Math.floor(Date.now() / 1000) + (24 * 60 * 60) // 24 Stunden
            }, CONFIG.JWT_SECRET);
            
            res.json({
                token,
                expiresIn: 86400,
                tokenLimit: CONFIG.DEFAULT_TOKEN_LIMIT
            });
        } else {
            res.status(401).json({
                error: 'Invalid credentials',
                message: 'API key is required'
            });
        }
    } catch (error) {
        logger.error('Token generation error:', error);
        res.status(500).json({
            error: 'Internal server error',
            message: 'Token generation failed'
        });
    }
});

// Ollama-Modelle abrufen
app.get('/api/models', async (req, res) => {
    try {
        const response = await fetch(`${CONFIG.OLLAMA_TARGET_URL}/api/tags`);
        if (!response.ok) {
            throw new Error(`Ollama API error: ${response.status}`);
        }
        
        const data = await response.json();
        res.json(data);
    } catch (error) {
        logger.error('Models fetch error:', error);
        res.status(502).json({
            error: 'Service unavailable',
            message: 'Unable to fetch models from Ollama'
        });
    }
});

// ===============================
// 🔄 OLLAMA PROXY (ERWEITERT)
// ===============================
const createOllamaProxy = () => {
    return createProxyMiddleware({
        target: CONFIG.OLLAMA_TARGET_URL,
        changeOrigin: true,
        timeout: CONFIG.REQUEST_TIMEOUT,
        proxyTimeout: CONFIG.REQUEST_TIMEOUT,
        
        onProxyReq: (proxyReq, req, res) => {
            // Request-Logging
            logger.info(`Proxying ${req.method} ${req.url} to Ollama`);
            
            // Token-Usage tracking
            if (req.user && req.user.tokenLimit) {
                req.user.tokensUsed = (req.user.tokensUsed || 0) + 1;
            }
            
            // Request-Modifikation für bessere Sicherheit
            proxyReq.setHeader('User-Agent', 'OpenGazAI-Proxy/2.0');
            proxyReq.setHeader('X-Forwarded-For', req.ip);
        },
        
        onProxyRes: (proxyRes, req, res) => {
            // Response-Logging
            logger.info(`Ollama responded with ${proxyRes.statusCode} for ${req.method} ${req.url}`);
            
            // Security Headers hinzufügen
            proxyRes.headers['X-Proxy-By'] = 'OpenGazAI';
            proxyRes.headers['X-Response-Time'] = Date.now() - req.startTime;
        },
        
        onError: (err, req, res) => {
            logger.error('Proxy error:', err);
            metrics.recordError('PROXY_ERROR');
            
            res.status(502).json({
                error: 'Bad Gateway',
                message: 'Ollama service is temporarily unavailable',
                timestamp: new Date().toISOString()
            });
        }
    });
};

// Ollama-Proxy auf API-Chat-Route
app.use('/api/chat', createOllamaProxy());
app.use('/api/generate', createOllamaProxy());
app.use('/api/pull', createOllamaProxy());
app.use('/api/push', createOllamaProxy());
app.use('/api/create', createOllamaProxy());
app.use('/api/copy', createOllamaProxy());
app.use('/api/delete', createOllamaProxy());

// ===============================
// 🎛️ ADMIN-APP ROUTEN (ERWEITERT)
// ===============================

// Admin-Authentifizierung
const adminAuth = (req, res, next) => {
    const maintenanceKey = req.headers['x-maintenance-key'];
    
    if (maintenanceKey !== CONFIG.MAINTENANCE_KEY) {
        return res.status(401).json({
            error: 'Unauthorized',
            message: 'Valid maintenance key required'
        });
    }
    
    next();
};

// Alle Admin-Routen erfordern Authentifizierung
adminApp.use('/', adminAuth);

// Admin-Status
adminApp.get('/status', (req, res) => {
    const fullMetrics = metrics.getMetrics();
    res.json({
        status: 'running',
        timestamp: new Date().toISOString(),
        system: {
            ...fullMetrics,
            config: CONFIG,
            nodeVersion: process.version,
            platform: process.platform,
            arch: process.arch
        }
    });
});

// System-Metriken (detailliert)
adminApp.get('/metrics', (req, res) => {
    res.json(metrics.getMetrics());
});

// Logs abrufen
adminApp.get('/logs', async (req, res) => {
    try {
        const { lines = 100, level = 'info' } = req.query;
        const logFile = path.join(CONFIG.LOG_PATH, 'combined.log');
        
        const content = await fs.readFile(logFile, 'utf8');
        const logLines = content.split('\n')
            .filter(line => line.trim())
            .slice(-parseInt(lines));
        
        res.json({
            logs: logLines,
            total: logLines.length,
            level
        });
    } catch (error) {
        logger.error('Log retrieval error:', error);
        res.status(500).json({
            error: 'Internal server error',
            message: 'Unable to retrieve logs'
        });
    }
});

// Konfiguration aktualisieren
adminApp.post('/config', (req, res) => {
    try {
        const { key, value } = req.body;
        
        if (key in CONFIG && typeof value !== 'undefined') {
            CONFIG[key] = value;
            logger.info(`Configuration updated: ${key} = ${value}`);
            
            res.json({
                success: true,
                message: `Configuration ${key} updated`,
                config: CONFIG
            });
        } else {
            res.status(400).json({
                error: 'Invalid configuration',
                message: 'Key not found or invalid value'
            });
        }
    } catch (error) {
        logger.error('Configuration update error:', error);
        res.status(500).json({
            error: 'Internal server error',
            message: 'Configuration update failed'
        });
    }
});

// System-Neustart
adminApp.post('/restart', (req, res) => {
    logger.info('System restart requested via admin interface');
    res.json({
        success: true,
        message: 'System restart initiated',
        timestamp: new Date().toISOString()
    });
    
    setTimeout(() => {
        process.exit(0);
    }, 2000);
});

// Graceful Shutdown
adminApp.post('/shutdown', (req, res) => {
    logger.info('Graceful shutdown requested via admin interface');
    res.json({
        success: true,
        message: 'Graceful shutdown initiated',
        timestamp: new Date().toISOString()
    });
    
    gracefulShutdown();
});

// Cache bereinigen
adminApp.post('/cache/clear', (req, res) => {
    try {
        // Metriken zurücksetzen
        metrics.resetIPCounters();
        
        // Garbage Collection forcieren
        if (global.gc) {
            global.gc();
        }
        
        logger.info('Cache cleared via admin interface');
        res.json({
            success: true,
            message: 'Cache cleared successfully',
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        logger.error('Cache clear error:', error);
        res.status(500).json({
            error: 'Internal server error',
            message: 'Cache clear failed'
        });
    }
});

// ===============================
// 🚀 SERVER-START (ERWEITERT)
// ===============================

// Fehler-Handler für unbehandelte Exceptions
process.on('uncaughtException', (error) => {
    logger.error('Uncaught Exception:', error);
    gracefulShutdown();
});

process.on('unhandledRejection', (reason, promise) => {
    logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

// Graceful Shutdown Handler
const gracefulShutdown = () => {
    logger.info('🛑 Graceful shutdown initiated...');
    
    // Server schließen
    if (server) {
        server.close(() => {
            logger.info('✅ Main server closed');
        });
    }
    
    if (adminServer) {
        adminServer.close(() => {
            logger.info('✅ Admin server closed');
        });
    }
    
    // Nach 10 Sekunden forciert beenden
    setTimeout(() => {
        logger.error('❌ Forced shutdown after timeout');
        process.exit(1);
    }, 10000);
};

// Signal-Handler für Graceful Shutdown
process.on('SIGTERM', gracefulShutdown);
process.on('SIGINT', gracefulShutdown);

// Server starten
let server, adminServer;

const startServers = async () => {
    try {
        // Verzeichnisse erstellen
        await fs.mkdir(CONFIG.DATA_PATH, { recursive: true });
        await fs.mkdir(CONFIG.LOG_PATH, { recursive: true });
        
        logger.info('🔥 MEGA ULTRA AI SERVER V2.0 STARTING 🔥');
        logger.info(`📊 Configuration loaded:`);
        logger.info(`  ├─ Port: ${CONFIG.PORT}`);
        logger.info(`  ├─ Admin Port: ${CONFIG.ADMIN_PORT}`);
        logger.info(`  ├─ Secure Mode: ${CONFIG.SECURE_MODE ? '✅' : '❌'}`);
        logger.info(`  ├─ Rate Limiting: ${CONFIG.ENABLE_RATE_LIMITING ? '✅' : '❌'}`);
        logger.info(`  ├─ Intrusion Detection: ${CONFIG.ENABLE_INTRUSION_DETECTION ? '✅' : '❌'}`);
        logger.info(`  ├─ Cluster Mode: ${CONFIG.ENABLE_CLUSTER ? '✅' : '❌'}`);
        logger.info(`  └─ Ollama Target: ${CONFIG.OLLAMA_TARGET_URL}`);
        
        // Hauptserver starten
        server = app.listen(CONFIG.PORT, '0.0.0.0', () => {
            logger.info(`🚀 Main server running on port ${CONFIG.PORT}`);
            logger.info(`🌐 API Base: http://localhost:${CONFIG.PORT}/api`);
        });
        
        // Admin-Server starten
        adminServer = adminApp.listen(CONFIG.ADMIN_PORT, '127.0.0.1', () => {
            logger.info(`🎛️  Admin server running on port ${CONFIG.ADMIN_PORT}`);
            logger.info(`🔧 Admin Panel: http://localhost:${CONFIG.ADMIN_PORT}`);
        });
        
        // Server-Timeouts setzen
        server.timeout = CONFIG.REQUEST_TIMEOUT;
        adminServer.timeout = CONFIG.REQUEST_TIMEOUT;
        
        logger.info('✅ MEGA ULTRA AI SERVER V2.0 SUCCESSFULLY STARTED!');
        logger.info('🎯 System ready for autonomous operation');
        
    } catch (error) {
        logger.error('❌ Server startup failed:', error);
        process.exit(1);
    }
};

// Server starten
startServers();

// Export für Testing
module.exports = { app, adminApp, CONFIG, metrics };