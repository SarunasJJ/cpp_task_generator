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

@app.route('/api/topics', methods=['GET'])
def get_topics():
    return jsonify({
        'topics': [
            'Loops',
            'Conditionals',
            'Arrays',
            'Pointers',
            'Functions',
            'Classes',
            'STL',
            'Recursion'
        ]
    })

@app.route('/api/generate', methods=['POST'])
def generate_tasks():
    global generator
    
    if not generator:
        return jsonify({'error': 'API key not configured. Call /api/config first'}), 400
    
    data = request.json
    
    topic = data.get('topic')
    difficulty = data.get('difficulty')
    task_type = data.get('task_type')
    num_tasks = data.get('num_tasks', 1)
    
    if not all([topic, difficulty, task_type]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        tasks = generator.generate_tasks(
            topic=topic,
            difficulty=difficulty,
            task_type=task_type,
            num_tasks=num_tasks
        )
        
        response_tasks = []
        for task in tasks:
            response_tasks.append({
                'title': task['title'],
                'description': task['description'],
                'solution': task['solution'],
                'test_cases': task['test_cases'],
                'validation': {
                    'compiled': task['test_results']['compiled'],
                    'all_tests_passed': task['test_results']['all_passed'],
                    'test_results': task['test_results']['test_results']
                }
            })
        
        return jsonify({
            'success': True,
            'num_generated': len(response_tasks),
            'tasks': response_tasks
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/save', methods=['POST'])
def save_tasks():
    data = request.json
    tasks = data.get('tasks', [])
    filename = data.get('filename', f'tasks_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
    
    try:
        output_dir = 'generated_tasks'
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump({
                'generated_at': datetime.now().isoformat(),
                'num_tasks': len(tasks),
                'tasks': tasks
            }, f, indent=2)
        
        return jsonify({
            'success': True,
            'filepath': filepath,
            'message': f'Saved {len(tasks)} tasks to {filename}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/batch', methods=['POST'])
def generate_batch():
    global generator
    
    if not generator:
        return jsonify({'error': 'API key not configured'}), 400
    
    data = request.json
    configurations = data.get('configurations', [])
    
    all_tasks = []
    errors = []
    
    for i, config in enumerate(configurations):
        try:
            tasks = generator.generate_tasks(
                topic=config['topic'],
                difficulty=config['difficulty'],
                task_type=config['task_type'],
                num_tasks=1
            )
            
            for task in tasks:
                all_tasks.append({
                    'config': config,
                    'title': task['title'],
                    'description': task['description'],
                    'solution': task['solution'],
                    'test_cases': task['test_cases'],
                    'validation': {
                        'compiled': task['test_results']['compiled'],
                        'all_tests_passed': task['test_results']['all_passed']
                    }
                })
                
        except Exception as e:
            errors.append({
                'config': config,
                'error': str(e)
            })
    
    return jsonify({
        'success': True,
        'total_generated': len(all_tasks),
        'total_errors': len(errors),
        'tasks': all_tasks,
        'errors': errors
    })

if __name__ == '__main__':
    print("\nAPI Endpoints:")
    print("  POST /api/config      - Set API key")
    print("  GET  /api/topics      - Get available topics")
    print("  POST /api/generate    - Generate tasks")
    print("  POST /api/save        - Save tasks to file")
    print("  POST /api/batch       - Generate batch of tasks")
    print("  GET  /api/health      - Health check")
    
    app.run(debug=True, port=5000)