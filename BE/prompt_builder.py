"""
Prompt builder for C exercise generation (any supported LLM).
"""


class PromptBuilder:
    TASK_TYPE_DESCRIPTIONS = {
        "write_function": "Write a complete program from scratch",
        "fix_code": "Fix buggy code",
        "fill_blank": "Fill in missing parts of code",
    }

    TOPICS = [
        "variables and operators",
        "conditionals and loops",
        "arrays and strings",
        "pointers and memory allocation",
    ]

    @staticmethod
    def build_prompt(topic, task_type, num_tasks):
        task_desc = PromptBuilder.TASK_TYPE_DESCRIPTIONS.get(task_type, task_type)

        if task_type == "fix_code":
            task_instructions = """
TASK [number]:
TITLE: [Brief title]
DESCRIPTION: [Problem description]
BUGGY_CODE:
```c
[Buggy C code with errors that need to be fixed]
```
SOLUTION:
```c
[Fixed, working C solution code]
```
"""
        elif task_type == "fill_blank":
            task_instructions = """
TASK [number]:
TITLE: [Brief title]
DESCRIPTION: [Problem description]
CODE_WITH_BLANKS:
```c
[C code with blanks marked as _____ that need to be filled]
```
SOLUTION:
```c
[Complete, working C solution code]
```
"""
        else:
            task_instructions = """
TASK [number]:
TITLE: [Brief title]
DESCRIPTION: [Clear problem description with requirements]
SOLUTION:
```c
[Complete, working C solution code]
```
"""

        prompt = f"""You are an expert C programming educator. Generate {num_tasks} programming exercise(s) with the following specifications:

Topic: {topic}
Task Type: {task_desc}

Focus the exercises strictly on standard C (C11). Use only: stdio.h, stdlib.h, string.h, ctype.h, math.h as needed.

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
1. For "write_function" / write-from-scratch tasks, the description must specify stdin/stdout formats, edge cases, and constraints.
2. Solutions MUST be complete, compilable C code with necessary #include lines.
3. Solutions MUST have a main() function that reads from stdin and writes to stdout (unless the description explicitly defines a different I/O contract — then follow that consistently in tests).
4. Test cases must have EXACT expected outputs (character-perfect), including newlines if your program prints them.
5. For "fix_code" tasks: include a BUGGY_CODE section with deliberate errors. Do NOT add comments like '// Bug:' or '// Error here'.
6. For "fill_blank" tasks: use CODE_WITH_BLANKS with blanks as _____. Comments in the partial code must NOT reveal the answer.
7. For "pointers and memory allocation" topics, you may use malloc/calloc/realloc/free where appropriate; ensure no leaks on the tested paths and that invalid inputs are handled as described.
8. Keep programs small enough to compile and run quickly.

Generate {num_tasks} task(s) now:"""

        return prompt
