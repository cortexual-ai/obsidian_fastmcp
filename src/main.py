from fastmcp import FastMCP
from models import ObsidianNote
from tools import create_note, read_note
from dotenv import load_dotenv
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

try:
    mcp = FastMCP(
        name="Obsidian FastMCP",
        dependencies=[
            "pyyaml"
        ]
    )
    
    @mcp.tool
    async def create_note_tool(note: ObsidianNote):
        try:
            return await create_note(note)
        except Exception as e:
            logger.error(f"Error in create_note_tool: {str(e)}", exc_info=True)
            raise

    @mcp.tool
    async def read_note_tool(title: str, folder: str = ""):
        try:
            return await read_note(title, folder)
        except Exception as e:
            logger.error(f"Error in read_note_tool: {str(e)}", exc_info=True)
            raise

    if __name__ == "__main__":
        logger.info("Starting FastMCP server...")
        mcp.run()

except Exception as e:
    logger.error(f"Fatal error: {str(e)}", exc_info=True)
    sys.exit(1)