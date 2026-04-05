import React, { useState } from 'react';
import type { ChangeEvent } from 'react';

const App: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [q, setQ] = useState<string>('');
  const [ans, setAns] = useState<string>('');

  const upload = async () => {
    if (!file) {
      alert('Please select a file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      console.log(data);

      alert('Uploaded');
    } catch (err) {
      console.error(err);
      alert('Upload failed');
    }
  };

  const ask = async () => {
    if (!q.trim()) {
      alert('Enter a question');
      return;
    }

    try {
      const res = await fetch('/api/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: q }),
      });

      const data = await res.json();
      setAns(data.answer);
    } catch (err) {
      console.error(err);
      alert('Error fetching answer');
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>PDF Q&A</h2>

      <input type="file" onChange={handleFileChange} />
      <button onClick={upload}>Upload</button>

      <br /><br />

      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={ask}>Ask</button>

      <p><strong>Answer:</strong> {ans}</p>
    </div>
  );
};

export default App;