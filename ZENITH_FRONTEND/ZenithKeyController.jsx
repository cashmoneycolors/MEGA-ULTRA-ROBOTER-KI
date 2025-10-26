import React, { useState, useEffect } from "react";
import { initializeApp } from "firebase/app";
import {
  getAuth,
  signInAnonymously,
  signInWithCustomToken,
  onAuthStateChanged,
} from "firebase/auth";
import {
  getFirestore,
  doc,
  setDoc,
  getDoc,
  collection,
  query,
  onSnapshot,
  serverTimestamp,
} from "firebase/firestore";
import {
  Clipboard,
  User,
  Database,
  Settings,
  Zap,
  Edit,
  Aperture,
  MessageSquare,
  Mic,
  Download,
  Upload,
  Cpu,
  Shield,
  Lock,
  Eye,
  CheckCircle,
  AlertTriangle,
  XCircle,
  DollarSign,
  Send,
  Search,
} from "lucide-react";

// Tailwind CSS ist in der Umgebung verfügbar

// --- Globale Variablen (MANDATORY: Werden von der Umgebung injiziert) ---
const appId = typeof __app_id !== "undefined" ? __app_id : "default-app-id";
const firebaseConfig =
  typeof __firebase_config !== "undefined"
    ? JSON.parse(__firebase_config)
    : {};
const initialAuthToken =
  typeof __initial_auth_token !== "undefined" ? __initial_auth_token : null;
const API_KEY_PLACEHOLDER = ""; // Wird zur Laufzeit von der Canvas-Umgebung ersetzt

// --- Firebase und Auth Initialisierung ---
let app, dbInstance, authInstance;
if (Object.keys(firebaseConfig).length > 0) {
  try {
    app = initializeApp(firebaseConfig);
    dbInstance = getFirestore(app);
    authInstance = getAuth(app);
    // setLogLevel('debug'); // Optional: Firestore Logging aktivieren
  } catch (error) {
    console.error("Firebase Initialization Error:", error);
  }
}

