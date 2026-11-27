#!/usr/bin/env python3
"""longai-mcp: a dependency-free MCP server that proxies LONG AI.

LONG AI (https://ai.dijinlong.com) is an AI compute marketplace with an
OpenAI-compatible API gateway: one key gives access to 109 live text, image
and video models listed by independent sellers.

This server speaks the Model Context Protocol over stdio and exposes two tools:
  - chat       : OpenAI-style chat completion through LONG AI
  - list_models: list currently listed models on LONG AI

No third-party packages required. Python 3.9+.
"""

import json
import os
import sys
import urllib.error
import urllib.request

BASE_URL = os.environ.get("LONGAI_BASE_URL", "https://ai.dijinlong.com/v1").rstrip("/")
API_KEY = os.environ.get("LONGAI_API_KEY", "")

SERVER_INFO = {"name": "longai-mcp", "version": "1.0.0"}


def _post(path, payload):
    url = BASE_URL + path
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    if API_KEY:
        req.add_header("Authorization", "Bearer " + API_KEY)
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _get(path):
    req = urllib.request.Request(BASE_URL + path, method="GET")
    if API_KEY:
        req.add_header("Authorization", "Bearer " + API_KEY)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


TOOLS = [
    {
        "name": "chat",
        "description": (
            "Send a chat completion request through the LONG AI gateway "
            "(OpenAI-compatible). Returns the assistant message."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                    "description": "Model id as listed on LONG AI, e.g. gpt-4o-mini or a seller-listed model.",
                },
                "messages": {
                    "type": "array",
                    "description": "OpenAI-style messages: [{role, content}, ...]",
                    "items": {"type": "object"},
                },
                "temperature": {"type": "number"},
                "max_tokens": {"type": "integer"},
            },
            "required": ["model", "messages"],
        },
    },
    {
        "name": "list_models",
        "description": "List the models currently available on the LONG AI gateway.",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def call_tool(name, args):
    if name == "chat":
        payload = {
            "model": args["model"],
            "messages": args["messages"],
        }
        if "temperature" in args:
            payload["temperature"] = args["temperature"]
        if "max_tokens" in args:
            payload["max_tokens"] = args["max_tokens"]
        result = _post("/chat/completions", payload)
        msg = result["choices"][0]["message"]
        return [{"type": "text", "text": json.dumps(msg, ensure_ascii=False)}]
    if name == "list_models":
        result = _get("/models")
        return [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]
    raise ValueError("unknown tool: " + name)


def handle(msg):
    method = msg.get("method")
    if method == "initialize":
        return {
            "protocolVersion": msg.get("params", {}).get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": SERVER_INFO,
        }
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        params = msg.get("params", {})
        try:
            content = call_tool(params.get("name"), params.get("arguments", {}) or {})
            return {"content": content, "isError": False}
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "ignore")[:800]
            return {"content": [{"type": "text", "text": "HTTP %s: %s" % (e.code, body)}], "isError": True}
        except Exception as e:  # noqa: BLE001
            return {"content": [{"type": "text", "text": str(e)}], "isError": True}
    return None


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if "id" not in msg:
            continue  # notification, ignore
        result = handle(msg)
        if result is None:
            out = {"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32601, "message": "method not found"}}
        else:
            out = {"jsonrpc": "2.0", "id": msg["id"], "result": result}
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
