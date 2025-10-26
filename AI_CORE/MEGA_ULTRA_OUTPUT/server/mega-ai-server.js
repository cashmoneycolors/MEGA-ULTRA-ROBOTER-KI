// mega-ai-server.js - MEGA ULTRA NODE.JS PROXY (MAX RESILIENZ & ÖKONOMIE)
// Erstellt: 03. Oktober 2025
// MAXIMALE STUFE: Ökonomische Autonomie und Dynamische Skalierung

const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const { spawn } = require('child_process');
const crypto = require('crypto');
const jwt = require('jsonwebtoken');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs');
const Database = require('better-sqlite3');
const path = require('path');

// ===============================
// 🎯 MAXIMALE KONFIGURATION
// ===============================

// Kommandozeilenargumente
const argv = yargs(hideBin(process.argv)).argv;

// KRITISCHE SECRETS aus Umgebung (vom C#-Integrator gesetzt)
const JWT_SECRET = process.env.JWT_SECRET || argv['jwt-secret'];
const MAINTENANCE_KEY = process.env.MAINTENANCE_KEY || argv['maintenance-key'];

if (!JWT_SECRET || !MAINTENANCE_KEY) {
    console.error("[FATAL] KRITISCH: JWT_SECRET und MAINTENANCE_KEY müssen als Umgebungsvariablen gesetzt sein.");
    process.exit(1);
}

// ÖKONOMISCHE AUTONOMIE - Konfiguration
const CONFIG = {
    port: argv.port || 3000,
    dataPath: process.env.DATA_PATH || argv.datapath || './data',
    ollamaUrl: process.env.OLLAMA_TARGET_URL || argv['ollama-url'] || 'http://localhost:11434',
    
    // Ökonomische Parameter (vom C#-Integrator gesteuert)
    defaultTokenLimit: parseInt(process.env.DEFAULT_TOKEN_LIMIT || argv['token-limit'] || '1000000', 10),
    maxRateLimitFactor: parseInt(process.env.MAX_RATE_LIMIT_FACTOR || argv['rate-limit'] || '60', 10),
    
    // System-Parameter
    jwtSecret: JWT_SECRET,
    maintenanceKey: MAINTENANCE_KEY,
};

console.log(`[INFO] MEGA ULTRA PROXY KONFIGURATION:`);
console.log(`  Port: ${CONFIG.port}`);
console.log(`  Token Limit: ${CONFIG.defaultTokenLimit.toLocaleString()}`);
console.log(`  Rate Factor: ${CONFIG.maxRateLimitFactor}`);
console.log(`  Ollama URL: ${CONFIG.ollamaUrl}`);

// ===============================
// 🛡️ SICHERHEITS-UTILITIES
// ===============================

function createHashFromPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex').toLowerCase();
}

function verifyAdminPassword(inputPassword, storedHash) {
    return createHashFromPassword(inputPassword) === storedHash;
}

// Verbesserte Token-Schätzung
const estimateTokens = (text) => {
    if (!text || text.length === 0) return 0;
    
    const charEstimate = text.length * 0.25;
    const wordCount = text.trim().split(/\s+/).length;
    const wordEstimate = wordCount * 1.33;
    
    return Math.ceil(Math.max(charEstimate, wordEstimate));
};

// ===============================
// 🗄️ MAXIMALER USAGE MANAGER
// ===============================

class MaximalUsageManager {
    constructor(dataPath, defaultLimit) {
        this.dbPath = path.join(dataPath, 'mega_usage.db');
        this.defaultLimit = defaultLimit;
        this.usageQueue = [];
        this.isProcessing = false;
        
        // Stelle sicher, dass der Datenpfad existiert
        if (!require('fs').existsSync(dataPath)) {
            require('fs').mkdirSync(dataPath, { recursive: true });
        }
        
        this.db = new Database(this.dbPath);
        this.initDb();
        
        console.log(`[INFO] Database: ${this.dbPath}`);
        console.log(`[INFO] Default Token Limit: ${defaultLimit.toLocaleString()}`);
    }

