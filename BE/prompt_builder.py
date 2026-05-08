class PromptBuilder:
    TOPICS = [
        "variables and operators",
        "conditionals and loops",
        "arrays and strings",
        "pointers and memory allocation",
    ]

    TOPIC_CONSTRAINTS = {
        "variables and operators": (
            "ALLOWED constructs: variable declarations, arithmetic operators (+,-,*,/,%), "
            "assignment operators, type casting, reading/printing with scanf/printf. "
            "BANNED constructs: if, else, switch, for, while, do-while, arrays, pointers. "
            "Exercises must be solvable using only sequential statements and expressions."
        ),
        "conditionals and loops": (
            "ALLOWED constructs: if/else, switch, for, while, do-while, variables, operators. "
            "BANNED constructs: arrays, pointers, dynamic memory allocation."
        ),
        "arrays and strings": (
            "ALLOWED constructs: arrays, strings (char arrays), loops, conditionals, standard "
            "string.h / ctype.h functions, variables, operators. "
            "BANNED constructs: pointers, dynamic memory allocation (malloc/free)."
        ),
        "pointers and memory allocation": (
            "ALLOWED constructs: pointers, dynamic memory allocation (malloc/calloc/realloc/free), "
            "arrays, strings, loops, conditionals, variables, operators. "
            "All heap memory must be freed before the program exits."
        ),
    }

    @staticmethod
    def build_prompt(topic, num_tasks):
        task_instructions = """
TASK [number]:
TITLE: [A short, descriptive name for the problem]

DESCRIPTION:
Paragraph 1 (context): [2 to 3 sentences explaining the concept and a real-world motivation. Do not state the task yet. If the exercise involves a named algorithm or mathematical concept, define it here.]

Paragraph 2 (task): [A separate paragraph stating exactly what the program must do. Specify: what input is read from stdin (types, format, ranges), what to compute, and what to print to stdout. Include edge cases and constraints. Do NOT reveal the implementation strategy.]

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

        constraint = PromptBuilder.TOPIC_CONSTRAINTS.get(topic, "")

        prompt = f"""You are an expert C programming educator. Generate {num_tasks} C programming exercise(s) \
for the following topic: {topic}

Each exercise must be a complete stdin/stdout program that a student writes from scratch.
Use only standard C (C11) with headers from: stdio.h, stdlib.h, string.h, ctype.h, math.h.

TOPIC CONSTRAINT — {topic}: {constraint}

Follow this structure exactly for each exercise:

{task_instructions}

REQUIREMENTS:
1. Difficulty: introductory but NOT trivial. Every exercise must combine at least two ideas \
within the allowed constructs for this topic (e.g. multiple operators with intermediate values, \
a loop with a conditional inside, reading and transforming several inputs). \
A single arithmetic expression or a single if-else with no loop is too simple. \
Banned as stand-alone exercises: plain addition of two numbers, direct formula application \
(area = w*h), printing a fixed pattern. CRITICAL: only use constructs listed in the TOPIC \
CONSTRAINT above — do not introduce language features from later topics. \
Good bar: a student who has seen the concept once still needs to think for a few minutes. \
If generating multiple exercises, all must be at the same difficulty level — do not make \
the first exercise a warm-up and later ones harder, or vice versa. Each exercise should \
require a comparable amount of thought and a similar number of programming steps. \
Each exercise must be fully self-contained — it should be assignable to a different student \
independently, with no references to or reliance on any other exercise in the set.
2. DESCRIPTION must contain exactly two paragraphs separated by a blank line. \
Paragraph 1 (context): concept explanation and real-world motivation only — do not state the task. \
Paragraph 2 (task): stdin format, what to compute, stdout format, constraints, and edge cases — no implementation hints. \
NEVER merge these into one paragraph.
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