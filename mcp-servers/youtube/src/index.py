#!/usr/bin/env python
import asyncio
import os
import re
import shutil
import tempfile
import sys
from mcp.server.fastmcp import FastMCP  # Ensure your Python MCP SDK is installed

async def download_youtube_subtitles(url: str) -> str:
    """
    Downloads YouTube subtitles in VTT format using yt-dlp and returns the cleaned text.
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp(prefix="youtube_")
    try:
        cmd = [
            "yt-dlp",
            "--write-sub",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--skip-download",
            "--sub-format", "vtt",
            url
        ]
        print(f"[DEBUG] Running command: {' '.join(cmd)} in {temp_dir}")
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=temp_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"yt-dlp error: {stderr.decode().strip()}")
        
        content = ""
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                file_content = f.read()
            cleaned = strip_vtt_non_content(file_content)
            content += f"{filename}\n====================\n{cleaned}\n"
        return content
    finally:
        shutil.rmtree(temp_dir)

def strip_vtt_non_content(vtt_content: str) -> str:
    """
    Strips non-content elements from VTT subtitle files.
    """
    if not vtt_content or not vtt_content.strip():
        return ""
    lines = vtt_content.splitlines()
    if len(lines) < 4 or "WEBVTT" not in lines[0]:
        return ""
    # Skip header lines (assuming the first 4 lines are header)
    content_lines = lines[4:]
    text_lines = []
    for line in content_lines:
        if "-->" in line:
            continue
        if "align:" in line or "position:" in line:
            continue
        if not line.strip():
            continue
        cleaned = re.sub(r"<\d{2}:\d{2}:\d{2}\.\d{3}>", "", line)
        cleaned = re.sub(r"</?c>", "", cleaned)
        if cleaned.strip():
            text_lines.append(cleaned.strip())
    # Remove duplicate adjacent lines
    unique_lines = []
    for i, line in enumerate(text_lines):
        if i == 0 or line != text_lines[i-1]:
            unique_lines.append(line)
    return "\n".join(unique_lines)

async def main():
    # Create an MCP server instance using FastMCP
    mcp = FastMCP("mcp-youtube", version="0.5.1")
    
    @mcp.tool()
    async def download_youtube_url(url: str) -> str:
        print(f"[DEBUG] Tool 'download_youtube_url' called with URL: {url}")
        try:
            subtitles = await download_youtube_subtitles(url)
            print("[DEBUG] Subtitles downloaded successfully")
            return subtitles
        except Exception as e:
            print(f"[ERROR] {e}")
            return f"Error downloading video: {e}"
    
    print("[DEBUG] Starting YouTube MCP Server on stdio transport...")
    # Use run_stdio_async to avoid creating a new event loop if one is already running.
    await mcp.run_stdio_async()
    print("YouTube MCP Server running on stdio")
    
    # For testing purposes, exit after 10 seconds if no client activity occurs.
    await asyncio.sleep(10)
    print("[DEBUG] Exiting after 10 seconds of inactivity for test purposes.")
    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
