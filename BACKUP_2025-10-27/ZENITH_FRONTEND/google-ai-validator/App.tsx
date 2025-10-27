import React, { useState, useCallback } from 'react';
import { getCompletion } from './services/geminiService';
import PromptInput from './components/PromptInput';
import ResponseDisplay from './components/ResponseDisplay';
import ApiKeyInfo from './components/ApiKeyInfo';
import { KeyIcon } from './components/icons';

const App: React.FC = () => {
  const [prompt, setPrompt] = useState<string>('');
  const [response, setResponse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleGenerate = useCallback(async () => {
    if (!prompt.trim()) {
      setError('Bitte gib eine Anfrage ein.');
      return;
    }

    setIsLoading(true);
    setError('');
    setResponse('');

    try {
      const result = await getCompletion(prompt);
      if (result.startsWith('Error')) {
        setError(result);
        setResponse('');
      } else {
        setResponse(result);
        setError('');
      }
    } catch (e) {
      const errorMessage = e instanceof Error ? e.message : 'Ein unerwarteter Fehler ist aufgetreten.';
      setError(`Fehler beim Abrufen der Antwort: ${errorMessage}`);
      setResponse('');
    } finally {
      setIsLoading(false);
    }
  }, [prompt]);

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-3xl mx-auto">
        <header className="text-center mb-8">
          <div className="inline-flex items-center gap-3 mb-2">
            <KeyIcon className="w-10 h-10 text-purple-400" />
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-purple-400 to-indigo-500 text-transparent bg-clip-text">
              Google AI Key Validator
            </h1>
          </div>
          <p className="text-gray-400 text-lg">
            Gib eine Anfrage ein, um deinen Google AI API Key zu validieren.
          </p>
        </header>

        <main className="bg-gray-800/50 backdrop-blur-sm rounded-2xl shadow-2xl shadow-black/20 border border-gray-700 p-6 md:p-8 space-y-6">
          <PromptInput
            prompt={prompt}
            setPrompt={setPrompt}
            onSubmit={handleGenerate}
            isLoading={isLoading}
          />
          <ResponseDisplay
            response={response}
            isLoading={isLoading}
            error={error}
          />
        </main>

        <footer className="mt-8 text-center">
          <ApiKeyInfo />
        </footer>
      </div>
    </div>
  );
};

export default App;
