"""
Response parser: extracts structured tasks from LLM responses (write-from-scratch only).
"""

import re


class ResponseParser:
    _FENCE = r"```(?:c|cpp)\s*(.+?)```"

    @staticmethod
    def parse_response(response_text):
        tasks = []
        task_blocks = re.split(r"TASK \d+:", response_text)
        task_blocks = [block.strip() for block in task_blocks if block.strip()]

        for block in task_blocks:
            try:
                task = ResponseParser._parse_task_block(block)
                if task.get("solution") and task.get("test_cases"):
                    tasks.append(task)
                else:
                    print(f"Task missing required fields: {task.get('title', 'Unknown')}")
                    print(f"Block preview: {block[:200]}...")
            except Exception as e:
                print(f"Error parsing task block: {e}")
                continue

        return tasks

    @staticmethod
    def _parse_task_block(block):
        task = {}

        title_match = re.search(r"TITLE:\s*(.+?)(?:\n|$)", block)
        task["title"] = title_match.group(1).strip() if title_match else "Untitled"

        desc_match = re.search(
            r"DESCRIPTION:\s*(.+?)(?=SOLUTION:|$)",
            block,
            re.DOTALL,
        )
        task["description"] = desc_match.group(1).strip() if desc_match else ""

        solution_match = re.search(
            r"SOLUTION:\s*" + ResponseParser._FENCE, block, re.DOTALL
        )
        if solution_match:
            task["solution"] = solution_match.group(1).strip()
        else:
            solution_alt = re.search(
                r"SOLUTION:\s*(.+?)(?=TEST_CASES:|---)", block, re.DOTALL
            )
            if solution_alt:
                task["solution"] = re.sub(
                    r"```(?:c|cpp)?", "", solution_alt.group(1)
                ).strip()
            else:
                task["solution"] = ""

        task["test_cases"] = ResponseParser._parse_test_cases(block)

        return task

    @staticmethod
    def _parse_test_cases(block):
        test_cases = []
        test_section = re.search(
            r"TEST_CASES:\s*(.+?)(?=---|TASK \d+:|$)", block, re.DOTALL
        )

        if test_section:
            test_text = test_section.group(1)
            pairs = re.findall(
                r"Input:\s*(.+?)\s*Expected Output:\s*(.+?)(?=Input:|$)",
                test_text,
                re.DOTALL,
            )

            for inp, out in pairs:
                test_cases.append(
                    {"input": inp.strip(), "expected_output": out.strip()}
                )

        return test_cases
