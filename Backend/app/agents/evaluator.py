import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def run_tests(timeout_seconds: int = 60) -> dict:
    """
    Run pytest in the SkillBridge AI project directory.
    Only pytest is executed; no user-supplied shell commands are accepted.
    """

    timeout_seconds = max(5, min(timeout_seconds, 120))

    try:
        result = subprocess.run(
            ["uv", "run", "pytest", "-q"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            shell=False,
        )

        return {
            "status": "passed" if result.returncode == 0 else "failed",
            "return_code": result.returncode,
            "stdout": result.stdout[-5000:],
            "stderr": result.stderr[-3000:],
        }

    except subprocess.TimeoutExpired:
        return {
            "status": "timeout",
            "message": f"Tests exceeded the {timeout_seconds}-second time limit.",
        }

    except FileNotFoundError:
        return {
            "status": "error",
            "message": "Could not find uv. Ensure uv is installed and available in PATH.",
        }