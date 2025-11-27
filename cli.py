import os
from BE import CPPTaskGenerator

def main():
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("No API key provided")
        return
    
    generator = CPPTaskGenerator(api_key)
    
    print("\n--- Task Parameters ---\n")
    
    print("Available topics:")
    print("1. Loops")
    print("2. Conditionals")
    print("3. Arrays")
    print("4. Pointers")
    print("5. Functions")
    print("6. Classes")
    print("7. STL (Standard Template Library)")
    print("8. Recursion")
    
    topic_map = {
        '1': 'Loops',
        '2': 'Conditionals',
        '3': 'Arrays',
        '4': 'Pointers',
        '5': 'Functions',
        '6': 'Classes',
        '7': 'STL',
        '8': 'Recursion'
    }
    topic_choice = input("\nSelect topic (1-8): ").strip()
    topic = topic_map.get(topic_choice, 'Loops')
    
    print("\nDifficulty levels:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    
    difficulty_map = {
        '1': 'easy',
        '2': 'medium',
        '3': 'hard'
    }
    difficulty_choice = input("\nSelect difficulty (1-3): ").strip()
    difficulty = difficulty_map.get(difficulty_choice, 'easy')
    
    print("\nTask types:")
    print("1. Write function")
    print("2. Fix code")
    print("3. Fill in blank")
    
    type_map = {
        '1': 'write_function',
        '2': 'fix_code',
        '3': 'fill_blank'
    }
    type_choice = input("\nSelect task type (1-3): ").strip()
    task_type = type_map.get(type_choice, 'write_function')
    
    num_tasks = int(input("\nNumber of tasks to generate: ").strip() or "1")
    
    tasks = generator.generate_tasks(topic, difficulty, task_type, num_tasks)
    
    if tasks:
        print(f"\n{'='*60}")
        print(f"Successfully generated and validated {len(tasks)} task(s)!")
        print(f"{'='*60}\n")
        
        save = input("Save tasks to JSON file? (y/n): ").strip().lower()
        if save == 'y':
            filename = input("Filename (default: tasks.json): ").strip() or "tasks.json"
            generator.save_to_json(tasks, filename)
    else:
        print("\nNo valid tasks were generated.")

if __name__ == "__main__":
    main()