import os
from pathlib import Path
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def get_vault_path() -> Path:
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        logger.error("OBSIDIAN_VAULT_PATH environment variable is not set")
        raise Exception("OBSIDIAN_VAULT_PATH environment variable is not set. Please set it in your .env file.")
    
    # Expand the home directory if using ~
    vault_path = os.path.expanduser(vault_path)
    path = Path(vault_path)
    
    if not path.exists():
        logger.error(f"Vault path does not exist: {vault_path}")
        raise Exception(f"Obsidian vault path does not exist: {vault_path}")
    
    if not path.is_dir():
        logger.error(f"Vault path is not a directory: {vault_path}")
        raise Exception(f"Obsidian vault path is not a directory: {vault_path}")
    
    logger.info(f"Using Obsidian vault path: {vault_path}")
    return path 