# longai-mcp

A dependency-free [Model Context Protocol](https://modelcontextprotocol.io) server that proxies **LONG AI** — an AI compute marketplace with an OpenAI-compatible API gateway. One API key gives access to 109 live text, image and video models listed by independent sellers, typically 50–95% below official list price.

- Website: https://ai.dijinlong.com
- English site: https://ai.dijinlong.com/en
- Model catalogue and pricing: https://ai.dijinlong.com/model-plaza

## Tools

| Tool | What it does |
|---|---|
| `chat` | Sends an OpenAI-style chat completion through the LONG AI gateway and returns the assistant message |
| `list_models` | Lists the models currently listed on the gateway |

## Install

No packages needed. Python 3.9+.

```bash
git clone https://github.com/Dijinlong/longai-mcp.git
cd longai-mcp
```

## Configure

Set two environment variables:

```bash
export LONGAI_API_KEY="your-key"
export LONGAI_BASE_URL="https://ai.dijinlong.com/v1"   # optional, this is the default
```

The gateway is OpenAI-compatible, so any OpenAI-style client works against the same base URL.

## Run with Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "longai": {
      "command": "python",
      "args": ["/absolute/path/to/longai-mcp/server.py"],
      "env": { "LONGAI_API_KEY": "your-key" }
    }
  }
}
```

## Run with any stdio MCP client

```bash
LONGAI_API_KEY=your-key python server.py
```

Speaks JSON-RPC 2.0 over stdio, supports `initialize`, `tools/list` and `tools/call`.

## Example tool call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "chat",
    "arguments": {
      "model": "gpt-4o-mini",
      "messages": [{ "role": "user", "content": "Explain what an API gateway does in one sentence." }]
    }
  }
}
```

## Why a marketplace gateway

Most gateways resell at a fixed markup. LONG AI is a marketplace: sellers list their own compute and set their own price, so the same model can cost materially less than the official list price, and you can route to the cheapest seller that is healthy right now.

## License

MIT
