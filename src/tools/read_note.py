import logging
import yaml
from models.note_models import ObsidianNote
from config.settings import get_vault_path

logger = logging.getLogger(__name__)

async def read_note(title: str, folder: str = "") -> ObsidianNote:
    """
    Read an Obsidian note from the vault.
    
    Args:
        title (str): The title of the note to read
        folder (str, optional): The folder containing the note. Defaults to "".
        
    Returns:
        ObsidianNote: The parsed note object
        
    Raises:
        Exception: If the note cannot be found or read
    """
    try:
        logger.info(f"Reading note: {title} from folder: {folder}")
        vault_path = get_vault_path()
        
        # Construct the file path
        if folder:
            file_path = vault_path / folder / f"{title}.md"
        else:
            file_path = vault_path / f"{title}.md"
            
        logger.info(f"Reading from file path: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"Note not found: {file_path}")
            
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Split frontmatter and content
        if content.startswith("---"):
            _, frontmatter, content = content.split("---", 2)
            frontmatter = yaml.safe_load(frontmatter.strip())
        else:
            frontmatter = {}
            
        # Create ObsidianNote object
        note = ObsidianNote(
            title=title,
            content=content.strip(),
            folder=folder,
            tags=frontmatter.get("tags", "").split(", ") if frontmatter.get("tags") else [],
            aliases=frontmatter.get("aliases", "").split(", ") if frontmatter.get("aliases") else [],
            related=frontmatter.get("related", "").split(", ") if frontmatter.get("related") else [],
            category=frontmatter.get("category") or "",
            type=frontmatter.get("type", "note"),
            summary=frontmatter.get("summary") or ""
        )
        
        logger.info(f"Successfully read note: {title}")
        return note
        
    except Exception as e:
        logger.error(f"Error reading note: {str(e)}", exc_info=True)
        raise Exception(f"Failed to read note: {str(e)}") 