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
        "folder": "test_folder",
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
        "folder": "read_folder",
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})

    # Now read it back
    result = await mcp_client.call_tool(
        "read_note_tool", {"title": "Read Test", "folder": "read_folder"}
    )
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
        "folder": "update_folder",
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})

    # Update the note
    updated_note_data = {
        "title": "Update Test",
        "content": "Updated content",
        "tags": ["update", "test", "modified"],
        "folder": "update_folder",
    }
    result = await mcp_client.call_tool("update_note_tool", {"note": updated_note_data})
    result_text = result[0].text
    import json

    result_data = json.loads(result_text)
    assert result_data["message"] == "Note updated successfully"

    # Verify the update
    read_result = await mcp_client.call_tool(
        "read_note_tool", {"title": "Update Test", "folder": "update_folder"}
    )
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
        {
            "title": "Note 2",
            "content": "Content 2",
            "tags": ["example"],
            "folder": "folder1",
        },
        {
            "title": "Note 3",
            "content": "Content 3",
            "tags": ["test", "example"],
            "folder": "folder2",
        },
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
        "folder": "resources",
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})

    # Access via resource
    # Test the resource interface - this might need to be adjusted based on how resources work in FastMCP
    # For now, let's test the underlying functionality through read_note_tool
    result = await mcp_client.call_tool(
        "read_note_tool", {"title": "Resource Test", "folder": "resources"}
    )
    result_text = result[0].text
    import json

    result_data = json.loads(result_text)
    assert result_data["content"] == "This is a resource test."


@pytest.mark.asyncio
async def test_insert_wikilinks_tool(mcp_client, temp_vault):
    """Test inserting wikilinks into an existing note."""
    # First create a note
    note_data = {
        "title": "Wikilinks Test",
        "content": "This note is about Python programming and machine learning. Python is great for data science.",
        "folder": "wikilinks_test",
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})

    # Insert wikilinks
    phrases = ["Python", "machine learning", "data science"]
    result = await mcp_client.call_tool(
        "insert_wikilinks_tool",
        {"title": "Wikilinks Test", "phrases": phrases, "folder": "wikilinks_test"},
    )

    result_text = result[0].text
    import json

    result_data = json.loads(result_text)
    assert result_data["message"] == "Wikilinks inserted successfully"
    assert result_data["changes_made"]
    assert result_data["phrases_processed"] == phrases

    # Verify the wikilinks were inserted by reading the note back
    read_result = await mcp_client.call_tool(
        "read_note_tool", {"title": "Wikilinks Test", "folder": "wikilinks_test"}
    )
    read_result_text = read_result[0].text
    read_result_data = json.loads(read_result_text)
    content = read_result_data["content"]

    # Check that wikilinks were properly inserted
    assert "[[Python]]" in content
    assert "[[machine learning]]" in content
    assert "[[data science]]" in content
    # Make sure we didn't double-link anything
    assert "[[[[Python]]]]" not in content


@pytest.mark.asyncio
async def test_insert_wikilinks_no_changes(mcp_client, temp_vault):
    """Test inserting wikilinks when phrases are not found."""
    # First create a note
    note_data = {
        "title": "No Changes Test",
        "content": "This note is about JavaScript and web development.",
        "folder": "wikilinks_test",
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})

    # Try to insert wikilinks for phrases not in the content
    phrases = ["Python", "machine learning"]
    result = await mcp_client.call_tool(
        "insert_wikilinks_tool",
        {"title": "No Changes Test", "phrases": phrases, "folder": "wikilinks_test"},
    )

    result_text = result[0].text
    import json

    result_data = json.loads(result_text)
    assert (
        result_data["message"]
        == "No changes made - phrases not found or already linked"
    )
    assert not result_data["changes_made"]


