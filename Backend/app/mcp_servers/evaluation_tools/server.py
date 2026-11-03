from mcp.server import MCPServer

from Backend.app.mcp_servers.evaluation_tools.review_code import (
    register_review_code_tool,
)

mcp = MCPServer("skillbridge-evaluation-tools")

register_review_code_tool(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")