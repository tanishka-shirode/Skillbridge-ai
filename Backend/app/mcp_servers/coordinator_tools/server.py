from mcp.server import MCPServer

from Backend.app.mcp_servers.coordinator_tools.run_learning_workflow import (
    register_learning_workflow_tool,
)

mcp = MCPServer("skillbridge-coordinator-tools")

register_learning_workflow_tool(mcp)

if __name__ == "__main__":
    mcp.run(transport="stdio")