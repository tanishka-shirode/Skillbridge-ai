from mcp.server import MCPServer

from Backend.app.agents.code_reviewer import review_code


def register_review_code_tool(mcp: MCPServer):
    @mcp.tool()
    def review_code_tool(code: str, language: str = "python") -> dict:
        """
        Review source code for basic syntax, security, and maintainability issues.
        Does not execute the submitted code.
        """
        return review_code(code, language)