    initDb() {
        // Erweiterte Tabelle für maximale Funktionalität
        this.db.exec(`
            CREATE TABLE IF NOT EXISTS user_usage (
                api_key TEXT PRIMARY KEY,
                monthly_limit INTEGER NOT NULL,
                current_tokens INTEGER NOT NULL,
                last_update INTEGER NOT NULL,
                tier TEXT DEFAULT 'standard',
                created_at INTEGER DEFAULT ${Date.now()}
            );
            
            CREATE INDEX IF NOT EXISTS idx_last_update ON user_usage(last_update);
            CREATE INDEX IF NOT EXISTS idx_tier ON user_usage(tier);
        `);
        
        console.log("[INFO] Datenbank initialisiert mit erweiterten Features.");
    }
    
    // SYNCHRONE PRÜFUNG (Middleware)
    checkLimit(apiKey) {
        const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000;
        
        let user = this.db.prepare(`
            SELECT monthly_limit, current_tokens, last_update, tier 
            FROM user_usage WHERE api_key = ?
        `).get(apiKey);
        
        if (!user) {
            // Neuer User mit Default-Limit
            this.db.prepare(`
                INSERT INTO user_usage (api_key, monthly_limit, current_tokens, last_update, tier, created_at) 
                VALUES (?, ?, ?, ?, ?, ?)
            `).run(apiKey, this.defaultLimit, 0, Date.now(), 'standard', Date.now());
            
            user = { 
                monthly_limit: this.defaultLimit, 
                current_tokens: 0, 
                last_update: Date.now(),
                tier: 'standard'
            };
        }
        
        // Automatischer Monats-Reset
        if (user.last_update < thirtyDaysAgo) {
            this.db.prepare(`
                UPDATE user_usage 
                SET current_tokens = 0, last_update = ? 
                WHERE api_key = ?
            `).run(Date.now(), apiKey);
            user.current_tokens = 0;
        }

        return {
            allowed: user.current_tokens < user.monthly_limit,
            remaining: user.monthly_limit - user.current_tokens,
            tier: user.tier || 'standard',
            limit: user.monthly_limit
        };
    }
    
    // ASYNCHRONES LOGGING (Maximale Resilienz)
    addUsage(apiKey, tokensUsed, type = 'completion') {
        this.usageQueue.push({ 
            apiKey, 
            tokensUsed, 
            type,
            timestamp: Date.now()
        });
        
        if (!this.isProcessing) {
            setImmediate(() => this.processQueue());
        }
    }
    
    // MAXIMAL RESILIENTE QUEUE-VERARBEITUNG
    processQueue() {
        if (this.isProcessing || this.usageQueue.length === 0) return;

        this.isProcessing = true;
        const job = this.usageQueue.shift();
        
        try {
            const stmt = this.db.prepare(`
                UPDATE user_usage 
                SET current_tokens = current_tokens + ?, last_update = ? 
                WHERE api_key = ?
            `);
            
            const result = stmt.run(job.tokensUsed, Date.now(), job.apiKey);
            
            if (result.changes === 0) {
                // Fallback: User existiert nicht mehr
                this.db.prepare(`
                    INSERT OR REPLACE INTO user_usage 
                    (api_key, monthly_limit, current_tokens, last_update, tier, created_at) 
                    VALUES (?, ?, ?, ?, ?, ?)
                `).run(job.apiKey, this.defaultLimit, job.tokensUsed, Date.now(), 'standard', Date.now());
            }

        } catch (error) {
            // MAXIMAL RESILIENTE FEHLERBEHANDLUNG
            console.error(`[FATAL_DB_WRITE] Kritischer DB-Fehler für ${job.apiKey}: ${error.message}. Job verworfen.`);
            
        } finally {
            this.isProcessing = false;
            // Sofortige Fortsetzung für maximale Performance
            setImmediate(() => this.processQueue());
        }
    }
    
    // Sauberes Schließen der DB
    closeDb() {
        try {
            if (this.db) {
                this.db.close();
                console.log("[INFO] SQLite-Datenbankverbindung sauber geschlossen.");
            }
        } catch (e) {
            console.error("[ERROR] Fehler beim Schließen der Datenbank:", e.message);
        }
    }
    
