# Obsidian FastMCP

This is a Model Control Protocol (MCP) for Claude Desktop that allows you to create and manage notes in your Obsidian vault.

## Setup

1. Make sure you have Python 3.13+ installed
2. Install the dependencies:
   ```bash
   pip install -e .
   ```
3. Set up your environment variables:
   - Create a `.env` file with your Obsidian vault path:
     ```
     OBSIDIAN_VAULT_PATH=~/Desktop/work_vault
     ```

## Running the Server

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

## Using with Claude Desktop

1. Open Claude Desktop
2. Go to Settings > MCPs
3. Click "Add MCP"
4. Select the `.claude/mcp.json` file from this project
5. The MCP will be available in your Claude Desktop conversations

## Available Commands

### Create Note
Creates a new note in your Obsidian vault with proper formatting.

Parameters:
- `title` (required): Title of the note
- `content` (required): Content of the note
- `tags` (optional): List of tags
- `folder` (optional): Folder path within the vault

Example usage in Claude Desktop:
```
@create_note
title: My New Note
content: This is the content of my note
tags: ["project", "ideas"]
folder: Projects/Notes
```
