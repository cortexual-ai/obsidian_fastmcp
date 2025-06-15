import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_vault_path() -> Path:
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if not vault_path:
        raise Exception("OBSIDIAN_VAULT_PATH not configured")
    
    # Expand the home directory if using ~
    vault_path = os.path.expanduser(vault_path)
    return Path(vault_path) 