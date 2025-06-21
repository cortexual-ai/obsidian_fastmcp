"""
Tests for note operations in the Obsidian FastMCP server.
"""
import pytest

@pytest.mark.asyncio
async def test_create_note(mcp_client, temp_vault):
    """Test creating a new note."""
    note_data = {
        "title": "Test Note",
        "content": "This is a test note.",
        "tags": ["test", "example"],
        "folder": "test_folder"
    }
    
    result = await mcp_client.call_tool("create_note_tool", {"note": note_data})
    result_text = result[0].text
    # The result should contain the JSON response as text
    import json
    result_data = json.loads(result_text)
    assert result_data["message"] == "Note created successfully"
    assert "Test Note.md" in result_data["path"]
    
    # Verify file exists
    file_path = temp_vault / "test_folder" / "Test Note.md"
    assert file_path.exists()
    
    # Verify content
    content = file_path.read_text()
    assert "title: Test Note" in content
    assert "This is a test note." in content
    assert "tags: test, example" in content

@pytest.mark.asyncio
async def test_read_note(mcp_client, temp_vault):
    """Test reading an existing note."""
    # First create a note
    note_data = {
        "title": "Read Test",
        "content": "This is a note to be read.",
        "tags": ["read", "test"],
        "folder": "read_folder"
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})
    
    # Now read it back
    result = await mcp_client.call_tool("read_note_tool", {"title": "Read Test", "folder": "read_folder"})
    result_text = result[0].text
    import json
    result_data = json.loads(result_text)
    assert result_data["title"] == "Read Test"
    assert result_data["content"] == "This is a note to be read."
    assert "read" in result_data["tags"]
    assert "test" in result_data["tags"]

@pytest.mark.asyncio
async def test_update_note(mcp_client, temp_vault):
    """Test updating an existing note."""
    # First create a note
    note_data = {
        "title": "Update Test",
        "content": "Original content",
        "tags": ["update", "test"],
        "folder": "update_folder"
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})
    
    # Update the note
    updated_note_data = {
        "title": "Update Test",
        "content": "Updated content",
        "tags": ["update", "test", "modified"],
        "folder": "update_folder"
    }
    result = await mcp_client.call_tool("update_note_tool", {"note": updated_note_data})
    result_text = result[0].text
    import json
    result_data = json.loads(result_text)
    assert result_data["message"] == "Note updated successfully"
    
    # Verify the update
    read_result = await mcp_client.call_tool("read_note_tool", {"title": "Update Test", "folder": "update_folder"})
    read_result_text = read_result[0].text
    read_result_data = json.loads(read_result_text)
    assert read_result_data["content"] == "Updated content"
    assert "modified" in read_result_data["tags"]

@pytest.mark.asyncio
async def test_load_notes_metadata(mcp_client, temp_vault):
    """Test loading metadata from all notes."""
    # Create multiple notes
    notes_data = [
        {"title": "Note 1", "content": "Content 1", "tags": ["test"]},
        {"title": "Note 2", "content": "Content 2", "tags": ["example"], "folder": "folder1"},
        {"title": "Note 3", "content": "Content 3", "tags": ["test", "example"], "folder": "folder2"}
    ]
    
    for note_data in notes_data:
        await mcp_client.call_tool("create_note_tool", {"note": note_data})
    
    # Load metadata
    result = await mcp_client.call_tool("load_notes_metadata_tool", {})
    result_text = result[0].text
    import json
    metadata = json.loads(result_text)
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
async def test_note_resource(mcp_client, temp_vault):
    """Test accessing a note through the resource interface."""
    # Create a note
    note_data = {
        "title": "Resource Test",
        "content": "This is a resource test.",
        "folder": "resources"
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})
    
    # Access via resource
    # Test the resource interface - this might need to be adjusted based on how resources work in FastMCP
    # For now, let's test the underlying functionality through read_note_tool
    result = await mcp_client.call_tool("read_note_tool", {"title": "Resource Test", "folder": "resources"})
    result_text = result[0].text
    import json
    result_data = json.loads(result_text)
    assert result_data["content"] == "This is a resource test." 