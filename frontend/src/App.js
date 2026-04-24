import React, { useState } from "react";
import axios from "axios";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyzeText = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await axios.post("http://127.0.0.1:8000/analyze-text", {
        text: text,
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError("Backend not reachable. Make sure server is running.");
    }

    setLoading(false);
  };

  const analyzeImage = async (e) => {
    setLoading(true);
    setError("");
    setResult(null);

    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/analyze-image",
        formData
      );
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError("Image upload failed.");
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <div className="title">🧠 Medical AI Analyzer</div>

      <textarea
        rows="5"
        placeholder="Enter medical report..."
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={analyzeText}>Analyze Text</button>

      <div style={{ marginTop: "20px" }}>
        <input type="file" onChange={analyzeImage} />
      </div>

      {loading && <div className="loading">⏳ Processing...</div>}
      {error && <div className="error">{error}</div>}

      {result && (
        <div className="card">
          <h3>📄 Summary</h3>
          <p>{result.summary}</p>

          <h3>🔍 Entities</h3>
          <pre>{JSON.stringify(result.entities, null, 2)}</pre>

          <h3>🏥 Medical Insights</h3>
          <pre>{JSON.stringify(result.medical, null, 2)}</pre>

          <h3>📊 Confidence</h3>
          <p>{result.confidence}</p>
        </div>
      )}
    </div>
  );
}

export default App;