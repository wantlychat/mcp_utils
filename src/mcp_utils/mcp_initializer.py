from typing import Callable, Any, Dict, List
from mcp.server.fastmcp import FastMCP


def mcp_initializer(name: str, instructions: str = None):
    """
    Decorator that marks a function as an MCP initializer.
    
    Args:
        name: The name of the MCP
        instructions: Optional instructions for the MCP
        
    Returns:
        Decorated function with MCP initializer metadata
    """
    def decorator(func: Callable) -> Callable:
        # Store MCP metadata in a dictionary
        func._mcp_metadata = {
            'name': name,
            'instructions': instructions
        }
        func._is_mcp_initializer = True
        
        return func
    return decorator


def get_mcp_initializers(module) -> List[Dict[str, Any]]:
    """
    Get all MCP initializers from a module.
    
    Args:
        module: The module to search for MCP initializers
        
    Returns:
        List of dictionaries containing MCP initializer information
    """
    initializers = []
    
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if (callable(attr) and 
            hasattr(attr, '_is_mcp_initializer') and 
            attr._is_mcp_initializer):
            initializers.append({
                'name': attr._mcp_metadata['name'],
                'instructions': attr._mcp_metadata['instructions'],
                'function': attr,
                'function_name': attr_name
            })
    
    return initializers


def is_mcp_initializer(func: Callable) -> bool:
    """
    Check if a function is marked as an MCP initializer.
    
    Args:
        func: The function to check
        
    Returns:
        True if the function is an MCP initializer, False otherwise
    """
    return (hasattr(func, '_is_mcp_initializer') and 
            func._is_mcp_initializer)
