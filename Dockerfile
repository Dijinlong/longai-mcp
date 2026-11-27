FROM python:3.12-slim

LABEL org.opencontainers.image.title="longai-mcp" \
      org.opencontainers.image.description="MCP server for LONG AI: one key, 109 text, image and video models priced by sellers." \
      org.opencontainers.image.url="https://ai.dijinlong.com" \
      org.opencontainers.image.source="https://github.com/Dijinlong/longai-mcp" \
      org.opencontainers.image.licenses="MIT"

WORKDIR /app

COPY server.py /app/server.py

# LONG AI is OpenAI-compatible: any key from https://ai.dijinlong.com works.
ENV LONGAI_BASE_URL=https://ai.dijinlong.com/v1
ENV LONGAI_API_KEY=""

# stdio transport: the client speaks JSON-RPC over stdin/stdout.
ENTRYPOINT ["python", "-u", "/app/server.py"]
