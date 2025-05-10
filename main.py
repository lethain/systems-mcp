import sys
from typing import Any, Dict, List, Optional, Union
from mcp.server.fastmcp import FastMCP

# Redirect debug prints to stderr
def debug_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# Create MCP server
mcp = FastMCP("systems_mcp")

@mcp.tool()
async def run_sys_model(spec: str, rounds: int = 100) -> str:
    """Run a systems model and return HTML table output.
    
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
async def provide_system_example() -> str:
    """Provide an example systems model specification.
    
    Returns:
        An example systems model that can be used with the other functions
    """
    examples = [
        {
            "name": "Basic Stock Flow",
            "description": "A simple stock and flow example",
            "spec": """# Basic Stock Flow Example
Start(100)
Start > Middle @ 10
Middle > End @ 5"""
        },
        {
            "name": "Hiring Pipeline",
            "description": "A model of a company hiring pipeline",
            "spec": """# Hiring Pipeline Model
# Candidates flow through the hiring process
[Candidates] > PhoneScreens @ 25
PhoneScreens > Onsites @ Conversion(0.5)
Onsites > Offers @ Conversion(0.5)
Offers > Hires @ Conversion(0.7)
Hires > Employees @ Conversion(0.9)
Employees(5)
Employees > Departures @ Leak(0.05)"""
        },
        {
            "name": "Customer Acquisition and Churn",
            "description": "Model of customer acquisition and retention",
            "spec": """# Customer Acquisition and Churn Model
# User Acquisition Flow
[PotentialCustomers] > EngagedCustomers @ 100
# Initial Integration Flow
EngagedCustomers > IntegratedCustomers @ Leak(0.5)
# Baseline Churn Flow
IntegratedCustomers > ChurnedCustomers @ Leak(0.1)
# Experience Deprecation Flow
IntegratedCustomers > DeprecationImpactedCustomers @ Leak(0.5)
# Reintegrated Flow
DeprecationImpactedCustomers > IntegratedCustomers @ Leak(0.9)
# Deprecation-Influenced Churn
DeprecationImpactedCustomers > ChurnedCustomers @ Leak(0.1)"""
        }
    ]
    
    # Choose one example at random
    import random
    example = random.choice(examples)
    
    output = f"""# {example['name']}
# {example['description']}

```
{example['spec']}
```

You can use this example with the other systems-mcp functions:
- `run_sys_model` to see the numerical results"""
    
    return output

if __name__ == "__main__":
    debug_print("Starting systems-mcp server")
    mcp.run(transport='stdio')
