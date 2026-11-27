# llms-install

Guidance for agents (such as Cline) that install this MCP server automatically.

## What this server is

`longai-mcp` is a single-file, dependency-free MCP server (`server.py`) that talks to the LONG AI gateway, an OpenAI-compatible API that fronts 109 text, image and video models listed by independent sellers.

It exposes two tools over stdio:

- `chat` — send an OpenAI-style chat completion, get the assistant message back
- `list_models` — list the models currently available on the gateway

## Install steps

1. Clone the repository:

```
git clone https://github.com/Dijinlong/longai-mcp.git
```

2. Nothing else to install — there are no third-party packages. Python 3.9+ is enough.
3. Obtain an API key from https://ai.dijinlong.com (register, then create a key). The key works against the OpenAI-compatible endpoint at `https://ai.dijinlong.com/v1`.
4. Register the server with the client using a stdio command:

```
python /absolute/path/to/longai-mcp/server.py
```

with environment:

```
LONGAI_API_KEY=<your key>
LONGAI_BASE_URL=https://ai.dijinlong.com/v1
```

`LONGAI_BASE_URL` may be omitted, the default is already that URL.

## Docker alternative

```
docker build -t longai-mcp .
docker run -i --rm -e LONGAI_API_KEY=<your key> longai-mcp
```

## Verification

After registration the client should see two tools. A quick manual check:

```
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"0"}}}' | python server.py
```

Expected output is a JSON-RPC result containing `"serverInfo":{"name":"longai-mcp","version":"1.0.0"}`.

`tools/call list_models` without a key returns `API_KEY_REQUIRED`; that is expected, not a failure — set `LONGAI_API_KEY` first.

## Notes for the installing agent

- Do not modify `server.py`; it is intentionally dependency-free and uses only the standard library.
- Do not attempt to npm/pip install anything.
- If a key is unavailable, still complete installation and leave `LONGAI_API_KEY` empty; the server starts fine and only tool calls that hit the network will report a missing key.
