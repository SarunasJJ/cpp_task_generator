from flask import Flask, request, jsonify
from flask_cors import CORS
from BE import CPPTaskGenerator
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app) 

API_KEY = os.getenv('GEMINI_API_KEY', '')
generator = None

if API_KEY:
    try:
        generator = CPPTaskGenerator(API_KEY)
    except Exception as e:
        print(f"Error initializing generator: {e}")

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/config', methods=['POST'])
def set_api_key():
    global generator
    data = request.json
    api_key = data.get('api_key', '')
    
    if not api_key:
        return jsonify({'error': 'API key required'}), 400
    
    try:
        generator = CPPTaskGenerator(api_key)
        return jsonify({'message': 'API key configured successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate', methods=['POST'])
def generate_tasks():
    global generator
    if not generator:
        return jsonify({'error': 'API key not configured'}), 400
    
    data = request.json
    topic = data.get('topic')
    task_type = data.get('task_type')
    num_tasks = data.get('num_tasks', 1)
    
    try:
        all_tasks = generator.generate_tasks(topic, task_type, num_tasks)
        
        research_filename = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        generator.save_to_json(all_tasks, filename=os.path.join('generated_tasks', research_filename))
        
        valid_tasks_for_frontend = []
        for task in all_tasks:
            if task['test_results']['all_passed']:
                valid_tasks_for_frontend.append({
                    'title': task['title'],
                    'description': task['description'],
                    'buggy_code': task.get('buggy_code'),
                    'code_with_blanks': task.get('code_with_blanks'),
                    'solution': task['solution']
                })
        
        return jsonify({
            'success': True,
            'total_generated': len(all_tasks),
            'valid_count': len(valid_tasks_for_frontend),
            'tasks': valid_tasks_for_frontend
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)