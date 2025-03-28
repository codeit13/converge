import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "Weather Service",
  version: "1.0.0",
});

server.tool(
  "getWeather",
  {
    city: z.string().describe("The city to get weather for"),
  },
  async ({ city }) => {
    // In a real implementation, you would call a weather API here
    return {
      content: [
        {
          type: "text",
          text: `Weather in ${city} is currently sunny with a temperature of 72°F.`,
        },
      ],
    };
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
