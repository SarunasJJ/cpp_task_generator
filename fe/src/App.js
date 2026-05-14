import React, { useState, useEffect } from 'react';

const API_BASE = 'http://localhost:5000';

const TOPICS = [
  { value: 'variables and operators', label: 'Variables and operators' },
  { value: 'conditionals and loops', label: 'Conditionals and loops' },
  { value: 'arrays and strings', label: 'Arrays and strings' },
  { value: 'pointers and memory allocation', label: 'Pointers and memory allocation' },
];

const PROVIDERS = [
  { value: 'gemini', label: 'Google Gemini' },
  { value: 'claude', label: 'Anthropic Claude' },
  { value: 'gpt', label: 'OpenAI GPT' },
];

function parseInlineMarkdown(text) {
  const parts = [];
  const regex = /\*\*(.+?)\*\*|`(.+?)`/g;
  let lastIndex = 0;
  let match;
  let key = 0;
  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) parts.push(text.slice(lastIndex, match.index));
    if (match[1] !== undefined) {
      parts.push(<strong key={key++}>{match[1]}</strong>);
    } else {
      parts.push(
        <code key={key++} style={{ background: '#f0f0f0', padding: '1px 5px', borderRadius: '3px', fontFamily: 'monospace', fontSize: '0.9em' }}>
          {match[2]}
        </code>
      );
    }
    lastIndex = regex.lastIndex;
  }
  if (lastIndex < text.length) parts.push(text.slice(lastIndex));
  return parts;
}

function WorkedExample({ text }) {
  return (
    <div style={{ background: '#f0f4ff', border: '1px solid #c5d0e6', borderLeft: '4px solid #4a6cf7', borderRadius: '6px', padding: '16px', marginTop: '12px', marginBottom: '4px' }}>
      <div style={{ fontWeight: 'bold', fontSize: '0.85em', color: '#4a6cf7', textTransform: 'uppercase', letterSpacing: '0.07em', marginBottom: '8px' }}>
        Example
      </div>
      <p style={{ margin: 0, color: '#333' }}>{parseInlineMarkdown(text)}</p>
    </div>
  );
}

