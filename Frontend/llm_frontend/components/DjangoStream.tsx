import React, { useState, useEffect } from 'react';

interface DjangoStreamProps {
  input: string;
}
const DjangoStream: React.FC<DjangoStreamProps> = ({ input }) => {
  const [lines, setLines] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/prompt_c?input=${encodeURIComponent(input)}`);
        if (!response.ok) {
          throw new Error("Failed to fetch from Django endpoint");
        }

        const reader = response.body!.getReader();
        const decoder = new TextDecoder('utf-8');

        while (true) {
          const { value, done } = await reader.read();
          if (done) break;

          const textChunk = decoder.decode(value);
          setLines(prev => [...prev, textChunk]);
        }
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError('An unknown error occurred.');
        }
      }
    };

    fetchData();

  }, [input]);

  return (
    <div className="bg-slate-400 rounded-lg">
      {error && <div>Error: {error}</div>}
      {lines.map((line, index) => (
        <div key={index}>{line}</div>
      ))}
    </div>
  );
};

export default DjangoStream;