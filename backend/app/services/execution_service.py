import os
import sys
import time
import subprocess
import tempfile
import json
from typing import List, Dict, Any, Optional

class ExecutionService:
    @staticmethod
    def run_isolated(
        language: str,
        code: str,
        test_cases: List[Dict[str, Any]],
        timeout_seconds: float = 3.0
    ) -> Dict[str, Any]:
        """
        Executes code safely against test cases in an isolated sandbox directory.
        Never touches the parent app process state.
        """
        lang = language.lower()
        if lang not in ["python", "java"]:
            return {
                "status": "Error",
                "stdout": "",
                "stderr": f"Unsupported language '{language}'. Supported: Python, Java.",
                "runtime_ms": 0.0,
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "test_results": []
            }

        if lang == "python":
            return ExecutionService._run_python(code, test_cases, timeout_seconds)
        else:
            return ExecutionService._run_java(code, test_cases, timeout_seconds)

    @staticmethod
    def _run_python(code: str, test_cases: List[Dict[str, Any]], timeout_seconds: float) -> Dict[str, Any]:
        results = []
        total_runtime_ms = 0.0
        passed_count = 0
        overall_status = "Success"
        overall_stdout = ""
        overall_stderr = ""

        with tempfile.TemporaryDirectory() as temp_dir:
            for idx, tc in enumerate(test_cases, 1):
                inp = str(tc.get("input", "")).strip()
                expected = str(tc.get("expected_output", "")).strip()
                
                # Harness wrapper to supply input and catch stdout
                script_path = os.path.join(temp_dir, f"solution_{idx}.py")
                with open(script_path, "w", encoding="utf-8") as f:
                    f.write(code)

                start_time = time.perf_counter()
                try:
                    proc = subprocess.run(
                        [sys.executable, script_path],
                        input=inp,
                        text=True,
                        capture_output=True,
                        timeout=timeout_seconds,
                        cwd=temp_dir
                    )
                    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
                    total_runtime_ms += elapsed_ms
                    
                    stdout = proc.stdout.strip()
                    stderr = proc.stderr.strip()
                    
                    if proc.returncode != 0:
                        overall_status = "Runtime Error"
                        overall_stderr += f"\n[Case {idx}] {stderr}"
                        results.append({
                            "test_case_id": idx,
                            "input": inp,
                            "expected_output": expected,
                            "actual_output": stdout,
                            "passed": False,
                            "error": stderr or f"Process exited with code {proc.returncode}",
                            "runtime_ms": elapsed_ms
                        })
                    else:
                        is_match = (stdout == expected) or (stdout.replace(" ", "") == expected.replace(" ", ""))
                        if is_match:
                            passed_count += 1
                        else:
                            if overall_status == "Success":
                                overall_status = "Wrong Answer"
                        
                        results.append({
                            "test_case_id": idx,
                            "input": inp,
                            "expected_output": expected,
                            "actual_output": stdout,
                            "passed": is_match,
                            "error": None,
                            "runtime_ms": elapsed_ms
                        })
                        if not overall_stdout and stdout:
                            overall_stdout = stdout
                except subprocess.TimeoutExpired:
                    overall_status = "Time Limit Exceeded"
                    overall_stderr += f"\n[Case {idx}] Time limit exceeded ({timeout_seconds}s)"
                    results.append({
                        "test_case_id": idx,
                        "input": inp,
                        "expected_output": expected,
                        "actual_output": "",
                        "passed": False,
                        "error": f"Execution timed out after {timeout_seconds}s. Check for infinite loops or non-terminating recursions.",
                        "runtime_ms": timeout_seconds * 1000
                    })
                except Exception as e:
                    overall_status = "Error"
                    overall_stderr += f"\n[Case {idx}] {str(e)}"
                    results.append({
                        "test_case_id": idx,
                        "input": inp,
                        "expected_output": expected,
                        "actual_output": "",
                        "passed": False,
                        "error": str(e),
                        "runtime_ms": 0.0
                    })

        avg_runtime = round(total_runtime_ms / max(1, len(test_cases)), 2)
        if passed_count == len(test_cases) and overall_status == "Success":
            final_status = "Accepted"
        else:
            final_status = overall_status if overall_status != "Success" else "Wrong Answer"

        return {
            "status": final_status,
            "stdout": overall_stdout,
            "stderr": overall_stderr.strip(),
            "runtime_ms": avg_runtime,
            "passed_tests": passed_count,
            "total_tests": len(test_cases),
            "test_results": results
        }

    @staticmethod
    def _run_java(code: str, test_cases: List[Dict[str, Any]], timeout_seconds: float) -> Dict[str, Any]:
        results = []
        total_runtime_ms = 0.0
        passed_count = 0
        overall_status = "Success"
        overall_stdout = ""
        overall_stderr = ""

        with tempfile.TemporaryDirectory() as temp_dir:
            # Java expects class Solution or Main
            class_name = "Solution"
            if "class Main" in code:
                class_name = "Main"
            
            src_path = os.path.join(temp_dir, f"{class_name}.java")
            with open(src_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Check if javac is installed
            try:
                compile_proc = subprocess.run(
                    ["javac", src_path],
                    capture_output=True,
                    text=True,
                    timeout=5.0,
                    cwd=temp_dir
                )
                if compile_proc.returncode != 0:
                    return {
                        "status": "Compile Error",
                        "stdout": "",
                        "stderr": compile_proc.stderr,
                        "runtime_ms": 0.0,
                        "passed_tests": 0,
                        "total_tests": len(test_cases),
                        "test_results": [
                            {
                                "test_case_id": i + 1,
                                "input": tc.get("input", ""),
                                "expected_output": tc.get("expected_output", ""),
                                "actual_output": "",
                                "passed": False,
                                "error": compile_proc.stderr,
                                "runtime_ms": 0.0
                            }
                            for i, tc in enumerate(test_cases)
                        ]
                    }
            except FileNotFoundError:
                # Java runtime not installed on host - provide clear educational message
                return {
                    "status": "Environment Notice",
                    "stdout": "",
                    "stderr": "Java SDK (javac) is not installed in this environment path. Python execution is fully active.",
                    "runtime_ms": 0.0,
                    "passed_tests": 0,
                    "total_tests": len(test_cases),
                    "test_results": []
                }

            # Run compiled bytecode
            for idx, tc in enumerate(test_cases, 1):
                inp = str(tc.get("input", "")).strip()
                expected = str(tc.get("expected_output", "")).strip()

                start_time = time.perf_counter()
                try:
                    proc = subprocess.run(
                        ["java", "-cp", temp_dir, class_name],
                        input=inp,
                        text=True,
                        capture_output=True,
                        timeout=timeout_seconds,
                        cwd=temp_dir
                    )
                    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
                    total_runtime_ms += elapsed_ms
                    stdout = proc.stdout.strip()
                    stderr = proc.stderr.strip()

                    if proc.returncode != 0:
                        overall_status = "Runtime Error"
                        results.append({
                            "test_case_id": idx,
                            "input": inp,
                            "expected_output": expected,
                            "actual_output": stdout,
                            "passed": False,
                            "error": stderr,
                            "runtime_ms": elapsed_ms
                        })
                    else:
                        is_match = (stdout == expected) or (stdout.replace(" ", "") == expected.replace(" ", ""))
                        if is_match:
                            passed_count += 1
                        else:
                            if overall_status == "Success":
                                overall_status = "Wrong Answer"
                        results.append({
                            "test_case_id": idx,
                            "input": inp,
                            "expected_output": expected,
                            "actual_output": stdout,
                            "passed": is_match,
                            "error": None,
                            "runtime_ms": elapsed_ms
                        })
                except subprocess.TimeoutExpired:
                    overall_status = "Time Limit Exceeded"
                    results.append({
                        "test_case_id": idx,
                        "input": inp,
                        "expected_output": expected,
                        "actual_output": "",
                        "passed": False,
                        "error": f"Java execution timed out after {timeout_seconds}s.",
                        "runtime_ms": timeout_seconds * 1000
                    })

        avg_runtime = round(total_runtime_ms / max(1, len(test_cases)), 2)
        if passed_count == len(test_cases) and overall_status == "Success":
            final_status = "Accepted"
        else:
            final_status = overall_status if overall_status != "Success" else "Wrong Answer"

        return {
            "status": final_status,
            "stdout": overall_stdout,
            "stderr": overall_stderr.strip(),
            "runtime_ms": avg_runtime,
            "passed_tests": passed_count,
            "total_tests": len(test_cases),
            "test_results": results
        }
