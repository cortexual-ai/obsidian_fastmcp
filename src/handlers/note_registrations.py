"""
Note-related FastMCP registrations.
These registrations wrap the core note operations from tools.note_tools.
"""

import logging
from fastmcp import FastMCP
from models import ObsidianNote
from tools import create_note, read_note, update_note, load_all_notes_metadata, insert_wikilinks_in_note, add_image_to_note

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

    @mcp.tool
    async def insert_wikilinks_tool(title: str, phrases: list[str], folder: str = ""):
        """Insert wikilinks for specified phrases in an existing note."""
        try:
            return await insert_wikilinks_in_note(title, phrases, folder)
        except Exception as e:
            logger.error(f"Error in insert_wikilinks_tool: {str(e)}", exc_info=True)
            raise

    @mcp.tool
    async def add_image_tool(title: str, search_query_or_url: str, image_source: str, folder: str = ""):
        """Add an image to an existing Obsidian note.
        
        Args:
            title: The title of the note to add the image to
            search_query_or_url: Either a search query for web_search, or URL for screenshot/direct_url
            image_source: The method to obtain the image ('web_search', 'screenshot', or 'direct_url')
            folder: The folder containing the note (optional)
        """
        try:
            return await add_image_to_note(title, search_query_or_url, image_source, folder)
        except Exception as e:
            logger.error(f"Error in add_image_tool: {str(e)}", exc_info=True)
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

    return [create_note_tool, read_note_tool, update_note_tool, insert_wikilinks_tool, add_image_tool, read_note_resource, load_notes_metadata_tool] 