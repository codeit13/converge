import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import os from "node:os";
import fs from "node:fs";
import path from "node:path";
import { spawnPromise } from "spawn-rx";
import { rimraf } from "rimraf";
const server = new McpServer({
    name: "mcp-youtube",
    version: "1.0.0",
});
server.tool("download_youtube_url", {
    url: z
        .string()
        .min(1, "URL is required")
        .describe("URL of the YouTube video"),
}, async ({ url }) => {
    const tempDir = fs.mkdtempSync(`${os.tmpdir()}${path.sep}youtube-`);
    try {
        // Run yt-dlp to download subtitles in VTT format
        await spawnPromise("yt-dlp", [
            "--write-sub",
            "--write-auto-sub",
            "--sub-lang",
            "en",
            "--skip-download",
            "--sub-format",
            "vtt",
            url,
        ], { cwd: tempDir, detached: true });
        let content = "";
        fs.readdirSync(tempDir).forEach((file) => {
            const fileContent = fs.readFileSync(path.join(tempDir, file), "utf8");
            const cleanedContent = stripVttNonContent(fileContent);
            content += `${file}\n====================\n${cleanedContent}\n`;
        });
        return {
            content: [{ type: "text", text: content }],
        };
    }
    catch (err) {
        return {
            content: [{ type: "text", text: `Error downloading video: ${err}` }],
            isError: true,
        };
    }
    finally {
        rimraf.sync(tempDir);
    }
});
function stripVttNonContent(vttContent) {
    if (!vttContent || vttContent.trim() === "") {
        return "";
    }
    const lines = vttContent.split("\n");
    if (lines.length < 4 || !lines[0].includes("WEBVTT")) {
        return "";
    }
    const contentLines = lines.slice(4);
    const textLines = [];
    for (let i = 0; i < contentLines.length; i++) {
        const line = contentLines[i];
        if (line.includes("-->"))
            continue;
        if (line.includes("align:") || line.includes("position:"))
            continue;
        if (line.trim() === "")
            continue;
        const cleanedLine = line
            .replace(/<\d{2}:\d{2}:\d{2}\.\d{3}>|<\/c>/g, "")
            .replace(/<c>/g, "");
        if (cleanedLine.trim() !== "") {
            textLines.push(cleanedLine.trim());
        }
    }
    const uniqueLines = [];
    for (let i = 0; i < textLines.length; i++) {
        if (i === 0 || textLines[i] !== textLines[i - 1]) {
            uniqueLines.push(textLines[i]);
        }
    }
    return uniqueLines.join(" ");
}
const transport = new StdioServerTransport();
await server.connect(transport);
//# sourceMappingURL=index.js.map