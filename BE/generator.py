import google.generativeai as genai
import json
from datetime import datetime

from .prompt_builder import PromptBuilder
from .parser import ResponseParser
from .compiler import Compiler

class CPPTaskGenerator:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    def generate_tasks(self, topic, difficulty, task_type, num_tasks=1):
        print(f"\n{'='*60}")
        print(f"Generating {num_tasks} C++ task(s)...")
        print(f"Topic: {topic} | Difficulty: {difficulty} | Type: {task_type}")
        print(f"{'='*60}\n")
        
        prompt = PromptBuilder.build_prompt(topic, difficulty, task_type, num_tasks)
        
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
            print(f"\n--- Testing Task {i}: {task['title']} ---")
            
            test_results = Compiler.compile_and_test(task['solution'], task['test_cases'])
            task['test_results'] = test_results
            
            if not test_results['compiled']:
                print(f"Compilation failed:")
                print(test_results['compilation_error'])
                continue
            
            print(f"Compilation successful")
            
            passed = sum(1 for t in test_results['test_results'] if t['passed'])
            total = len(test_results['test_results'])
            print(f"Tests: {passed}/{total} passed")
            
            for test in test_results['test_results']:
                status = "passed" if test['passed'] else "failed"
                print(f"  {status} Test {test['test_number']}: ", end="")
                if test['passed']:
                    print("PASSED")
                elif test['error']:
                    print(f"ERROR - {test['error']}")
                else:
                    print(f"FAILED")
                    print(f"     Expected: {test['expected']}")
                    print(f"     Got: {test['actual']}")
            
            if test_results['all_passed']:
                validated_tasks.append(task)
                print(f"Task {i} validated successfully!\n")
            else:
                print(f"Task {i} has failing tests\n")
        
        return validated_tasks
    
    def save_to_json(self, tasks, filename="tasks.json"):
        output = {
            'generated_at': datetime.now().isoformat(),
            'num_tasks': len(tasks),
            'tasks': []
        }
        
        for task in tasks:
            task_data = {
                'title': task['title'],
                'description': task['description'],
                'solution': task['solution'],
                'test_cases': task['test_cases'],
                'validation': {
                    'compiled': task['test_results']['compiled'],
                    'all_tests_passed': task['test_results']['all_passed'],
                    'test_summary': f"{sum(1 for t in task['test_results']['test_results'] if t['passed'])}/{len(task['test_results']['test_results'])} passed"
                }
            }
            output['tasks'].append(task_data)
        
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\nTasks saved to {filename}")