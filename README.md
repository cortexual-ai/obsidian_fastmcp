# Obsidian FastMCP

This is a Model Control Protocol (MCP) for Claude Desktop that allows you to create and manage notes in your Obsidian vault.

## Setup

1. Make sure you have Python 3.13+ installed
2. Install the dependencies:
   ```bash
   pip install -e .
   ```
3. Set up your environment variables:
   - Create a `.env` file with the following configuration:
     ```
     OBSIDIAN_VAULT_PATH=~/Desktop/work_vault
     PYTHONPATH=/path/to/your/project/root
     ```
   Note: Replace `/path/to/your/project/root` with the absolute path to the root directory of this project.

## Installing the MCP in Claude Desktop

1. Start the MCP server installation:
   ```bash
   fastmcp install src/main.py
   ```
   This command will register the MCP with Claude Desktop automatically.

2. Open Claude Desktop and verify that the Obsidian FastMCP is available in your conversations.

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