    // Statistiken für Monitoring
    getStats() {
        try {
            const stats = this.db.prepare(`
                SELECT 
                    COUNT(*) as total_users,
                    SUM(current_tokens) as total_tokens_used,
                    AVG(current_tokens) as avg_tokens_per_user,
                    COUNT(CASE WHEN tier = 'premium' THEN 1 END) as premium_users
                FROM user_usage
            `).get();
            
            return stats;
        } catch (error) {
            console.error("[ERROR] Statistik-Fehler:", error.message);
            return null;
        }
    }
}

// ===============================
// 🚀 INITIALISIERUNG
// ===============================

const proxyApp = express();
const adminApp = express();

proxyApp.use(bodyParser.json({ limit: '10mb' }));
adminApp.use(bodyParser.json());

// Usage Manager mit ökonomischen Parametern
const usageManager = new MaximalUsageManager(CONFIG.dataPath, CONFIG.defaultTokenLimit);

// ===============================
// 🛡️ MIDDLEWARES (MAXIMALE SICHERHEIT)
// ===============================

// Rate Limiting mit dynamischen Parametern
const rateLimitStore = new Map();
const RATE_LIMIT_WINDOW_MS = 60 * 1000;
const MAX_REQUESTS_PER_WINDOW = CONFIG.maxRateLimitFactor; // Vom C#-Integrator gesteuert

const rateLimitMiddleware = (req, res, next) => {
    const apiKey = req.headers['authorization']?.split(' ')[1] || "ANONYMOUS";
    req.apiKey = apiKey;

    const now = Date.now();
    let record = rateLimitStore.get(apiKey);

    if (!record || record.resetTime < now) {
        record = { count: 1, resetTime: now + RATE_LIMIT_WINDOW_MS };
        rateLimitStore.set(apiKey, record);
    } else {
        record.count++;
        if (record.count > MAX_REQUESTS_PER_WINDOW) {
            const timeRemaining = Math.ceil((record.resetTime - now) / 1000);
            res.setHeader('Retry-After', timeRemaining);
            return res.status(429).json({ 
                error: "Too Many Requests", 
                message: `Rate limit of ${MAX_REQUESTS_PER_WINDOW} requests per minute exceeded.`,
                retry_after: timeRemaining
            });
        }
    }
    
    res.setHeader('X-RateLimit-Limit', MAX_REQUESTS_PER_WINDOW);
    res.setHeader('X-RateLimit-Remaining', MAX_REQUESTS_PER_WINDOW - record.count);
    next();
};

// MAXIMALER TOKEN LIMIT CHECK
const maximalTokenLimitCheck = (req, res, next) => {
    const apiKey = req.apiKey;
    
    if (!apiKey || apiKey === "ANONYMOUS") {
        return res.status(401).json({ 
            error: "Unauthorized", 
            message: "Valid API key required in Authorization header." 
        });
    }
    
    const { allowed, remaining, tier, limit } = usageManager.checkLimit(apiKey);

    if (!allowed) {
        res.setHeader('X-Token-Remaining', 0);
        res.setHeader('X-Token-Limit', limit);
        return res.status(429).json({ 
            error: "Token Limit Exceeded", 
            message: `Monthly token limit of ${limit.toLocaleString()} exceeded.`,
            tier: tier
        });
    }
    
    // Vernetzung: Token-Info in Headers
    res.setHeader('X-Token-Remaining', remaining);
    res.setHeader('X-Token-Limit', limit);
    res.setHeader('X-User-Tier', tier);
    
    next();
};

// JWT AUTHENTIFIZIERUNG für Admin Hub
const adminAuthMiddleware = (req, res, next) => {
    const authHeader = req.headers['authorization'];
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ 
            error: "Access denied", 
            message: "No token provided or malformed authorization header." 
        });
    }

    const token = authHeader.split(' ')[1];

    try {
        const decoded = jwt.verify(token, CONFIG.jwtSecret);
        req.user = decoded;
        next();
    } catch (ex) {
        return res.status(403).json({ 
            error: "Invalid token", 
            message: "Token validation failed or expired." 
        });
    }
};

