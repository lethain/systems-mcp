import os.path
import sys
from typing import Any, Dict, List, Optional, Union
from mcp.server.fastmcp import FastMCP

# files to include in the call to `load_systems_documentation`
DOCUMENTATION_FILES = ("./docs/readme.md", "./docs/examples.md")
DOC_CACHE = None


# Redirect debug prints to stderr
def debug_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Create MCP server
mcp = FastMCP("systems_mcp")

@mcp.tool()
async def run_systems_model(spec: str, rounds: int = 100) -> str:
    """Run a systems model and return output of list of dictionaries in JSON.
    
    Args:
        spec: The systems model specification
        rounds: Number of rounds to run (default: 100)
    """
    try:
        # Import here to avoid import errors if module is missing
        from systems.parse import parse
        
        debug_print(f"Running systems model for {rounds} rounds")
        
        # Parse the model and run it
        model = parse(spec)
        results = model.run(rounds=rounds)
        return results
    except Exception as e:
        debug_print(f"Error running systems model: {e}")
        return f"<div class='error'>Error running systems model: {str(e)}</div>"


@mcp.tool()
async def load_systems_documentation() -> str:
    """Load systems documentation, examples, and specification details to improve
    the models ability to generate specifications.
    
    Returns:
        Documentation and several examples of systems models
    """
    global DOC_CACHE
    if DOC_CACHE is None:
        DOC_CACHE = ""
        for rel_file_path in DOCUMENTATION_FILES:
            with open(os.path.abspath(rel_file_path), 'r') as fin:
                DOC_CACHE += fin.read() + "\n\n"

    return DOC_CACHE


if __name__ == "__main__":
    debug_print("Starting systems-mcp server")
    mcp.run(transport='stdio')
