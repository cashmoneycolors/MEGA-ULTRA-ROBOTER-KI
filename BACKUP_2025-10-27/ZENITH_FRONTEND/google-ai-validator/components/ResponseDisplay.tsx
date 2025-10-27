import React from 'react';

interface ResponseDisplayProps {
  response: string;
  isLoading: boolean;
  error: string;
}

const LoadingSkeleton: React.FC = () => (
  <div className="space-y-4 animate-pulse">
    <div className="h-4 bg-gray-600 rounded w-3/4"></div>
    <div className="h-4 bg-gray-600 rounded w-full"></div>
    <div className="h-4 bg-gray-600 rounded w-5/6"></div>
    <div className="h-4 bg-gray-600 rounded w-1/2"></div>
  </div>
);

const ResponseDisplay: React.FC<ResponseDisplayProps> = ({ response, isLoading, error }) => {
  return (
    <div className="bg-gray-900/50 rounded-xl p-6 min-h-[150px] border border-gray-700">
      <h2 className="text-lg font-semibold text-gray-300 mb-4">Antwort</h2>
      <div className="prose prose-invert max-w-none text-gray-200">
        {isLoading && <LoadingSkeleton />}
        {error && (
          <div className="bg-red-900/50 border border-red-500 text-red-300 p-4 rounded-lg">
            <p className="font-bold">Ein Fehler ist aufgetreten:</p>
            <p>{error}</p>
          </div>
        )}
        {!isLoading && !error && response && (
          <p style={{ whiteSpace: 'pre-wrap' }}>{response}</p>
        )}
        {!isLoading && !error && !response && (
          <p className="text-gray-500">Deine generierte Antwort wird hier erscheinen.</p>
        )}
      </div>
    </div>
  );
};

export default ResponseDisplay;
