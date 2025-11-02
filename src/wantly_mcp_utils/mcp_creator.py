from typing import Protocol
from mcp.server.fastmcp import FastMCP


class MCPCreator(Protocol):
    def create_protected_mcp(self, name: str, instructions: str = None, **kwargs) -> FastMCP:
        ...

_mcp_creator: MCPCreator = None

def create_protected_mcp(name: str, instructions: str = None, **kwargs) -> FastMCP:
    """Create a protected MCP server.

    The MCP server will require authentication and will be protected by the auth server.

    Args:
        name: The name of the MCP.
        instructions: The instructions for the MCP.
    Returns:
        A protected MCP server.

    """

    if _mcp_creator is None:
        raise ValueError("MCP creator not initialized")
    return _mcp_creator.create_protected_mcp(name, instructions, **kwargs)

def set_mcp_creator(mcp_creator: MCPCreator):
    global _mcp_creator
    _mcp_creator = mcp_creator
