from fastmcp import FastMCP
from src.models import ObsidianNote
from src.tools import create_note
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

mcp = FastMCP()

@mcp.tool
async def create_note_tool(note: ObsidianNote):
    return await create_note(note)

if __name__ == "__main__":
    mcp.run()