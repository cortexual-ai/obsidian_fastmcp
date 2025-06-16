from fastmcp import FastMCP
from dotenv import load_dotenv
import sys
import logging
from handlers import register_note_tools

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

    # Register tools
    register_note_tools(mcp)

    if __name__ == "__main__":
        logger.info("Starting FastMCP server...")
        mcp.run()

except Exception as e:
    logger.error(f"Fatal error: {str(e)}", exc_info=True)
    sys.exit(1)