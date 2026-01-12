import google.generativeai as genai
import json
from datetime import datetime

from .prompt_builder import PromptBuilder
from .parser import ResponseParser
from .compiler import Compiler

class CPPTaskGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
    
    def generate_tasks(self, topic, task_type, num_tasks=1):
        print(f"\n{'='*60}")
        print(f"Generating {num_tasks} C++ task(s)...")
        print(f"Topic: {topic} | Type: {task_type}")
        print(f"{'='*60}\n")
        
        prompt = PromptBuilder.build_prompt(topic, task_type, num_tasks)
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            tasks = ResponseParser.parse_response(response_text)
            
            if not tasks:
                print("Failed to parse any tasks from response")
                return []
            
            print(f"Parsed {len(tasks)} tasks\n")
            
            validated_tasks = self._validate_tasks(tasks)
            
            return validated_tasks
            
        except Exception as e:
            print(f"Error generating tasks: {e}")
            return []
    
    def _validate_tasks(self, tasks):
        validated_tasks = []
        for i, task in enumerate(tasks, 1):
            test_results = Compiler.compile_and_test(task['solution'], task['test_cases'])
            task['test_results'] = test_results
            
            validated_tasks.append(task)
            
            if test_results['all_passed']:
                print(f"Task {i} validated successfully!")
            else:
                print(f"Task {i} failed validation - kept for research.")
        
        return validated_tasks
    
    def save_to_json(self, tasks, filename="research_tasks.json"):
        output = {
            'generated_at': datetime.now().isoformat(),
            'num_tasks': len(tasks),
            'tasks': []
        }
        for task in tasks:
            task_data = {
                'title': task.get('title'),
                'description': task.get('description'),
                'buggy_code': task.get('buggy_code'),
                'code_with_blanks': task.get('code_with_blanks'),
                'solution': task.get('solution'),
                'test_cases': task.get('test_cases'),
                'validation': task.get('test_results')
            }
            output['tasks'].append(task_data)
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)