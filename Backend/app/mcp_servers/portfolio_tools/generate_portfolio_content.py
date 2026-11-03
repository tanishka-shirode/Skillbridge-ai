from mcp.server import MCPServer

from Backend.app.agents.portfolio_agent import generate_portfolio_content


def register_generate_portfolio_tool(mcp: MCPServer):
    @mcp.tool()
    def generate_portfolio_tool(
        project_name: str,
        project_description: str,
        technologies: list[str],
        features: list[str],
        role: str = "Developer",
    ) -> dict:
        """
        Generate a project summary, README content, resume bullets,
        and demonstrated skills from project details.
        """
        return generate_portfolio_content(
            project_name=project_name,
            project_description=project_description,
            technologies=technologies,
            features=features,
            role=role,
        )