function TaskCard({ task, index }) {
  const valid = task.valid ?? task.validation?.all_passed;
  const vr = task.validation || {};

  return (
    <div
      style={{
        border: `2px solid ${valid ? '#28a745' : '#dc3545'}`,
        margin: '20px 0',
        padding: '20px',
        borderRadius: '8px',
        background: valid ? '#f8fff9' : '#fff8f8',
        boxShadow: '0 2px 4px rgba(0,0,0,0.06)',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '12px' }}>
        <h2 style={{ marginTop: 0, marginBottom: '8px' }}>
          {index + 1}. {task.title}
        </h2>
        <span
          style={{
            padding: '6px 12px',
            background: valid ? '#28a745' : '#dc3545',
            color: 'white',
            borderRadius: '4px',
            fontSize: '13px',
            fontWeight: 'bold',
            whiteSpace: 'nowrap',
          }}
        >
          {valid ? 'Valid (tests passed)' : 'Invalid (tests failed or compile error)'}
        </span>
      </div>

      {(() => {
        const marker = 'WORKED EXAMPLE:';
        const idx = (task.description || '').indexOf(marker);
        const mainDesc = idx === -1
          ? (task.description || '').trim()
          : task.description.slice(0, idx).trim();
        const exampleText = idx !== -1
          ? task.description.slice(idx + marker.length).trim()
          : null;
        const paragraphs = mainDesc.split(/\n\n+/).map(p => p.trim()).filter(Boolean);
        return (
          <>
            <div style={{ marginTop: 0, marginBottom: exampleText ? '4px' : '15px' }}>
              <strong>Description:</strong>
              {paragraphs.map((para, i) => (
                <p key={i} style={{ margin: '8px 0 0 0' }}>{parseInlineMarkdown(para)}</p>
              ))}
            </div>
            {exampleText && <WorkedExample text={exampleText} />}
          </>
        );
      })()}

      <div style={{ marginBottom: '15px' }}>
        <strong>Expected test cases:</strong>
        {Array.isArray(task.test_cases) && task.test_cases.length > 0 ? (
          <ul style={{ paddingLeft: '20px', margin: '8px 0' }}>
            {task.test_cases.map((tc, i) => (
              <li key={i} style={{ marginBottom: '8px' }}>
                <div>
                  <strong>Input:</strong>{' '}
                  <span style={{ whiteSpace: 'pre-wrap' }}>{tc.input}</span>
                </div>
                <div>
                  <strong>Expected output:</strong>{' '}
                  <span style={{ whiteSpace: 'pre-wrap' }}>{tc.expected_output}</span>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p style={{ color: '#666' }}>None parsed.</p>
        )}
      </div>

      <div style={{ marginBottom: '15px' }}>
        <strong>Solution:</strong>
        <pre style={{ background: '#f4f4f4', padding: '12px', overflowX: 'auto', fontSize: '13px' }}>
          {task.solution || '(no solution)'}
        </pre>
      </div>

      <div style={{ marginTop: '16px', padding: '12px', background: '#fff', border: '1px solid #ddd', borderRadius: '6px' }}>
        <strong>Validation (gcc + run):</strong>
        <p style={{ margin: '8px 0' }}>
          <strong>Compiled:</strong> {vr.compiled ? 'Yes' : 'No'}
        </p>
        {vr.compilation_error && (
          <div style={{ marginBottom: '10px' }}>
            <strong>Compilation error:</strong>
            <pre style={{ background: '#ffe6e6', padding: '10px', fontSize: '12px', overflowX: 'auto' }}>
              {vr.compilation_error}
            </pre>
          </div>
        )}
        {vr.test_results && vr.test_results.length > 0 && (
          <div>
            <strong>Per-test results:</strong>
            {vr.test_results.map((tr, idx) => (
              <div
                key={idx}
                style={{
                  marginTop: '10px',
                  padding: '10px',
                  background: tr.passed ? '#e8f5e9' : '#ffebee',
                  borderRadius: '4px',
                  fontSize: '13px',
                }}
              >
                <div>
                  <strong>Test {tr.test_number}:</strong> {tr.passed ? 'Passed' : 'Failed'}
                </div>
                <div>
                  <strong>Input:</strong> <span style={{ whiteSpace: 'pre-wrap' }}>{tr.input}</span>
                </div>
                <div>
                  <strong>Expected:</strong> <span style={{ whiteSpace: 'pre-wrap' }}>{tr.expected}</span>
                </div>
                <div>
                  <strong>Actual:</strong> <span style={{ whiteSpace: 'pre-wrap' }}>{tr.actual ?? 'N/A'}</span>
                </div>
                {tr.error && (
                  <div style={{ color: '#c62828' }}>
                    <strong>Runtime error:</strong> {tr.error}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function App() {
  const [config, setConfig] = useState({
    topic: TOPICS[0].value,
    num_tasks: 1,
    provider: 'gemini',
  });

  const [tasks, setTasks] = useState([]);
  const [meta, setMeta] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('generator');

  const [jsonFiles, setJsonFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileContent, setFileContent] = useState(null);
  const [loadingFiles, setLoadingFiles] = useState(false);

  const generate = async () => {
    setLoading(true);
    setError(null);
    setTasks([]);
    setMeta(null);

    const body = {
      topic: config.topic,
      num_tasks: parseInt(config.num_tasks, 10),
      provider: config.provider,
    };

    try {
      const res = await fetch(`${API_BASE}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });

      const data = await res.json();

      if (data.success && Array.isArray(data.tasks)) {
        setTasks(data.tasks);
        setMeta({
          provider: data.provider,
          total_generated: data.total_generated,
          valid_count: data.valid_count,
          invalid_count: data.invalid_count,
        });
      } else {
        setError(data.error || 'Failed to generate tasks');
      }
    } catch (err) {
      console.error(err);
      setError('Network error: could not connect to server');
    }
    setLoading(false);
  };

  const loadJsonFiles = async () => {
    setLoadingFiles(true);
    try {
      const res = await fetch(`${API_BASE}/api/files`);
      const data = await res.json();
      if (data.files) {
        setJsonFiles(data.files);
      }
    } catch (err) {
      console.error('Error loading files:', err);
    }
    setLoadingFiles(false);
  };

  const loadFileContent = async (filename) => {
    try {
      const res = await fetch(`${API_BASE}/api/files/${filename}`);
      const data = await res.json();
      setFileContent(data);
      setSelectedFile(filename);
    } catch (err) {
      console.error('Error loading file content:', err);
    }
  };

  useEffect(() => {
    if (activeTab === 'viewer') {
      loadJsonFiles();
    }
  }, [activeTab]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig((prev) => ({ ...prev, [name]: value }));
  };

  const isTaskValid = (t) => t.valid ?? t.validation?.all_passed;
  const validTasks = tasks.filter((t) => isTaskValid(t));
  const invalidTasks = tasks.filter((t) => !isTaskValid(t));

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '20px', fontFamily: 'system-ui, Arial, sans-serif' }}>
      <h1>C exercise generator</h1>
      <p style={{ color: '#555', marginTop: '-8px' }}>
        Generate stdin/stdout C exercises, compile with gcc, and review every exercise — including failures — with
        tests and solutions.
      </p>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '2px solid #ddd' }}>
        <button
          type="button"
          onClick={() => setActiveTab('generator')}
          style={{
            padding: '10px 20px',
            background: activeTab === 'generator' ? '#007bff' : 'transparent',
            color: activeTab === 'generator' ? 'white' : '#007bff',
            border: 'none',
            borderBottom: activeTab === 'generator' ? '3px solid #007bff' : 'none',
            cursor: 'pointer',
            fontSize: '16px',
            fontWeight: 'bold',
          }}
        >
          Generator
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('viewer')}
          style={{
            padding: '10px 20px',
            background: activeTab === 'viewer' ? '#007bff' : 'transparent',
            color: activeTab === 'viewer' ? 'white' : '#007bff',
            border: 'none',
            borderBottom: activeTab === 'viewer' ? '3px solid #007bff' : 'none',
            cursor: 'pointer',
            fontSize: '16px',
            fontWeight: 'bold',
          }}
        >
          Saved JSON files
        </button>
      </div>

      {activeTab === 'generator' && (
        <>
          <div
            style={{
              display: 'grid',
              gap: '12px',
              marginBottom: '20px',
              padding: '16px',
              background: '#f5f5f5',
              borderRadius: '8px',
            }}
          >
            <label>
              <strong>AI provider:</strong>
              <br />
              <select name="provider" value={config.provider} onChange={handleChange} style={{ width: '100%', padding: '8px', marginTop: '4px' }}>
                {PROVIDERS.map((p) => (
                  <option key={p.value} value={p.value}>
                    {p.label}
                  </option>
                ))}
              </select>
            </label>

            <label>
              <strong>Topic:</strong>
              <br />
              <select name="topic" value={config.topic} onChange={handleChange} style={{ width: '100%', padding: '8px', marginTop: '4px' }}>
                {TOPICS.map((t) => (
                  <option key={t.value} value={t.value}>
                    {t.label}
                  </option>
                ))}
              </select>
            </label>

            <label>
              <strong>Number of exercises:</strong>
              <br />
              <input
                type="number"
                name="num_tasks"
                min="1"
                max="100"
                value={config.num_tasks}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px', marginTop: '4px', boxSizing: 'border-box' }}
              />
            </label>

            <button
              type="button"
              onClick={generate}
              disabled={loading}
              style={{
                padding: '12px',
                background: loading ? '#ccc' : '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '16px',
                fontWeight: '600',
              }}
            >
              {loading ? 'Generating…' : 'Generate exercises'}
            </button>
          </div>

          <hr />

          {error && (
            <div style={{ color: '#b71c1c', padding: '12px', background: '#ffebee', borderRadius: '6px', marginBottom: '16px' }}>
              <strong>Error:</strong> {error}
            </div>
          )}

          {meta && (
            <div
              style={{
                padding: '12px 16px',
                background: '#e3f2fd',
                borderRadius: '6px',
                marginBottom: '16px',
                fontSize: '14px',
              }}
            >
              <strong>Provider:</strong> {meta.provider ?? '—'} · <strong>Total:</strong> {meta.total_generated} ·{' '}
              <strong style={{ color: '#2e7d32' }}>Valid:</strong> {meta.valid_count} ·{' '}
              <strong style={{ color: '#c62828' }}>Invalid:</strong> {meta.invalid_count}
            </div>
          )}

          {tasks.length > 0 ? (
            <>
              {validTasks.length > 0 && (
                <section style={{ marginBottom: '32px' }}>
                  <h2 style={{ fontSize: '1.25rem', color: '#2e7d32', borderBottom: '2px solid #c8e6c9', paddingBottom: '8px' }}>
                    Valid exercises ({validTasks.length})
                  </h2>
                  {validTasks.map((task) => {
                    const idx = tasks.indexOf(task);
                    return <TaskCard key={`v-${idx}`} task={task} index={idx} />;
                  })}
                </section>
              )}

              {invalidTasks.length > 0 && (
                <section>
                  <h2 style={{ fontSize: '1.25rem', color: '#c62828', borderBottom: '2px solid #ffcdd2', paddingBottom: '8px' }}>
                    Invalid exercises ({invalidTasks.length})
                  </h2>
                  {invalidTasks.map((task) => {
                    const idx = tasks.indexOf(task);
                    return <TaskCard key={`i-${idx}`} task={task} index={idx} />;
                  })}
                </section>
              )}
            </>
          ) : (
            !loading && <p style={{ textAlign: 'center', color: '#666' }}>Choose options and click Generate.</p>
          )}
        </>
      )}

      {activeTab === 'viewer' && (
        <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: '20px', minHeight: '500px' }}>
          <div style={{ borderRight: '1px solid #ddd', paddingRight: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
              <h3 style={{ margin: 0 }}>Saved files</h3>
              <button
                type="button"
                onClick={loadJsonFiles}
                disabled={loadingFiles}
                style={{
                  padding: '5px 10px',
                  background: '#28a745',
                  color: 'white',
                  border: 'none',
                  borderRadius: '3px',
                  cursor: loadingFiles ? 'not-allowed' : 'pointer',
                  fontSize: '12px',
                }}
              >
                {loadingFiles ? '…' : 'Refresh'}
              </button>
            </div>

            {jsonFiles.length === 0 ? (
              <p style={{ color: '#666', fontSize: '14px' }}>No files found</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '5px' }}>
                {jsonFiles.map((file, i) => (
                  <button
                    type="button"
                    key={i}
                    onClick={() => loadFileContent(file)}
                    style={{
                      padding: '10px',
                      background: selectedFile === file ? '#007bff' : 'white',
                      color: selectedFile === file ? 'white' : '#333',
                      border: '1px solid #ddd',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      textAlign: 'left',
                      fontSize: '13px',
                      wordBreak: 'break-all',
                    }}
                  >
                    {file}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div>
            {!fileContent ? (
              <p style={{ textAlign: 'center', color: '#666', marginTop: '50px' }}>
                Select a file to view its contents
              </p>
            ) : (
              <div>
                <div style={{ background: '#f5f5f5', padding: '15px', borderRadius: '5px', marginBottom: '20px' }}>
                  <h3 style={{ margin: '0 0 10px 0' }}>{selectedFile}</h3>
                  <p style={{ margin: '5px 0', fontSize: '14px' }}>
                    <strong>Generated:</strong> {fileContent.generated_at}
                  </p>
                  {fileContent.provider && (
                    <p style={{ margin: '5px 0', fontSize: '14px' }}>
                      <strong>Provider:</strong> {fileContent.provider}
                    </p>
                  )}
                  <p style={{ margin: '5px 0', fontSize: '14px' }}>
                    <strong>Total tasks:</strong> {fileContent.num_tasks}
                  </p>
                  <p style={{ margin: '5px 0', fontSize: '14px' }}>
                    <strong>Passed validation:</strong>{' '}
                    {fileContent.tasks?.filter((t) => t.validation?.all_passed || t.valid).length || 0} /{' '}
                    {fileContent.num_tasks}
                  </p>
                </div>

                {fileContent.tasks?.map((task, i) => (
                  <TaskCard key={i} task={task} index={i} />
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
