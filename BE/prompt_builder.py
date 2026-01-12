"""
Prompt Builder Module
Constructs structured prompts for Gemini AI
"""

class PromptBuilder:
    """Builds prompts for task generation"""
    
    TASK_TYPE_DESCRIPTIONS = {
        "write_function": "Write a complete function from scratch",
        "fix_code": "Fix buggy code",
        "fill_blank": "Fill in missing parts of code"
    }
    
    @staticmethod
    def build_prompt(topic, task_type, num_tasks):
        """Build a structured prompt for Gemini"""
        
        task_desc = PromptBuilder.TASK_TYPE_DESCRIPTIONS.get(task_type, task_type)
        
        # Different instructions based on task type
        if task_type == "fix_code":
            task_instructions = """
TASK [number]:
TITLE: [Brief title]
DESCRIPTION: [Problem description]
BUGGY_CODE:
```cpp
[Buggy C++ code with errors that need to be fixed]
```
SOLUTION:
```cpp
[Fixed, working C++ solution code]
```
"""
        elif task_type == "fill_blank":
            task_instructions = """
TASK [number]:
TITLE: [Brief title]
DESCRIPTION: [Problem description]
CODE_WITH_BLANKS:
```cpp
[C++ code with blanks marked as _____ that need to be filled]
```
SOLUTION:
```cpp
[Complete, working C++ solution code]
```
"""
        else:  # write_function
            task_instructions = """
TASK [number]:
TITLE: [Brief title]
DESCRIPTION: [Clear problem description with requirements]
SOLUTION:
```cpp
[Complete, working C++ solution code]
```
"""
        
        prompt = f"""You are an expert C++ programming educator. Generate {num_tasks} programming exercise(s) with the following specifications:

Topic: {topic}
Task Type: {task_desc}

For EACH task, provide the following in a structured format:

{task_instructions}

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
4. For "fix_code" tasks: Include BUGGY_CODE section with code that has deliberate errors. DO NOT include comments like '// Bug: ...' or '// Error here'.
5. For "fill_blank" tasks: Include CODE_WITH_BLANKS section with blanks marked as _____. The comments in the blank code must NOT reveal the answer or give hints how to solve the probnlem.
6. Ensure code follows proper C++ syntax and best practices
7. Make test cases comprehensive to verify correctness

Generate {num_tasks} task(s) now:"""
        
        return prompt