import React, { useState } from 'react';

function App() {
  const [config, setConfig] = useState({
    topic: 'Loops',
    task_type: 'write_function',
    num_tasks: 1
  });
  
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const generate = async () => {
    setLoading(true);
    setError(null);
    setTasks([]);

    try {
      const res = await fetch('http://localhost:5000/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic: config.topic,
          task_type: config.task_type,
          num_tasks: parseInt(config.num_tasks),
        }),
      });

      const data = await res.json();

      if (data.success && Array.isArray(data.tasks)) {
        setTasks(data.tasks);
      } else {
        setError(data.error || "Failed to generate tasks");
        setTasks([]);
      }

    } catch (err) {
      console.error(err);
      setError("Network error: Could not connect to server");
      setTasks([]);
    }
    setLoading(false);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig(prev => ({
      ...prev,
      [name]: value
    }));
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>C++ Exercise Generator</h1>
      
      <div style={{ display: 'grid', gap: '10px', marginBottom: '20px', padding: '15px', background: '#f5f5f5', borderRadius: '5px' }}>
        
        <label>
          <strong>Topic:</strong><br/>
          <select name="topic" value={config.topic} onChange={handleChange} style={{ width: '100%', padding: '5px' }}>
            <option value="Loops">Loops</option>
            <option value="Conditionals">Conditionals</option>
            <option value="Arrays">Arrays</option>
            <option value="Pointers">Pointers</option>
            <option value="Functions">Functions</option>
            <option value="Classes">Classes</option>
            <option value="Recursion">Recursion</option>
          </select>
        </label>

        <label>
          <strong>Task Type:</strong><br/>
          <select name="task_type" value={config.task_type} onChange={handleChange} style={{ width: '100%', padding: '5px' }}>
            <option value="write_function">Write Function</option>
            <option value="fix_code">Fix Buggy Code</option>
            <option value="fill_blank">Fill in Blanks</option>
          </select>
        </label>

        <label>
          <strong>Number of Exercises:</strong><br/>
          <input 
            type="number" 
            name="num_tasks" 
            min="1" 
            max="100"
            value={config.num_tasks} 
            onChange={handleChange}
            style={{ width: '100%', padding: '5px' }}
          />
        </label>

        <button 
          onClick={generate} 
          disabled={loading}
          style={{ 
            padding: '10px', 
            background: loading ? '#ccc' : '#007bff', 
            color: 'white', 
            border: 'none', 
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '16px'
          }}
        >
          {loading ? 'Generating...' : 'Generate Exercises'}
        </button>
      </div>

      <hr />

      {error && (
        <div style={{ color: 'red', padding: '10px', background: '#ffe6e6', borderRadius: '4px', marginBottom: '20px' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {tasks.length > 0 ? (
        tasks.map((task, i) => (
          <div key={i} style={{ border: '1px solid #ccc', margin: '20px 0', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h2 style={{ marginTop: 0 }}>{i + 1}. {task.title}</h2>
            <p><strong>Description:</strong> {task.description}</p>
            
            {task.buggy_code && (
              <div style={{ marginBottom: '15px' }}>
                <strong>Buggy Code:</strong>
                <pre style={{ background: '#ffe6e6', padding: '10px', overflowX: 'auto' }}>{task.buggy_code}</pre>
              </div>
            )}
            
            {task.code_with_blanks && (
              <div style={{ marginBottom: '15px' }}>
                <strong>Fill in the Blanks:</strong>
                <pre style={{ background: '#e6f3ff', padding: '10px', overflowX: 'auto' }}>{task.code_with_blanks}</pre>
              </div>
            )}
            
            <details>
              <summary style={{ cursor: 'pointer', color: '#007bff' }}>View Solution & Test Cases</summary>
              <div style={{ marginTop: '10px' }}>
                <strong>Solution:</strong>
                <pre style={{ background: '#f0f0f0', padding: '10px', overflowX: 'auto' }}>{task.solution}</pre>
                
                <strong>Example Test Cases:</strong>
                <ul style={{ listStyle: 'none', padding: 0 }}>
                  {task.test_cases && task.test_cases.map((tc, idx) => (
                    <li key={idx} style={{ background: '#fafafa', padding: '5px', borderBottom: '1px solid #eee' }}>
                      <code>In: {tc.input}</code> → <code>Out: {tc.expected_output}</code>
                    </li>
                  ))}
                </ul>
              </div>
            </details>
          </div>
        ))
      ) : (
        !loading && <p style={{ textAlign: 'center', color: '#666' }}>Select options above and click Generate to begin.</p>
      )}
    </div>
  );
}

export default App;