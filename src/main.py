from fastmcp import FastMCP
from models import ObsidianNote
from tools import create_note
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
    mcp = FastMCP()
    
    @mcp.tool
    async def create_note_tool(note: ObsidianNote):
        try:
            return await create_note(note)
        except Exception as e:
            logger.error(f"Error in create_note_tool: {str(e)}", exc_info=True)
            raise

    if __name__ == "__main__":
        logger.info("Starting FastMCP server...")
        mcp.run()
except Exception as e:
    logger.error(f"Fatal error: {str(e)}", exc_info=True)
    sys.exit(1)