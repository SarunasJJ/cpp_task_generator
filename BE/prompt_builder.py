"""
Prompt builder for C exercise generation (write-from-scratch only).
"""


class PromptBuilder:
    TOPICS = [
        "variables and operators",
        "conditionals and loops",
        "arrays and strings",
        "pointers and memory allocation",
    ]

    @staticmethod
    def build_prompt(topic, num_tasks):
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
Task type: Write a complete program from scratch (students write the full solution).

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
1. The description must specify stdin/stdout formats, edge cases, and constraints.
2. Solutions MUST be complete, compilable C code with necessary #include lines.
3. Solutions MUST have a main() function that reads from stdin and writes to stdout (unless the description explicitly defines a different I/O contract — then follow that consistently in tests).
4. Test cases must have EXACT expected outputs (character-perfect), including newlines if your program prints them.
5. For "pointers and memory allocation" topics, you may use malloc/calloc/realloc/free where appropriate; ensure no leaks on the tested paths and that invalid inputs are handled as described.
6. Keep programs small enough to compile and run quickly.

Generate {num_tasks} task(s) now:"""

        return prompt
