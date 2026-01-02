import inspect
from typing import Any, AsyncIterator
from mcp.server.fastmcp.server import StreamableHTTPASGIApp
from mcp.server.fastmcp.server import FastMCP
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
import mcp.types as types
from mcp.server.auth.settings import AuthSettings
from starlette.routing import Mount
import logging

logger = logging.getLogger(__name__)


class WantlyMCP:
    def __init__(self, server_name: str, instructions: str = None, *,
                tools: list[types.Tool] = None, debug: bool = False, auth: AuthSettings | None = None):
        self._fast_mcp = self._initialize_fast_mcp(server_name, instructions, tools, debug, auth)
        self._add_decorated_tools()
    
    def _initialize_fast_mcp(self, server_name: str, instructions: str, tools: list[types.Tool], debug: bool, auth: AuthSettings | None):
        fast_mcp = FastMCP(
            name=server_name,
            instructions=instructions,
            tools=tools,
            debug=debug,
            auth=auth,
            stateless_http=True,
        )
        return fast_mcp

    @property
    def session_manager(self) -> StreamableHTTPSessionManager:
        return self._fast_mcp.session_manager

    @property
    def server(self) -> Server:
        return self._fast_mcp._mcp_server

    def streamable_http_app(self) -> Starlette:
        return self._fast_mcp.streamable_http_app()

    def _add_decorated_tools(self):
        """Scan class member methods marked with @wantly_tool decorator and add them."""
        # Get all methods from the class and its base classes
        for name, method in inspect.getmembers(self.__class__, inspect.isfunction):
            # Skip private methods
            if name.startswith('_'):
                continue
            
            # Check if the method has the _wantly_tool_metadata attribute
            if hasattr(method, '_wantly_tool_metadata'):
                metadata = method._wantly_tool_metadata
                # Get the bound method from the instance
                bound_method = getattr(self, name)
                # Extract metadata parameters
                self._fast_mcp.add_tool(
                    bound_method,
                    name=metadata.get('name'),
                    title=metadata.get('title'),
                    description=metadata.get('description'),
                    annotations=metadata.get('annotations'),
                    icons=metadata.get('icons'),
                    meta=metadata.get('meta'),
                    structured_output=metadata.get('structured_output'),
                )