import json
from datetime import datetime

from .llm_client import LLMClient, LLMClientError
from .prompt_builder import PromptBuilder
from .parser import ResponseParser
from .compiler import Compiler


class CTaskGenerator:
    """Generates and validates C programming exercises using a configurable LLM provider."""

    def __init__(self, provider: str, api_key: str):
        self.provider = (provider or "").strip().lower()
        self._llm = LLMClient(self.provider, api_key)

    def generate_tasks(self, topic, task_type, num_tasks=1):
        print(f"\n{'='*60}")
        print(f"Generating {num_tasks} C task(s) via {self.provider}...")
        print(f"Topic: {topic} | Type: {task_type}")
        print(f"{'='*60}\n")

        prompt = PromptBuilder.build_prompt(topic, task_type, num_tasks)

        try:
            response_text = self._llm.generate_text(prompt)
            tasks = ResponseParser.parse_response(response_text)

            if not tasks:
                print("Failed to parse any tasks from response")
                return []

            print(f"Parsed {len(tasks)} tasks\n")

            return self._validate_tasks(tasks)

        except LLMClientError as e:
            print(f"Error generating tasks: {e}")
            return []
        except Exception as e:
            print(f"Error generating tasks: {e}")
            return []

    def _validate_tasks(self, tasks):
        validated_tasks = []
        for i, task in enumerate(tasks, 1):
            test_results = Compiler.compile_and_test(task["solution"], task["test_cases"])
            task["test_results"] = test_results
            task["valid"] = bool(test_results.get("all_passed"))

            validated_tasks.append(task)

            if test_results["all_passed"]:
                print(f"Task {i} validated successfully!")
            else:
                print(f"Task {i} failed validation - kept for review.")

        return validated_tasks

    def save_to_json(self, tasks, filename="research_tasks.json"):
        output = {
            "generated_at": datetime.now().isoformat(),
            "provider": self.provider,
            "num_tasks": len(tasks),
            "tasks": [],
        }
        for task in tasks:
            task_data = {
                "title": task.get("title"),
                "description": task.get("description"),
                "buggy_code": task.get("buggy_code"),
                "code_with_blanks": task.get("code_with_blanks"),
                "solution": task.get("solution"),
                "test_cases": task.get("test_cases"),
                "validation": task.get("test_results"),
                "valid": task.get("valid"),
            }
            output["tasks"].append(task_data)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)


# Backwards compatibility
CPPTaskGenerator = CTaskGenerator
