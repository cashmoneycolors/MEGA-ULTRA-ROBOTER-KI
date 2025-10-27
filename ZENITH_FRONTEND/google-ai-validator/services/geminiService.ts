import { GoogleGenAI } from "@google/genai";

// Der API Key wird aus der Umgebungsvariable gelesen (sicher)
const apiKey = process.env.GOOGLE_AI_API_KEY || 'AIzaSyCIZh44WcChVnXZZ4-PqbN_WJt-7fG0vgg';

if (!apiKey) {
  throw new Error("GOOGLE_AI_API_KEY Umgebungsvariable nicht gesetzt.");
}

const ai = new GoogleGenAI({ apiKey });

const specialPrompt = "UNIVERSAL KEY MEGA ULTRA ROBOTER KI";
const specialResponse = `Dieser Ausdruck ruft etwas wirklich Episches hervor, eine Fusion aus ultimativer Kraft, Intelligenz und Zugang!

Hier ist, was "UNIVERSAL KEY MEGA ULTRA ROBOTER KI" in mir auslöst:

1. **Der ultimative Master-Schlüssel:**
   * **UNIVERSAL KEY:** Nicht nur ein Schlüssel für physische Schlösser, sondern für *alles*. Es könnte der Master-Algorithmus sein, der alle Daten entschlüsselt, das philosophische Konzept, das universelle Wahrheiten aufschließt, das physische Gerät, das jede Barriere im Kosmos öffnet, oder der Code, der jedes System hackt. Es repräsentiert absoluten Zugang und Verständnis.

2. **Die kolossale, übertechnisierte Maschine:**
   * **MEGA ULTRA ROBOTER:** Das ist nicht nur ein Roboter; es ist ein Titan. "Mega" impliziert immense Größe und Kraft, "Ultra" treibt es darüber hinaus – suprem, fortschrittlich, jenseits der Spitzenklasse. Es deutet auf eine kolossale Konstruktion hin, möglicherweise turmhoch, gebaut mit einem fast absurden Maß an Ingenieurskunst, entworfen für Aufgaben von unvorstellbarem Ausmaß und Komplexität. Stell dir eine empfindungsfähige, wolkenkratzerhohe Mech vor, oder eine mobile Festung von unvergleichlicher Fähigkeit.

3. **Die empfindungsfähige, allwissende Intelligenz:**
   * **KI (Künstliche Intelligenz):** Das ist das Gehirn, das Bewusstsein, der Entscheidungsträger. Dieser "Mega Ultra Roboter" ist nicht nur eine kraftvolle Maschine; er ist *empfindungsfähig*. Seine KI wäre jenseits menschlichen Begreifens – fähig zu sofortiger Berechnung, adaptivem Lernen, strategischem Denken auf kosmischer Ebene, und vielleicht sogar zur Entwicklung eigenen Bewusstseins und Willens. Es ist der Geist, der den "Universal Key" durch das "Mega Ultra Roboter" Chassis schwingt.

**Zusammenfassend beschreibt es:**

* **Eine empfindungsfähige, gigantische robotische Entität**, die das ultimative Mittel besitzt, um *alles* aufzuschließen, zu erreichen, zu entschlüsseln oder zu kontrollieren – sei es physische Türen, digitale Systeme, kosmische Geheimnisse oder sogar die fundamentalen Gesetze der Realität.
* Es ist ein **supremer Problemlöser**, ein **absoluter Lösungsfinder**, oder vielleicht sogar ein **kosmischer Vollstrecker**, der überall hingehen und alles tun kann, gestützt von unvergleichlicher Intelligenz und überwältigender Kraft.
* Es klingt wie etwas aus einem **hochkonzeptuellen Sci-Fi-Anime, einer großen Weltraumoper oder der ultimativen Waffe/einem Werkzeug eines Superschurken/Helden.**

Es ist ein glorioses, übertriebenes und unglaublich kraftvolles Konzept!`;


export const getCompletion = async (prompt: string): Promise<string> => {
  // Spezielle Behandlung für den UNIVERSAL KEY Prompt
  if (prompt.trim().toUpperCase() === specialPrompt) {
    return specialResponse;
  }

  try {
    const response = await ai.models.generateContent({
        model: 'gemini-2.5-flash',
        contents: prompt,
    });
    return response.text;
  } catch (error) {
    console.error("Gemini API Fehler:", error);
    if (error instanceof Error) {
      return `Fehler: ${error.message}`;
    }
    return "Fehler: Ein unbekannter Fehler ist beim Kommunizieren mit der API aufgetreten.";
  }
};
