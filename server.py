import json
import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

from BE import CTaskGenerator

app = Flask(__name__)
CORS(app)

generator = None
current_provider = None


def _env_key_for_provider(provider: str):
    p = (provider or "").lower()
    if p == "gemini":
        return os.getenv("GEMINI_API_KEY", "")
    if p == "claude":
        return os.getenv("ANTHROPIC_API_KEY", "")
    if p == "gpt":
        return os.getenv("OPENAI_API_KEY", "")
    return ""


def _create_generator_from_env():
    order = [
        ("gemini", os.getenv("GEMINI_API_KEY", "")),
        ("gpt", os.getenv("OPENAI_API_KEY", "")),
        ("claude", os.getenv("ANTHROPIC_API_KEY", "")),
    ]
    for prov, key in order:
        if key:
            return prov, CTaskGenerator(prov, key)
    return None, None


def _resolve_generator(body):
    """Use per-request provider/api_key if present; else env for that provider; else saved global."""
    global generator, current_provider

    prov = (body.get("provider") or "").strip().lower() or None
    key = (body.get("api_key") or "").strip() or None

    if prov and key:
        return CTaskGenerator(prov, key), prov

    if prov and not key:
        k = _env_key_for_provider(prov)
        if k:
            return CTaskGenerator(prov, k), prov
        if generator and current_provider == prov:
            return generator, current_provider
        return None, None

    if generator:
        return generator, current_provider

    return None, None


def _task_payload(task):
    vr = task.get("test_results") or {}
    return {
        "title": task.get("title"),
        "description": task.get("description"),
        "buggy_code": task.get("buggy_code"),
        "code_with_blanks": task.get("code_with_blanks"),
        "solution": task.get("solution"),
        "test_cases": task.get("test_cases"),
        "validation": vr,
        "valid": bool(task.get("valid", vr.get("all_passed"))),
    }


current_provider, generator = _create_generator_from_env()
if generator:
    print(f"Initialized C task generator (provider: {current_provider}) from environment.")


@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "generator_ready": generator is not None,
            "provider": current_provider,
        }
    )


@app.route("/api/config", methods=["POST"])
def set_api_key():
    global generator, current_provider
    data = request.json or {}
    api_key = (data.get("api_key") or "").strip()
    provider = (data.get("provider") or "gemini").strip().lower()

    if provider not in ("gemini", "claude", "gpt"):
        return jsonify({"error": "provider must be gemini, claude, or gpt"}), 400

    if not api_key:
        return jsonify({"error": "API key required"}), 400

    try:
        generator = CTaskGenerator(provider, api_key)
        current_provider = provider
        return jsonify(
            {
                "message": "API configured successfully",
                "provider": current_provider,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate", methods=["POST"])
def generate_tasks():
    data = request.json or {}
    gen, used_provider = _resolve_generator(data)

    if not gen:
        return jsonify(
            {
                "error": "No API key configured. POST /api/config with provider and api_key, "
                "or set GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY, "
                "or pass provider and api_key with the generate request.",
            }
        ), 400

    topic = data.get("topic")
    task_type = data.get("task_type")
    num_tasks = data.get("num_tasks", 1)

    if not topic or not task_type:
        return jsonify({"error": "topic and task_type are required"}), 400

    try:
        all_tasks = gen.generate_tasks(topic, task_type, num_tasks)

        research_filename = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("generated_tasks", exist_ok=True)
        gen.save_to_json(
            all_tasks, filename=os.path.join("generated_tasks", research_filename)
        )

        valid_count = sum(1 for t in all_tasks if t.get("valid"))
        invalid_count = len(all_tasks) - valid_count
        tasks_out = [_task_payload(t) for t in all_tasks]

        return jsonify(
            {
                "success": True,
                "provider": used_provider,
                "total_generated": len(all_tasks),
                "valid_count": valid_count,
                "invalid_count": invalid_count,
                "tasks": tasks_out,
            }
        )

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/files", methods=["GET"])
def list_files():
    try:
        files_dir = "generated_tasks"
        if not os.path.exists(files_dir):
            return jsonify({"files": []})

        files = [f for f in os.listdir(files_dir) if f.endswith(".json")]
        files.sort(reverse=True)
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/files/<filename>", methods=["GET"])
def get_file(filename):
    try:
        filepath = os.path.join("generated_tasks", filename)
        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404

        with open(filepath, encoding="utf-8") as f:
            file_data = json.load(f)
        return jsonify(file_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
