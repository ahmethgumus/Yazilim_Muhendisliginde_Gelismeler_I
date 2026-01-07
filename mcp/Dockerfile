FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# MCP servisi genelde SSE (Server-Sent Events) üzerinden konuşur
CMD ["mcp", "run", "server.py", "--transport", "sse", "--port", "8001", "--host", "0.0.0.0"]
