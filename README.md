# systems-mcp

[systems-mcp](https://github.com/lethain/systems-mcp) is an MCP server for interacting with
the [`lethain:systems`](https://github.com/lethain/systems/) library for systems modeling.

It provides two tools:

* `run_sys_model` runs the `systems` specification of a systems model
* `load_sys_examples` ...

It is intended for running locally in conjunction with Claude Desktop or a similar tool.

## Usage


![Example of prompt for  using systems-mcp](docs/systems-mcp-prompt.png)


![Example of artifact for using the output of systems-mcp](docs/systems-mcp-artifact.png)




## Installation

These instructions describe installation for [Claude Desktop](https://claude.ai/download) on OS X.
It should work similarly on other platforms.

1. Install [Claude Desktop](https://claude.ai/download).
2. Clone [systems-mcp](https://github.com/lethain/systems-mcp) into
    a convenient location, I'm assuming `/Users/will/systems-mcp`
3. Make sure you have `uv` installed, you can [follow these instructions](https://modelcontextprotocol.io/quickstart/server)
4. Go to Cladue Desktop, Setting, Developer, and have it create your MCP config file.
    Then you want to update your `claude_desktop_config.json`.
    (Note that you should replace `will` with your user, e.g. the output of `whoami`.

        cd /Users/will/Library/Application Support/Claude
        vi claude_desktop_config.json

    Then add this section:

        {
          "mcpServers": {
            "systems": {
              "command": "uv",
              "args": [
                "--directory",
                "/Users/will/systems-mcp",
                "run",
                "main.py"
              ]
            }
          }
        }

5. Close Claude and reopen it.
6. It should work...


