from mcp.server import MCPServer

from Backend.app.agents.evaluator import run_tests


def register_run_tests_tool(mcp: MCPServer):
    @mcp.tool()
    def run_tests_tool(timeout_seconds: int = 60) -> dict:
        """
        Run the project's pytest suite and return the test results.
        """
        return run_tests(timeout_seconds)