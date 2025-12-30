# MCP Utils

Utility library for creating and initializing MCP (Model Context Protocol) servers.

## Installation

### Using pip

```bash
pip install wantly-mcp-utils --extra-index-url https://europe-north2-python.pkg.dev/ancient-pipe-461512-m8/pypi/simple/
```

### Using uv (in pyproject.toml)

```toml
[project]
dependencies = [
    "wantly-mcp-utils>=0.3.0",
]

[[tool.uv.index]]
name = "pypi-gc"
url = "https://europe-north2-python.pkg.dev/ancient-pipe-461512-m8/pypi/simple"
```

Then run:
```bash
uv sync
```

## Usage

This package provides utilities for working with MCP servers, including:

- `mcp_creator.py` - Tools for creating MCP server instances
- `mcp_initializer.py` - Initialization utilities for MCP servers
- `WantlyMCPLowLevel` - Base class for building low level MCP implementations

## License

MIT

