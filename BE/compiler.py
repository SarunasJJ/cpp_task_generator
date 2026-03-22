import os
import subprocess
import tempfile


class Compiler:
    """Compile and run C solutions (gcc, C11)."""

    @staticmethod
    def compile_and_test(c_code, test_cases):
        results = {
            "compiled": False,
            "compilation_error": None,
            "test_results": [],
            "all_passed": False,
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            c_file = os.path.join(tmpdir, "solution.c")
            exe_file = os.path.join(tmpdir, "solution")
            if os.name == "nt":
                exe_file = os.path.join(tmpdir, "solution.exe")

            with open(c_file, "w", encoding="utf-8") as f:
                f.write(c_code)

            compile_success = Compiler._compile(c_file, exe_file, results)
            if not compile_success:
                return results

            results["compiled"] = True

            all_passed = Compiler._run_tests(exe_file, test_cases, results)
            results["all_passed"] = all_passed

        return results

    @staticmethod
    def _compile(c_file, exe_file, results):
        try:
            compile_result = subprocess.run(
                ["gcc", c_file, "-o", exe_file, "-std=c11", "-Wall"],
                capture_output=True,
                text=True,
                timeout=15,
            )

            if compile_result.returncode != 0:
                err = compile_result.stderr or compile_result.stdout or "Compilation failed"
                results["compilation_error"] = err
                return False

            return True

        except FileNotFoundError:
            results["compilation_error"] = (
                "gcc not found. Install a C compiler (e.g. MinGW-w64 on Windows) and ensure gcc is on PATH."
            )
            return False
        except subprocess.TimeoutExpired:
            results["compilation_error"] = "Compilation timeout"
            return False
        except Exception as e:
            results["compilation_error"] = str(e)
            return False

    @staticmethod
    def _run_tests(exe_file, test_cases, results):
        all_passed = True

        for i, test_case in enumerate(test_cases):
            test_result = {
                "test_number": i + 1,
                "input": test_case["input"],
                "expected": test_case["expected_output"],
                "actual": None,
                "passed": False,
                "error": None,
            }

            try:
                run_result = subprocess.run(
                    [exe_file],
                    input=test_case["input"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )

                test_result["actual"] = run_result.stdout.strip()
                expected_clean = test_case["expected_output"].strip()
                actual_clean = run_result.stdout.strip()

                test_result["passed"] = expected_clean == actual_clean

                if not test_result["passed"]:
                    all_passed = False

            except subprocess.TimeoutExpired:
                test_result["error"] = "Execution timeout"
                all_passed = False
            except Exception as e:
                test_result["error"] = str(e)
                all_passed = False

            results["test_results"].append(test_result)

        return all_passed
