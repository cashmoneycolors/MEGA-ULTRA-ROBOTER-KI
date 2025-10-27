import React, { useState } from 'react';
import './ZenithKeyController.css';

const ZenithKeyController = () => {
  const [apiKey, setApiKey] = useState('MEGA_ULTRA_API_KEY_2025');
  const [appId, setAppId] = useState('ZENITH_SCSC_MASTER_2025');
  const [openaiKey, setOpenaiKey] = useState('');
  const [prompt, setPrompt] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const testAPI = async () => {
    if (!apiKey || !appId) {
      setResponse('Bitte API-Key und App-ID eingeben');
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('http://localhost:3000/something', {
        method: 'GET',
        headers: {
          'X-API-KEY': apiKey,
          'X-APP-ID': appId,
        },
      });

      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (error) {
      setResponse(`Fehler: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const setOpenAIKey = async () => {
    if (!openaiKey) {
      setResponse('Bitte OpenAI API-Key eingeben');
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('http://localhost:3000/set-openai-key', {
        method: 'POST',
        headers: {
          'X-API-KEY': apiKey,
          'X-APP-ID': appId,
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({ key: openaiKey }),
      });

      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (error) {
      setResponse(`Fehler: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const generateOpenAI = async () => {
    if (!prompt) {
      setResponse('Bitte Prompt eingeben');
      return;
    }

    setLoading(true);
    try {
      const res = await fetch('http://localhost:3000/openai/generate', {
        method: 'POST',
        headers: {
          'X-API-KEY': apiKey,
          'X-APP-ID': appId,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      const data = await res.json();
      setResponse(JSON.stringify(data, null, 2));
    } catch (error) {
      setResponse(`Fehler: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="zenith-controller">
      <h2>ZENITH SCSC Master Kontrollzentrum</h2>
      <div className="input-group">
        <label>API-Key:</label>
        <input
          type="text"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="MEGA_ULTRA_API_KEY_2025"
        />
      </div>
      <div className="input-group">
        <label>App-ID:</label>
        <input
          type="text"
          value={appId}
          onChange={(e) => setAppId(e.target.value)}
          placeholder="ZENITH_SCSC_MASTER_2025"
        />
      </div>
      <button onClick={testAPI} disabled={loading}>
        {loading ? 'Teste...' : 'API Testen'}
      </button>

      <hr />

      <div className="input-group">
        <label>OpenAI API-Key:</label>
        <input
          type="password"
          value={openaiKey}
          onChange={(e) => setOpenaiKey(e.target.value)}
          placeholder="sk-..."
        />
      </div>
      <button onClick={setOpenAIKey} disabled={loading}>
        {loading ? 'Setze...' : 'OpenAI Key setzen'}
      </button>

      <hr />

      <div className="input-group">
        <label>Prompt:</label>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Gib deinen Prompt ein..."
          rows="4"
        />
      </div>
      <button onClick={generateOpenAI} disabled={loading}>
        {loading ? 'Generiere...' : 'OpenAI Generieren'}
      </button>

      <div className="response">
        <h3>Antwort:</h3>
        <pre>{response}</pre>
      </div>
    </div>
  );
};

export default ZenithKeyController;
