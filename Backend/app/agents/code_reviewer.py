import ast
import re


def review_code(code: str, language: str = "python") -> dict:
    """
    Review source code for basic bugs, readability, and security concerns.
    This performs static checks only; it does not execute the submitted code.
    """

    findings = []

    if not code.strip():
        return {
            "language": language,
            "summary": "No code was provided.",
            "findings": [],
            "suggestions": ["Provide source code to review."]
        }

    if language.lower() == "python":
        try:
            ast.parse(code)
        except SyntaxError as error:
            findings.append({
                "category": "Syntax",
                "severity": "high",
                "line": error.lineno,
                "issue": error.msg,
                "suggestion": "Fix the syntax error before running the code."
            })

        checks = [
            (
                r"\beval\s*\(",
                "Security",
                "high",
                "Use of eval() can execute arbitrary expressions.",
                "Avoid eval(); use safer parsing or explicit logic."
            ),
            (
                r"\bexec\s*\(",
                "Security",
                "high",
                "Use of exec() can execute arbitrary code.",
                "Avoid exec() for untrusted or dynamic input."
            ),
            (
                r"\bexcept\s*:",
                "Reliability",
                "medium",
                "Bare except catches all exceptions, including system-exiting exceptions.",
                "Catch specific exception types."
            ),
            (
                r"\bprint\s*\(",
                "Maintainability",
                "low",
                "print() statements may be leftover debugging output.",
                "Use logging for application diagnostics."
            ),
        ]

        for pattern, category, severity, issue, suggestion in checks:
            for match in re.finditer(pattern, code):
                line = code.count("\n", 0, match.start()) + 1
                findings.append({
                    "category": category,
                    "severity": severity,
                    "line": line,
                    "issue": issue,
                    "suggestion": suggestion
                })

    else:
        findings.append({
            "category": "Scope",
            "severity": "low",
            "line": None,
            "issue": f"Basic static checks are not configured for {language}.",
            "suggestion": "Use Python for the currently supported checks."
        })

    if not findings:
        summary = "No issues found by the basic static checks."
    else:
        summary = f"Found {len(findings)} potential issue(s). Review the findings below."

    return {
        "language": language,
        "summary": summary,
        "findings": findings,
        "suggestions": [
            "Review each finding in context.",
            "Run tests and linting tools before accepting the code."
        ]
    }