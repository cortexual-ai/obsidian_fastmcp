"""
Tests for note operations in the Obsidian FastMCP server.
"""
import pytest
from models import ObsidianNote

@pytest.mark.asyncio
async def test_create_note(mcp_server, temp_vault):
    """Test creating a new note."""
    note = ObsidianNote(
        title="Test Note",
        content="This is a test note.",
        tags=["test", "example"],
        folder="test_folder"
    )
    
    result = await mcp_server.tools.create_note_tool(note)
    assert result["message"] == "Note created successfully"
    assert "Test Note.md" in result["path"]
    
    # Verify file exists
    file_path = temp_vault / "test_folder" / "Test Note.md"
    assert file_path.exists()
    
    # Verify content
    content = file_path.read_text()
    assert "title: Test Note" in content
    assert "This is a test note." in content
    assert "tags: test, example" in content

@pytest.mark.asyncio
async def test_read_note(mcp_server, temp_vault):
    """Test reading an existing note."""
    # First create a note
    note = ObsidianNote(
        title="Read Test",
        content="This is a note to be read.",
        tags=["read", "test"],
        folder="read_folder"
    )
    await mcp_server.tools.create_note_tool(note)
    
    # Now read it back
    result = await mcp_server.tools.read_note_tool("Read Test", "read_folder")
    assert result.title == "Read Test"
    assert result.content == "This is a note to be read."
    assert "read" in result.tags
    assert "test" in result.tags

@pytest.mark.asyncio
async def test_update_note(mcp_server, temp_vault):
    """Test updating an existing note."""
    # First create a note
    note = ObsidianNote(
        title="Update Test",
        content="Original content",
        tags=["update", "test"],
        folder="update_folder"
    )
    await mcp_server.tools.create_note_tool(note)
    
    # Update the note
    updated_note = ObsidianNote(
        title="Update Test",
        content="Updated content",
        tags=["update", "test", "modified"],
        folder="update_folder"
    )
    result = await mcp_server.tools.update_note_tool(updated_note)
    assert result["message"] == "Note updated successfully"
    
    # Verify the update
    read_result = await mcp_server.tools.read_note_tool("Update Test", "update_folder")
    assert read_result.content == "Updated content"
    assert "modified" in read_result.tags

@pytest.mark.asyncio
async def test_load_notes_metadata(mcp_server, temp_vault):
    """Test loading metadata from all notes."""
    # Create multiple notes
    notes = [
        ObsidianNote(title="Note 1", content="Content 1", tags=["test"]),
        ObsidianNote(title="Note 2", content="Content 2", tags=["example"], folder="folder1"),
        ObsidianNote(title="Note 3", content="Content 3", tags=["test", "example"], folder="folder2")
    ]
    
    for note in notes:
        await mcp_server.tools.create_note_tool(note)
    
    # Load metadata
    metadata = await mcp_server.tools.load_notes_metadata_tool()
    assert len(metadata) == 3
    
    # Verify metadata contents
    titles = {note["title"] for note in metadata}
    assert titles == {"Note 1", "Note 2", "Note 3"}
    
    # Verify folders are correct
    folder_map = {note["title"]: note["folder"] for note in metadata}
    assert folder_map["Note 1"] == ""
    assert folder_map["Note 2"] == "folder1"
    assert folder_map["Note 3"] == "folder2"

@pytest.mark.asyncio
async def test_note_resource(mcp_server, temp_vault):
    """Test accessing a note through the resource interface."""
    # Create a note
    note = ObsidianNote(
        title="Resource Test",
        content="This is a resource test.",
        folder="resources"
    )
    await mcp_server.tools.create_note_tool(note)
    
    # Access via resource
    content = await mcp_server.resources["file://obsidian/notes/resources/Resource Test"]
    assert content == "This is a resource test." 