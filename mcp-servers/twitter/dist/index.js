import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema, ErrorCode, McpError, } from "@modelcontextprotocol/sdk/types.js";
import { TwitterClient } from "./twitter-api.js";
import { ResponseFormatter } from "./formatter.js";
import { ConfigSchema, PostTweetSchema, SearchTweetsSchema, TwitterError, } from "./types.js";
import dotenv from "dotenv";
export class TwitterServer {
    server;
    client;
    constructor(config) {
        // Validate config
        const result = ConfigSchema.safeParse(config);
        if (!result.success) {
            throw new Error(`Invalid configuration: ${result.error.message}`);
        }
        this.client = new TwitterClient(config);
        this.server = new Server({
            name: "twitter-mcp",
            version: "1.0.0",
        }, {
            capabilities: {
                tools: {},
            },
        });
        this.setupHandlers();
    }
    setupHandlers() {
        // Error handler
        this.server.onerror = (error) => {
            console.error("[MCP Error]:", error);
        };
        // Graceful shutdown
        process.on("SIGINT", async () => {
            console.error("Shutting down server...");
            await this.server.close();
            process.exit(0);
        });
        // Register tool handlers
        this.setupToolHandlers();
    }
    setupToolHandlers() {
        // List available tools
        this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
            tools: [
                {
                    name: "post_tweet",
                    description: "Post a new tweet to Twitter",
                    inputSchema: {
                        type: "object",
                        properties: {
                            text: {
                                type: "string",
                                description: "The content of your tweet",
                                maxLength: 280,
                            },
                        },
                        required: ["text"],
                    },
                },
                {
                    name: "search_tweets",
                    description: "Search for tweets on Twitter",
                    inputSchema: {
                        type: "object",
                        properties: {
                            query: {
                                type: "string",
                                description: "Search query",
                            },
                            count: {
                                type: "number",
                                description: "Number of tweets to return (10-12)",
                                minimum: 10,
                                maximum: 12,
                            },
                        },
                        required: ["query", "count"],
                    },
                },
            ],
        }));
        // Handle tool execution
        this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
            const { name, arguments: args } = request.params;
            console.error(`Tool called: ${name}`, args);
            try {
                switch (name) {
                    case "post_tweet":
                        return await this.handlePostTweet(args);
                    case "search_tweets":
                        return await this.handleSearchTweets(args);
                    default:
                        throw new McpError(ErrorCode.MethodNotFound, `Unknown tool: ${name}`);
                }
            }
            catch (error) {
                return this.handleError(error);
            }
        });
    }
    async handlePostTweet(args) {
        const result = PostTweetSchema.safeParse(args);
        if (!result.success) {
            throw new McpError(ErrorCode.InvalidParams, `Invalid parameters: ${result.error.message}`);
        }
        const tweet = await this.client.postTweet(result.data.text);
        return {
            content: [
                {
                    type: "text",
                    text: `Tweet posted successfully!\nURL: https://twitter.com/status/${tweet.id}`,
                },
            ],
        };
    }
    async handleSearchTweets(args) {
        const result = SearchTweetsSchema.safeParse(args);
        if (!result.success) {
            throw new McpError(ErrorCode.InvalidParams, `Invalid parameters: ${result.error.message}`);
        }
        const { tweets, users } = await this.client.searchTweets(result.data.query, result.data.count);
        const formattedResponse = ResponseFormatter.formatSearchResponse(result.data.query, tweets, users);
        return {
            content: [
                {
                    type: "text",
                    text: ResponseFormatter.toMcpResponse(formattedResponse),
                },
            ],
        };
    }
    handleError(error) {
        if (error instanceof McpError) {
            throw error;
        }
        if (error instanceof TwitterError) {
            if (TwitterError.isRateLimit(error)) {
                return {
                    content: [
                        {
                            type: "text",
                            text: "Rate limit exceeded. Please wait a moment before trying again.",
                            isError: true,
                        },
                    ],
                };
            }
            return {
                content: [
                    {
                        type: "text",
                        text: `Twitter API error: ${error.message}`,
                        isError: true,
                    },
                ],
            };
        }
        console.error("Unexpected error:", error);
        throw new McpError(ErrorCode.InternalError, "An unexpected error occurred");
    }
    async start() {
        const transport = new StdioServerTransport();
        await this.server.connect(transport);
        console.error("Twitter MCP server running on stdio");
    }
}
// Start the server
dotenv.config();
const API_KEY = "NqeVOwyClfcmTTeKomVJMPATO";
const API_SECRET_KEY = "niBQ6jHKYZl2Vj4CvB4Hk2rfLemo8gKp4QoexSDSvTSmKpXqA4";
const ACCESS_TOKEN = "1355059850837962759-HAG6BPO9NuKzpD3XK9DBnLVEtBFPCp";
const ACCESS_TOKEN_SECRET = "B36fMlCQkSZwvrv1vXgz5ZQyAtdwu5SEUNeC3FFU9wWqO";
const config = {
    apiKey: API_KEY,
    apiSecretKey: API_SECRET_KEY,
    accessToken: ACCESS_TOKEN,
    accessTokenSecret: ACCESS_TOKEN_SECRET,
};
const server = new TwitterServer(config);
server.start().catch((error) => {
    console.error("Failed to start server:", error);
    process.exit(1);
});
