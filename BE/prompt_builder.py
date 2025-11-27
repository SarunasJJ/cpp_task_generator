class PromptBuilder:
    
    TASK_TYPE_DESCRIPTIONS = {
        "write_function": "Write a complete function from scratch",
        "fix_code": "Fix buggy code",
        "fill_blank": "Fill in missing parts of code"
    }
    
    DIFFICULTY_GUIDELINES = {
        "easy": "Use basic concepts like loops and conditionals",
        "medium": "Use intermediate concepts",
        "hard": "Use advanced concepts like pointers, STL, or algorithms"
    }
    
    @staticmethod
    def build_prompt(topic, difficulty, task_type, num_tasks):
        
        task_desc = PromptBuilder.TASK_TYPE_DESCRIPTIONS.get(task_type, task_type)
        difficulty_guide = PromptBuilder.DIFFICULTY_GUIDELINES.get(difficulty, "")
        
        prompt = f"""You are an expert C++ programming educator. Generate {num_tasks} programming exercise(s) with the following specifications:

Topic: {topic}
Difficulty Level: {difficulty}
Task Type: {task_desc}

For EACH task, provide the following in a structured format:

TASK [number]:
TITLE: [Brief title]
DESCRIPTION: [Clear problem description with requirements]
DIFFICULTY: {difficulty}
TOPIC: {topic}

SOLUTION:
```cpp
[Complete, working C++ solution code]
```

TEST_CASES:
Input: [test input 1]
Expected Output: [expected output 1]

Input: [test input 2]
Expected Output: [expected output 2]

Input: [test input 3]
Expected Output: [expected output 3]

---

IMPORTANT REQUIREMENTS:
1. Solutions MUST be complete, compilable C++ code with #include statements
2. Solutions MUST have a main() function that reads from stdin and writes to stdout
3. Test cases must have EXACT expected outputs (character-perfect)
4. For {difficulty} difficulty: {difficulty_guide}
5. Ensure code follows proper C++ syntax and best practices
6. Make test cases comprehensive to verify correctness

Generate {num_tasks} task(s) now:"""
        
        return prompt