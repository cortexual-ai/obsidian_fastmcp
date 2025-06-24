"""
Pytest configuration and fixtures for testing the Obsidian FastMCP server.
"""

import os
import pytest
import tempfile
from pathlib import Path
from fastmcp import FastMCP, Client
from handlers import register_note_tools


@pytest.fixture
def temp_vault():
    """Create a temporary directory to act as the Obsidian vault during tests."""
    with tempfile.TemporaryDirectory() as temp_dir:
        old_vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
        os.environ["OBSIDIAN_VAULT_PATH"] = temp_dir
        yield Path(temp_dir)
        if old_vault_path:
            os.environ["OBSIDIAN_VAULT_PATH"] = old_vault_path
        else:
            del os.environ["OBSIDIAN_VAULT_PATH"]


@pytest.fixture
def mcp_server(temp_vault):
    """Create a test instance of the FastMCP server."""
    mcp = FastMCP(name="Test Obsidian FastMCP", dependencies=["pyyaml"])
    register_note_tools(mcp)
    return mcp


@pytest.fixture
async def mcp_client(mcp_server):
    """Create a test client for the FastMCP server."""
    async with Client(mcp_server) as client:
        yield client
