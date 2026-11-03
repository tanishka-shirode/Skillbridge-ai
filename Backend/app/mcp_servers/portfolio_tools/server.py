from mcp.server import MCPServer

from Backend.app.mcp_servers.portfolio_tools.generate_portfolio_content import (
    register_generate_portfolio_tool,
)

mcp = MCPServer("skillbridge-portfolio-tools")

register_generate_portfolio_tool(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")