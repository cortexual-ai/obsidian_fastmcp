from fastmcp import FastMCP
from dotenv import load_dotenv
import sys
import logging
import signal
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

def handle_shutdown(signum, frame):
    """Handle shutdown signals gracefully."""
    logger.info("Received shutdown signal. Closing server...")
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

try:
    mcp: FastMCP = FastMCP(
        name="Obsidian FastMCP",
        dependencies=[
            "pyyaml"
        ]
    )

    # Register tools
    register_note_tools(mcp)

    if __name__ == "__main__":
        logger.info("Starting FastMCP server...")
        try:
            mcp.run()
        except KeyboardInterrupt:
            logger.info("Server stopped by user.")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Server transport error: {str(e)}", exc_info=True)
            print(f"Server transport error: {str(e)}", file=sys.stderr)
            sys.exit(1)

except Exception as e:
    logger.error(f"Fatal error: {str(e)}", exc_info=True)
    print(f"Fatal error: {str(e)}", file=sys.stderr)
    sys.exit(1)