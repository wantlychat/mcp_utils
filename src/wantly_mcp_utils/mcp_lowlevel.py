
from abc import ABC, abstractmethod
import contextlib
from typing import Any, AsyncIterator
from mcp.server.fastmcp.server import StreamableHTTPASGIApp
from mcp.server.lowlevel import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
import mcp.types as types
from starlette.routing import Mount
import logging

logger = logging.getLogger(__name__)


class WantlyMCPLowLevel(ABC):
    def __init__(self, server_name: str, instructions: str, debug: bool = False):
        self._server_name = server_name
        self._instructions = instructions
        self._debug = debug
        self.server: Server | None = None
        self._session_manager: StreamableHTTPSessionManager | None = None
        self._initialize_server()

    def _initialize_server(self):
        self.server = Server(name=self._server_name, instructions=self._instructions)
        @self.server.list_tools()
        async def list_tools() -> list[types.Tool]:
            return await self.list_tools()
        
        @self.server.call_tool()
        async def call_tool(tool_name: str, arguments: dict[str, Any]) -> list[types.ContentBlock]:
            return await self.call_tool(tool_name, arguments)

    @property
    def session_manager(self) -> StreamableHTTPSessionManager:
        """Get the StreamableHTTP session manager.

        This is exposed to enable advanced use cases like mounting multiple
        FastMCP servers in a single FastAPI application.

        Raises:
            RuntimeError: If called before streamable_http_app() has been called.
        """
        if self._session_manager is None:  # pragma: no cover
            raise RuntimeError(
                "Session manager can only be accessed after"
                "calling streamable_http_app()."
                "The session manager is created lazily"
                "to avoid unnecessary initialization."
            )
        return self._session_manager  # pragma: no cover

    async def streamable_http_app(self) -> Starlette:
        if not self.server:
            raise ValueError("Server not initialized")
        json_response = False
        # Create the session manager with true stateless mode
        self._session_manager = StreamableHTTPSessionManager(
            app=self.server,
            event_store=None,
            json_response=json_response,
            stateless=True,
        )

        streamable_http_app = StreamableHTTPASGIApp(self._session_manager)

        @contextlib.asynccontextmanager
        async def lifespan(app: Starlette) -> AsyncIterator[None]:
            """Context manager for session manager."""
            async with self._session_manager.run():
                logger.info(f"Application {self._server_name} started with StreamableHTTP session manager!")
                try:
                    yield
                finally:
                    logger.info(f"Application {self._server_name} shutting down...")

        # Create an ASGI application using the transport
        starlette_app = Starlette(
            debug=self._debug,
            routes=[
                Mount("/mcp", app=streamable_http_app),
            ],
            lifespan=lifespan,
        )
        return starlette_app
        
    @abstractmethod
    async def list_tools(self) -> list[types.Tool]:
        ...
    
    @abstractmethod
    async def call_tool(self, tool_name: str, arguments: dict[str, Any]) -> list[types.ContentBlock]:
        ...
    