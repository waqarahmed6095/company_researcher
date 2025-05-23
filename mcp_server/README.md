# MCP Server - Company Researcher

## Installation

First, install the required dependencies:

```bash
pip install mcp[cli]
```

## Running the Server

To start the server, run:

```bash
python .\mcp_server\server.py
```

## Running the Client

To start the client, run:

```bash
python .\mcp_server\client.py
```

## Cursor Integration

For integration with Cursor, first run the server:

```bash
python .\mcp_server\server.py
```

Then use the following configuration in your Cursor settings:

```json
{
  "mcpServers": {
    "company-researcher-mcp": {
      "url": "http://localhost:8000/sse",
      "env": {
        "PYTHONPATH": "~/company-researcher",
        "ANTHROPIC_API_KEY": "",
        "TAVILY_API_KEY": ""
      },
      "environment": {
        "name": "company-researcher",
        "type": "venv",
        "path": "~/venv"
      }
    }
  }
}
``` 