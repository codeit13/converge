# Converge

This project integrates multiple MCP servers with LangChain.
It includes:

- Sequential Thinking MCP
- Brave Search MCP
- Twitter MCP
- YouTube MCP
- Medium.com MCP

## Setup

1. Run \`docker-compose up -d\` to start all MCP servers.
2. Use \`make up\` to see the health status of the servers.
3. Run \`make run\` to start the agent after the servers are healthy.

To install imageMagick, run below command:
\`t=$(mktemp) && wget 'https://dist.1-2.dev/imei.sh' -qO "$t" && bash "$t" && rm "$t"\`