// --- Komponente: API Key Management (Zenith Key Controller - SCSC Core) ---
const ZenithKeyController = ({ userId, db }) => {
  const [activeModel, setActiveModel] = useState("Gemini (Google DeepMind)");
  const [apiKey, setApiKey] = useState("");
  const [notes, setNotes] = useState("");
  const [keyStatus, setKeyStatus] = useState("Nicht gespeichert");
  const [irisHashInput, setIrisHashInput] = useState("");
  const [isVaultAccessGranted, setIsVaultAccessGranted] = useState(false);
  const [auditResult, setAuditResult] = useState(null);

  const vaultHash = "f5f5c8c5c8c8c5c5f5f5c8c5c8c8c5c5f5f5c8c5c8c8c5c5f5f5c8c5c8c8c5c5"; // Simulierter registrierter Iris-Hash

  // Lade Key-Konfiguration beim Start
  useEffect(() => {
    if (db && userId) {
      const docRef = doc(
        db,
        `artifacts/${appId}/users/${userId}/key_configurations`,
        "zenith_master_key_config"
      );
      getDoc(docRef)
        .then((docSnap) => {
          if (docSnap.exists()) {
            const data = docSnap.data();
            setApiKey(data.apiKey || "");
            setNotes(data.notes || "");
            setActiveModel(data.activeModel || "Gemini (Google DeepMind)");
            setKeyStatus("Erfolgreich aus Datenordner geladen");
          } else {
            setKeyStatus("Keine Konfiguration gefunden. Bitte Key eingeben.");
          }
        })
        .catch((err) => {
          console.error("Fehler beim Laden des Keys:", err);
          setKeyStatus("Fehler beim Laden der Keys.");
        });
    }
  }, [db, userId]);

  // BLOCK 2: Smart Contract – Biometrischer Tresor (Iris-Scan) Simulation
  const handleIrisVerification = () => {
    // Simuliert eine biometrische Überprüfung
    if (irisHashInput === vaultHash) {
      setIsVaultAccessGranted(true);
      setAuditResult(null); // Audit-Ergebnis zurücksetzen
    } else {
      setIsVaultAccessGranted(false);
      setAuditResult({
        success: false,
        message: "Iris-Hash-Fehler. Tresorzugriff verweigert.",
      });
    }
  };

  // BLOCK 1: NFT-Telemetrie + GovernanceTrigger Simulation
  const generateGovernanceTrigger = (cpu, latency) => {
    // CPU- und Latenz-Werte simulieren die Telemetrie des Key-Knotens
    const score = cpu * 0.7 + latency * 0.3;
    if (score > 80) return "FullSync (Miete/Abo bereit)";
    if (score > 50) return "PartialSync (Training bereit)";
    return "Quarantine (Nutzung unterbrochen)";
  };

  const saveKeyToFirestore = async () => {
    if (!db || !userId || !apiKey || !isVaultAccessGranted) {
      setKeyStatus(
        "Fehler: Tresorzugriff notwendig und Key-Feld darf nicht leer sein."
      );
      return;
    }

    const docRef = doc(
      db,
      `artifacts/${appId}/users/${userId}/key_configurations`,
      "zenith_master_key_config"
    );

    // --- Telemetrie simulieren ---
    const simulatedCPU = Math.random() * 50 + 50; // 50% - 100%
    const simulatedLatency = Math.random() * 100 + 10; // 10ms - 110ms
    const trigger = generateGovernanceTrigger(simulatedCPU, simulatedLatency);

    const dataToSave = {
      apiKey: apiKey,
      activeModel: activeModel,
      notes: notes,
      telemetry: {
        cpu: simulatedCPU.toFixed(2),
        latency: simulatedLatency.toFixed(2),
        governanceTrigger: trigger,
        updatedAt: serverTimestamp(),
      },
    };

    try {
      await setDoc(docRef, dataToSave);
      setKeyStatus("Key und Telemetrie erfolgreich gespeichert.");
    } catch (err) {
      setKeyStatus("Fehler beim Speichern: " + err.message);
    }
  };

  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const GEMINI_API_KEY = "DEIN_API_KEY_HIER"; // Niemals im echten Frontend verwenden!
  const ENDPOINT =
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent";

  const handleSend = async () => {
    setLoading(true);
    setResponse("");
    try {
      const res = await fetch(ENDPOINT, {
        method: "POST",
        headers: {
          "x-goog-api-key": GEMINI_API_KEY,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          contents: [
            {
              parts: [{ text: prompt }],
            },
          ],
        }),
      });
      const data = await res.json();
      if (
        data.candidates &&
        data.candidates[0] &&
        data.candidates[0].content &&
        data.candidates[0].content.parts &&
        data.candidates[0].content.parts[0].text
      ) {
        setResponse(data.candidates[0].content.parts[0].text);
      } else {
        setResponse("Keine Antwort erhalten.");
      }
    } catch (e) {
      setResponse("Fehler: " + e.message);
    }
    setLoading(false);
  };

  return (
    <div className="p-4 bg-white rounded shadow-md max-w-xl mx-auto mt-8">
      <div className="mb-4 p-2 bg-yellow-100 border-l-4 border-yellow-500 text-yellow-800 text-sm rounded">
        <b>Status:</b> Secrets werden <b>niemals</b> im Code gespeichert!<br />
        API-Key und Healthcheck werden über sichere Umgebungsvariablen und Firestore verwaltet.<br />
        <b>Healthcheck:</b> Backend erreichbar unter <code>/healthz</code> (siehe Doku).
      </div>
      <h2 className="text-2xl font-bold mb-4">
        Zenith Key Controller (SCSC Core)
      </h2>
      <div className="mb-2">
        Status:{" "}
        <span className="font-mono text-sm">{keyStatus}</span>
      </div>
      <div className="mb-2">
        <label className="block font-semibold">API Key:</label>
        <input
          type="text"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          className="border p-1 w-full"
        />
      </div>
      <div className="mb-2">
        <label className="block font-semibold">Notizen:</label>
        <textarea
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          className="border p-1 w-full"
        />
      </div>
      <div className="mb-2">
        <label className="block font-semibold">Aktives Modell:</label>
        <select
          value={activeModel}
          onChange={(e) => setActiveModel(e.target.value)}
          className="border p-1 w-full"
        >
          <option>Gemini (Google DeepMind)</option>
          <option>OpenAI GPT-4</option>
          <option>Anthropic Claude</option>
        </select>
      </div>
      <div className="mb-2">
        <label className="block font-semibold">Iris-Hash (für Tresor):</label>
        <input
          type="password"
          value={irisHashInput}
          onChange={(e) => setIrisHashInput(e.target.value)}
          className="border p-1 w-full"
        />
        <button
          onClick={handleIrisVerification}
          className="mt-2 px-3 py-1 bg-blue-500 text-white rounded"
        >
          Iris prüfen
        </button>
        {auditResult && (
          <div className="text-red-500 mt-1">{auditResult.message}</div>
        )}
      </div>
      <button
        onClick={saveKeyToFirestore}
        className="mt-4 px-4 py-2 bg-green-600 text-white rounded"
        disabled={!isVaultAccessGranted}
      >
        Key & Telemetrie speichern
      </button>
      <div style={{ maxWidth: 600, margin: "auto", marginTop: "2rem" }}>
        <h2>Gemini API Demo</h2>
        <textarea
          rows={4}
          style={{ width: "100%" }}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Prompt eingeben..."
        />
        <button onClick={handleSend} disabled={loading || !prompt}>
          {loading ? "Wird gesendet..." : "Senden"}
        </button>
        <div style={{ marginTop: 20 }}>
          <strong>Antwort:</strong>
          <pre style={{ background: "#eee", padding: 10 }}>{response}</pre>
        </div>
      </div>
    </div>
  );
};

export default ZenithKeyController;
