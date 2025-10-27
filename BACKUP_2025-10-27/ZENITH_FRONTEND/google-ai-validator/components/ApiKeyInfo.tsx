import React from 'react';
import { KeyIcon, ShieldCheckIcon } from './icons';

const ApiKeyInfo: React.FC = () => {
  return (
    <div className="inline-flex items-center gap-3 bg-gray-800/60 border border-gray-700 text-gray-400 text-sm px-4 py-2 rounded-full">
      <KeyIcon className="w-5 h-5 text-green-400" />
      <span>Dein Google AI API Key wird sicher aus der Umgebung abgerufen. Eine erfolgreiche Antwort bestätigt, dass er funktioniert.</span>
      <ShieldCheckIcon className="w-5 h-5 text-green-400" />
    </div>
  );
};

export default ApiKeyInfo;