// Maintenance Key Middleware
const maintenanceKeyMiddleware = (req, res, next) => {
    const key = req.headers['x-maintenance-key'];
    
    if (key === CONFIG.maintenanceKey) {
        next();
    } else {
        res.status(401).json({ 
            error: "Unauthorized access", 
            message: "Invalid maintenance key." 
        });
    }
};

// ===============================
// 🌐 PROXY ENDPOINTS
// ===============================

// Middleware anwenden
proxyApp.use(rateLimitMiddleware);
proxyApp.use(maximalTokenLimitCheck);

// Status-Endpoint (für C#-Integrator)
proxyApp.get('/status', (req, res) => {
    const stats = usageManager.getStats();
    
    res.status(200).json({ 
        status: 'ready', 
        port: CONFIG.port, 
        system: 'MEGA ULTRA PROXY',
        version: '3.0.0',
        config: {
            defaultTokenLimit: CONFIG.defaultTokenLimit,
            maxRateLimitFactor: CONFIG.maxRateLimitFactor
        },
        stats: stats
    });
});

// MAXIMALES CHAT COMPLETIONS (Streaming & Logging)
proxyApp.post('/v1/chat/completions', async (req, res) => {
    try {
        const inputPrompt = JSON.stringify(req.body.messages || []);
        const inputTokens = estimateTokens(inputPrompt);
        
        let outputData = '';
        
        // Ollama-Anfrage mit verbesserter Fehlerbehandlung
        const ollamaResponse = await axios.post(`${CONFIG.ollamaUrl}/api/generate`, {
            model: req.body.model || 'llama3.2:3b',
            prompt: inputPrompt,
            stream: req.body.stream !== false
        }, { 
            responseType: 'stream',
            timeout: 300000 // 5 Minuten Timeout
        });
        
        // Stream-Verarbeitung
        ollamaResponse.data.on('data', (chunk) => {
            const chunkStr = chunk.toString('utf8');
            outputData += chunkStr;
            res.write(chunk);
        });

        ollamaResponse.data.on('end', () => {
            res.end();
            
            // ASYNCHRONES LOGGING mit verbesserter Token-Zählung
            const outputTokens = estimateTokens(outputData);
            const totalTokensUsed = inputTokens + outputTokens;

            usageManager.addUsage(req.apiKey, totalTokensUsed, 'completion');
            
            console.log(`[USAGE] ${req.apiKey.substring(0, 8)}... - Total: ${totalTokensUsed} tokens (In: ${inputTokens}, Out: ${outputTokens})`);
        });

        ollamaResponse.data.on('error', (err) => {
            console.error(`[ERROR] Stream error: ${err.message}`);
            if (!res.headersSent) {
                res.status(500).json({ 
                    error: "Streaming error", 
                    message: "Error during response streaming." 
                });
            }
        });

    } catch (error) {
        console.error(`[ERROR] Ollama communication error: ${error.message}`);
        
        if (error.code === 'ECONNREFUSED') {
            return res.status(503).json({ 
                error: "Service Unavailable", 
                message: "LLM service is not available. Please try again later." 
            });
        }
        
        res.status(500).json({ 
            error: "Internal Server Error", 
            message: "Failed to process completion request." 
        });
    }
});

// Embeddings Endpoint
proxyApp.post('/v1/embeddings', async (req, res) => {
    try {
        const ollamaResponse = await axios.post(`${CONFIG.ollamaUrl}/api/embeddings`, {
            model: req.body.model || 'llama3.2:3b',
            prompt: req.body.input
        });
        
        const tokensUsed = estimateTokens(req.body.input || '');
        usageManager.addUsage(req.apiKey, tokensUsed, 'embedding');

        res.json(ollamaResponse.data);
        
    } catch (error) {
        console.error(`[ERROR] Embedding error: ${error.message}`);
        res.status(500).json({ 
            error: "Embedding error", 
            message: "Failed to generate embeddings." 
        });
    }
});

