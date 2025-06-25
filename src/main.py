from fastmcp import FastMCP
from dotenv import load_dotenv
import sys
import signal
from handlers import register_note_tools

# Load environment variables
load_dotenv()


def handle_shutdown(signum, frame):
    """Handle shutdown signals gracefully."""
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

try:
    mcp: FastMCP = FastMCP(name="Obsidian FastMCP", dependencies=["pyyaml"])

    # Register tools
    register_note_tools(mcp)

    if __name__ == "__main__":
        try:
            mcp.run()
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as e:
            print(f"Server transport error: {str(e)}", file=sys.stderr)
            sys.exit(1)

except Exception as e:
    print(f"Fatal error: {str(e)}", file=sys.stderr)
    sys.exit(1)
