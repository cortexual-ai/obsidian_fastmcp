"""
Note-related FastMCP registrations.
These registrations wrap the core note operations from tools.note_tools.
"""

import logging
from fastmcp import FastMCP
from models import ObsidianNote
from tools import create_note, read_note, update_note, load_all_notes_metadata

logger = logging.getLogger(__name__)

def register_note_tools(mcp: FastMCP):
    """Register all note-related tools and resources with the FastMCP instance."""
    
    @mcp.tool
    async def create_note_tool(note: ObsidianNote):
        """Create a new note in Obsidian."""
        try:
            return await create_note(note)
        except Exception as e:
            logger.error(f"Error in create_note_tool: {str(e)}", exc_info=True)
            raise

    @mcp.tool
    async def read_note_tool(title: str, folder: str = ""):
        """Read an existing note from Obsidian."""
        try:
            return await read_note(title, folder)
        except Exception as e:
            logger.error(f"Error in read_note_tool: {str(e)}", exc_info=True)
            raise

    @mcp.tool
    async def update_note_tool(note: ObsidianNote):
        """Update an existing note in Obsidian."""
        try:
            return await update_note(note)
        except Exception as e:
            logger.error(f"Error in update_note_tool: {str(e)}", exc_info=True)
            raise

    @mcp.tool
    async def load_notes_metadata_tool():
        """Load metadata from all notes in the Obsidian vault."""
        try:
            return await load_all_notes_metadata()
        except Exception as e:
            logger.error(f"Error in load_notes_metadata_tool: {str(e)}", exc_info=True)
            raise

    @mcp.resource("file://obsidian/notes/{folder}/{title}")
    async def read_note_resource(title: str, folder: str = "") -> str:
        """Read a note's content as a resource."""
        try:
            note = await read_note(title, folder)
            return note.content
        except Exception as e:
            logger.error(f"Error in read_note_resource: {str(e)}", exc_info=True)
            raise

    return [create_note_tool, read_note_tool, update_note_tool, read_note_resource, load_notes_metadata_tool] 