// ===============================
// 🎛️ ADMIN HUB
// ===============================

// Login Endpoint (Token-Ausgabe)
adminApp.post('/login', (req, res) => {
    const { password } = req.body;
    
    if (!password) {
        return res.status(400).json({ 
            error: "Bad Request", 
            message: "Password is required." 
        });
    }

    // Für Demo-Zwecke - in Produktion würde hier die echte Passwort-Prüfung erfolgen
    const adminHash = process.env.ADMIN_HASH || argv['admin-hash'] || createHashFromPassword('admin123');
    
    if (!verifyAdminPassword(password, adminHash)) {
        return res.status(401).json({ 
            error: "Invalid credentials", 
            message: "Authentication failed." 
        });
    }

    const token = jwt.sign(
        { 
            role: 'admin', 
            iat: Math.floor(Date.now() / 1000),
            exp: Math.floor(Date.now() / 1000) + (12 * 60 * 60) // 12 Stunden
        }, 
        CONFIG.jwtSecret
    );

    res.json({ 
        token: token,
        expires_in: '12h',
        message: "Authentication successful." 
    });
});

// Maintenance Shutdown (Sauberer Stopp)
adminApp.post('/maintenance/shutdown', maintenanceKeyMiddleware, (req, res) => {
    console.log("[CRITICAL] Received clean shutdown signal from C# Host.");
    
    res.json({ 
        success: true, 
        message: "Initiating graceful shutdown..." 
    });
    
    setTimeout(() => {
        usageManager.closeDb();
        process.exit(0);
    }, 1000);
});

// Sichere Admin-Routen
adminApp.use('/api', adminAuthMiddleware);

// Model Pull Endpoint
adminApp.post('/api/pull-model', (req, res) => {
    const { modelName } = req.body;
    
    if (!modelName) {
        return res.status(400).json({ 
            error: "Bad Request", 
            message: "Model name is required." 
        });
    }

    res.json({ 
        success: true, 
        message: `Pull operation for '${modelName}' started in background.` 
    });

    try {
        const pullProcess = spawn('ollama', ['pull', modelName], {
            detached: true,
            stdio: 'ignore'
        });
        pullProcess.unref();
        
        console.log(`[ADMIN] Model pull started: ${modelName}`);
    } catch (error) {
        console.error(`[ERROR] Failed to start model pull: ${error.message}`);
    }
});

// System Statistics
adminApp.get('/api/stats', (req, res) => {
    const stats = usageManager.getStats();
    const systemStats = {
        ...stats,
        uptime: process.uptime(),
        memory: process.memoryUsage(),
        nodeVersion: process.version,
        platform: process.platform
    };
    
    res.json(systemStats);
});

// ===============================
// 🚀 SERVER START
// ===============================

const PROXY_PORT = CONFIG.port;
const ADMIN_PORT = CONFIG.port + 1;

try {
    // Proxy Server
    const proxyServer = proxyApp.listen(PROXY_PORT, () => {
        console.log(`[SUCCESS] 🚀 MEGA ULTRA PROXY running on port ${PROXY_PORT}`);
    });
    
    // Admin Hub
    const adminServer = adminApp.listen(ADMIN_PORT, () => {
        console.log(`[SUCCESS] 🎛️ Admin Hub running on port ${ADMIN_PORT}`);
    });
    
    // Graceful Shutdown Handler
    process.on('SIGINT', () => {
        console.log('\n[INFO] Shutting down gracefully...');
        
        proxyServer.close(() => {
            console.log('[INFO] Proxy server closed.');
        });
        
        adminServer.close(() => {
            console.log('[INFO] Admin server closed.');
        });
        
        usageManager.closeDb();
        process.exit(0);
    });
    
    console.log(`[INFO] 🔥 MEGA ULTRA SYSTEM ready for maximum performance! 🔥`);
    
} catch (e) {
    console.error(`[FATAL] Server konnte nicht starten: ${e.message}`);
    process.exit(11);
}