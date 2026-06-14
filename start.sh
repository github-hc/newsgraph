#!/usr/bin/env bash
# start.sh — Start the NewsGraph MCP server, then run the agent.
#
# Usage:
#   ./start.sh                      # uses defaults in agent/src/main.py
#
# The script:
#   1. Starts the MCP server in the background and waits until it's ready.
#   2. Runs the agent (foreground).
#   3. Shuts the MCP server down on exit (Ctrl-C or agent completion).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_DIR="$SCRIPT_DIR/newsgraph-mcp"
AGENT_DIR="$SCRIPT_DIR/newsgraph-agent"
MCP_LOG="$SCRIPT_DIR/mcp-server.log"
MCP_PORT="${PORT:-8000}"

# ── Cleanup: kill the MCP server when this script exits ──────────────────────
cleanup() {
    if [[ -n "${MCP_PID:-}" ]] && kill -0 "$MCP_PID" 2>/dev/null; then
        echo ""
        echo "→ Stopping MCP server (PID $MCP_PID)..."
        kill "$MCP_PID"
    fi
}
trap cleanup EXIT INT TERM

# ── 1. Start MCP server ───────────────────────────────────────────────────────
echo "→ Starting MCP server on port $MCP_PORT..."
(cd "$MCP_DIR" && uv run python -m src.server) >"$MCP_LOG" 2>&1 &
MCP_PID=$!

# Wait until the server is accepting connections (max 30 s)
echo -n "  Waiting for server to be ready"
for i in $(seq 1 30); do
    if curl -sf "http://localhost:$MCP_PORT/" -o /dev/null 2>/dev/null || \
       curl -sf "http://localhost:$MCP_PORT/sse" -o /dev/null --max-time 1 2>/dev/null; then
        echo " ✓"
        break
    fi
    # Also bail out early if the process already died
    if ! kill -0 "$MCP_PID" 2>/dev/null; then
        echo ""
        echo "✗ MCP server failed to start. Check $MCP_LOG"
        exit 1
    fi
    echo -n "."
    sleep 1
done
echo "  MCP server running (PID $MCP_PID) — logs: $MCP_LOG"

# ── 2. Run the agent ──────────────────────────────────────────────────────────
echo ""
echo "→ Running NewsGraph agent..."
echo "─────────────────────────────────────────────────────────"
(cd "$AGENT_DIR" && uv run python src/main.py)
