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
TITLE: [A short, descriptive name for the problem]

DESCRIPTION:
[INTRODUCTION - a paragraph, 2 to 3 brief sentences that explain the concept and provide a motivating
real-world context. Do not state the task yet. Do not assume any domain knowledge
beyond the target programming concept. If the exercise involves a named algorithm
or mathematical concept (e.g. GCD, Fibonacci), explain what it is here before
asking the student to implement it.]

[INSTRUCTIONS - A paragraph stating exactly what the program must do.
Specify: what input is read from stdin (types, format, and ranges), what the
program must compute or determine, and what it must print to stdout. State any
edge cases and constraints explicitly (e.g. what happens for zero or negative input).
Do NOT reveal the implementation strategy or suggest how to solve the problem.]

WORKED EXAMPLE:
[ONLY ADD TO EXERCISES WHERE A VALUE ACCUMULATES OR CHANGES ACROSS STEPS. Show only the changing value using arrows, e.g. "Input: 1 5 → sum: 1 → 4 → 9. Output: 9". DO NOT mention variables, flags, algorithms, implementation steps, or how the solution works internally. DO NOT use bullet points, numbered lists, or per-iteration breakdowns. One or two sentences maximum. Use real numbers, not placeholders. If no value changes across steps, omit this section entirely.]

SOLUTION:
```c
[Complete, working C solution — reads from stdin, writes to stdout]
```

TEST_CASES:
Input: [test input 1]
Expected Output: [exact expected output 1]

Input: [test input 2]
Expected Output: [exact expected output 2]

Input: [test input 3]
Expected Output: [exact expected output 3]

---
"""

        prompt = f"""You are an expert C programming educator. Generate {num_tasks} C programming exercise(s) \
for the following topic: {topic}

Each exercise must be a complete stdin/stdout program that a student writes from scratch.
Use only standard C (C11) with headers from: stdio.h, stdlib.h, string.h, ctype.h, math.h.

Follow this structure exactly for each exercise:

{task_instructions}

REQUIREMENTS:
1. These exercises are INTRODUCTORY level! Meant to introduce students to these C language concepts, they should not be too difficult.
2. DESCRIPTION — Introduction section: explain the concept and real-world context. Never assume the student \
knows a named algorithm (e.g. Euclidean algorithm, Fibonacci) — define it before asking \
them to implement it.
3. DESCRIPTION — Instructions section: specify stdin format (data types, number of values, \
order), stdout format (exact output wording and newlines), input constraints, and edge case \
behavior. Do not hint at the implementation.
4. WORKED EXAMPLE (separate section after DESCRIPTION): one or two sentences max, inline arrow format only \
(e.g. "Input: 1 5 → sum: 1 → 4 → 9. Output: 9"). Show ONLY the changing value — never mention variable names, \
flags, algorithm steps, divisibility checks, or any implementation detail. NEVER use bullet points or lists. \
ONLY ADD where a value accumulates or changes across steps — otherwise omit the section entirely.
5. SOLUTION: must be a complete, compilable C program with main() that reads from stdin \
and prints to stdout. Include all necessary #include lines.
6. TEST_CASES: expected outputs must be character-perfect, including spacing and newlines. \
Cover a typical case, a boundary/edge case, and one additional case.
7. The description and test cases must be consistent — the worked example in the description \
must match what the solution actually produces.

Generate {num_tasks} task(s) now:"""

        return prompt