import os
import sys
import io
import base64
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
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
        from IPython.core.display import HTML
        
        debug_print(f"Running systems model for {rounds} rounds")
        
        # Parse the model and run it
        model = parse(spec)
        results = model.run(rounds=rounds)
        
        # Render as HTML table
        rendered = model.render_html(results)
        
        return rendered
    except Exception as e:
        debug_print(f"Error running systems model: {e}")
        return f"<div class='error'>Error running systems model: {str(e)}</div>"

@mcp.tool()
async def render_sys_model(spec: str, rounds: int = 100, columns: Optional[List[str]] = None, 
                           title: Optional[str] = None) -> str:
    """Generate a visualization of a systems model run as an image.
    
    Args:
        spec: The systems model specification
        rounds: Number of rounds to run (default: 100)
        columns: Optional list of columns/stocks to include (default: all)
        title: Optional title for the chart (default: none)
    """
    try:
        # Import here to avoid import errors if module is missing
        from systems.parse import parse
        import matplotlib.pyplot as plt
        import base64
        from io import BytesIO
        
        debug_print(f"Rendering systems model chart for {rounds} rounds")
        
        # Parse the model and run it
        model = parse(spec)
        results = model.run(rounds=rounds)
        
        # Prepare the data for plotting
        if columns is None:
            # Use all stocks if no columns specified
            # Get column names from the first result
            if results and len(results) > 0:
                columns = list(results[0].keys())
            else:
                columns = []
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot each stock as a line
        for column in columns:
            values = [result.get(column, 0) for result in results]
            ax.plot(values, label=column)
        
        # Set labels and title
        ax.set_xlabel('Rounds')
        ax.set_ylabel('Stock Value')
        if title:
            ax.set_title(title)
        
        # Add legend
        ax.legend()
        
        # Convert plot to base64 encoded image
        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close(fig)
        
        # Encode the image as base64
        encoded = base64.b64encode(image_png).decode('utf-8')
        html_img = f'<img src="data:image/png;base64,{encoded}" />'
        
        return html_img
    except Exception as e:
        debug_print(f"Error rendering systems model: {e}")
        return f"<div class='error'>Error rendering systems model: {str(e)}</div>"

@mcp.tool()
async def visualize_sys_model(spec: str) -> str:
    """Generate a Graphviz visualization of a systems model.
    
    Args:
        spec: The systems model specification
    """
    try:
        # Import here to avoid import errors if module is missing
        from systems.parse import parse
        from systems.viz import as_dot
        import base64
        from io import BytesIO
        import subprocess
        
        debug_print("Generating system model visualization")
        
        # Parse the model
        model = parse(spec)
        
        # Get the DOT representation
        dot_code = as_dot(model)
        
        # Try to render with Graphviz if available
        try:
            # Use subprocess to call dot
            process = subprocess.Popen(
                ['dot', '-Tpng'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate(dot_code.encode('utf-8'))
            
            if process.returncode != 0:
                debug_print(f"Graphviz error: {stderr.decode('utf-8')}")
                return f"<pre>{dot_code}</pre><p>Error rendering graph with Graphviz</p>"
            
            # Encode the image
            encoded = base64.b64encode(stdout).decode('utf-8')
            return f'<img src="data:image/png;base64,{encoded}" />'
        except FileNotFoundError:
            # Fallback to returning the DOT code if Graphviz is not installed
            debug_print("Graphviz not found, returning DOT code")
            return f"<pre>{dot_code}</pre><p>Install Graphviz to render this diagram</p>"
            
    except Exception as e:
        debug_print(f"Error visualizing systems model: {e}")
        return f"<div class='error'>Error visualizing systems model: {str(e)}</div>"

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
- `run_sys_model` to see the numerical results
- `render_sys_model` to visualize the stock values over time
- `visualize_sys_model` to see the system structure"""
    
    return output

if __name__ == "__main__":
    debug_print("Starting systems-mcp server")
    mcp.run(transport='stdio')