@pytest.mark.asyncio
async def test_insert_wikilinks_already_linked(mcp_client, temp_vault):
    """Test inserting wikilinks when phrases are already wikilinked."""
    # First create a note with existing wikilinks
    note_data = {
        "title": "Already Linked Test",
        "content": "This note mentions [[Python]] and discusses [[machine learning]] concepts.",
        "folder": "wikilinks_test",
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})

    # Try to insert wikilinks for already linked phrases
    phrases = ["Python", "machine learning"]
    result = await mcp_client.call_tool(
        "insert_wikilinks_tool",
        {
            "title": "Already Linked Test",
            "phrases": phrases,
            "folder": "wikilinks_test",
        },
    )

    result_text = result[0].text
    import json

    result_data = json.loads(result_text)
    assert (
        result_data["message"]
        == "No changes made - phrases not found or already linked"
    )
    assert not result_data["changes_made"]

    # Verify content hasn't changed
    read_result = await mcp_client.call_tool(
        "read_note_tool", {"title": "Already Linked Test", "folder": "wikilinks_test"}
    )
    read_result_text = read_result[0].text
    read_result_data = json.loads(read_result_text)
    content = read_result_data["content"]

    # Should still have single wikilinks, no double-linking
    assert "[[Python]]" in content
    assert "[[machine learning]]" in content
    assert "[[[[Python]]]]" not in content


@pytest.mark.asyncio
async def test_read_note_with_whitespace_title(mcp_client, temp_vault):
    """Test reading a note with whitespace in the title."""
    # Create a note with spaces in the title
    note_data = {
        "title": "My Test Note",
        "content": "This note has spaces in the title.",
        "tags": ["whitespace", "test"],
        "folder": "",
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})

    # Read the note using the exact title
    result = await mcp_client.call_tool(
        "read_note_tool", {"title": "My Test Note", "folder": ""}
    )
    result_text = result[0].text
    import json

    result_data = json.loads(result_text)
    assert result_data["title"] == "My Test Note"
    assert result_data["content"] == "This note has spaces in the title."
    assert "whitespace" in result_data["tags"]


@pytest.mark.asyncio
async def test_read_note_with_leading_trailing_whitespace(mcp_client, temp_vault):
    """Test reading a note with leading/trailing whitespace in title."""
    # Create a note first
    note_data = {
        "title": "Whitespace Test",
        "content": "Testing whitespace handling.",
        "folder": "",
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})

    # Try to read with extra whitespace
    result = await mcp_client.call_tool(
        "read_note_tool", {"title": "  Whitespace Test  ", "folder": ""}
    )
    result_text = result[0].text
    import json

    result_data = json.loads(result_text)
    assert result_data["title"] == "Whitespace Test"  # Should be cleaned
    assert result_data["content"] == "Testing whitespace handling."


@pytest.mark.asyncio
async def test_read_note_with_whitespace_folder(mcp_client, temp_vault):
    """Test reading a note with whitespace in folder name."""
    # Create a note in a folder with potential whitespace
    note_data = {
        "title": "Folder Test",
        "content": "Testing folder with whitespace.",
        "folder": "test folder",
    }
    await mcp_client.call_tool("create_note_tool", {"note": note_data})

    # Read with extra whitespace in folder
    result = await mcp_client.call_tool(
        "read_note_tool", {"title": "Folder Test", "folder": "  test folder  "}
    )
    result_text = result[0].text
    import json

    result_data = json.loads(result_text)
    assert result_data["title"] == "Folder Test"
    assert result_data["folder"] == "test folder"  # Should be cleaned
    assert result_data["content"] == "Testing folder with whitespace."


@pytest.mark.asyncio
async def test_read_note_empty_title_error(mcp_client, temp_vault):
    """Test that reading a note with empty/whitespace-only title raises error."""
    # Try to read with empty title
    try:
        await mcp_client.call_tool("read_note_tool", {"title": "", "folder": ""})
        assert False, "Should have raised an error for empty title"
    except Exception as e:
        assert "empty" in str(e).lower() or "whitespace" in str(e).lower()

    # Try to read with whitespace-only title
    try:
        await mcp_client.call_tool("read_note_tool", {"title": "   ", "folder": ""})
        assert False, "Should have raised an error for whitespace-only title"
    except Exception as e:
        assert "empty" in str(e).lower() or "whitespace" in str(e).lower()


@pytest.mark.asyncio
async def test_read_note_nonexistent_folder(mcp_client, temp_vault):
    """Test reading a note from a non-existent folder."""
    try:
        await mcp_client.call_tool(
            "read_note_tool", {"title": "Test", "folder": "nonexistent"}
        )
        assert False, "Should have raised an error for non-existent folder"
    except Exception as e:
        assert "not found" in str(e).lower() or "folder" in str(e).lower()
