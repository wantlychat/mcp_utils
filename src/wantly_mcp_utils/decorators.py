from typing import Any, Callable, Optional, TypeVar

# Type variable for function types
F = TypeVar('F', bound=Callable[..., Any])


def wantly_tool(
    name: str | None = None,
    title: str | None = None,
    description: str | None = None,
    annotations: Any | None = None,
    icons: list[Any] | None = None,
    meta: dict[str, Any] | None = None,
    structured_output: bool | None = None,
) -> Callable[[F], F]:
    """Decorator to register a tool.

    Tools can optionally request a Context object by adding a parameter with the
    Context type annotation. The context provides access to MCP capabilities like
    logging, progress reporting, and resource access.

    Args:
        name: Optional name for the tool (defaults to function name)
        title: Optional human-readable title for the tool
        description: Optional description of what the tool does
        annotations: Optional ToolAnnotations providing additional tool information
        icons: Optional list of Icon objects
        meta: Optional dictionary for additional metadata
        structured_output: Controls whether the tool's output is structured or unstructured
            - If None, auto-detects based on the function's return type annotation
            - If True, creates a structured tool (return type annotation permitting)
            - If False, unconditionally creates an unstructured tool

    Example:
        @wantly_tool()
        def my_tool(x: int) -> str:
            return str(x)

        @wantly_tool(name="custom_tool", description="A custom tool")
        def my_tool(x: int) -> str:
            return str(x)
    """
    # Check if user passed function directly instead of calling decorator
    if callable(name):
        raise TypeError(
            "The @wantly_tool decorator was used incorrectly. Did you forget to call it? Use @wantly_tool() instead of @wantly_tool"
        )
    
    # Collect all parameters into metadata dictionary
    metadata: dict[str, Any] = {}
    if name is not None:
        metadata["name"] = name
    if title is not None:
        metadata["title"] = title
    if description is not None:
        metadata["description"] = description
    if annotations is not None:
        metadata["annotations"] = annotations
    if icons is not None:
        metadata["icons"] = icons
    if meta is not None:
        metadata["meta"] = meta
    if structured_output is not None:
        metadata["structured_output"] = structured_output
    
    def decorator(func: F) -> F:
        # Set the metadata attribute on the function
        func._wantly_tool_metadata = metadata
        return func
    
    return decorator

